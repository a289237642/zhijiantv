# -*- coding:utf-8 -*-
# author: will
import json
import random
import re

import time

import datetime
from flask import jsonify, g
from flask import request
from pymongo import MongoClient

from app import db, mongo_store, es_store
from app.models import Article, ArticleGroup, Group, Banner, UserBTN, UpdateTime, ZhiHuData, Top, ArticleKeyWords
from config.keys_config import KeysConfig
from utils.article_service.article_model_build import ArticleModel
from utils.article_service.keywords_filter import ArticleFilter
from utils.log_service import Logging
from utils.redis_service.Redis_Client import RedisClient
from utils.user_service.login import login_required, admin_required, auth_required
from utils.time_service import get_time
from utils.spider_service.upload import Upload
from utils.spider_service.wechat_url_spider import wechat_url_spider
from utils.spider_service.wechat_url_spider_new import WechatUrlSpider
from . import api_article
from celery_tasks.tasks import get_audio_baidu


# 获取文章分类类别
@api_article.route('/groups')
# @auth_required
def groups():
    groups = Group.query.filter(Group.is_show == 1).all()
    group_list = []
    for group in groups:
        group_dict = {}
        group_dict['group_id'] = group.id
        group_dict['group_name'] = group.name

        group_list.append(group_dict)

    return jsonify(errno=0, errmsg="OK", data=group_list)


# pc获取文章分类类别
@api_article.route('/pc_groups')
# @login_required
# @admin_required
def pc_groups():
    groups = Group.query.order_by(Group.sort_num, Group.id).all()
    group_list = []
    for group in groups:
        group_dict = {}
        group_dict['group_id'] = "BL" + str(group.id).zfill(6)
        group_dict['group_name'] = group.name
        group_dict['is_show'] = group.is_show
        group_dict['sort_num'] = group.sort_num

        group_list.append(group_dict)

    return jsonify(errno=0, errmsg="OK", data=group_list)


# 更新pc爆料库文章类型
@api_article.route('/update_group', methods=['POST'])
@login_required
@admin_required
def update_group():
    try:
        res = request.get_json()
        name = res.get('name')
        group_id = res.get('group_id')
        sort_num = res.get('sort_num')

        Logging.logger.info('request_args:{0}'.format(res))
        if group_id:
            # 修改
            try:
                group_id = int(group_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg='参数错误,请传入int类型的group_id')

            obj = Group.query.get(group_id)
            if not obj:
                return jsonify(errno=-1, errmsg='参数错误,该分类不存在')

            if name:
                obj.name = name
            else:
                obj.name = obj.name

            if sort_num:
                # 自定义排序
                try:
                    sort_num = int(sort_num)
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                groups = Group.query.all()
                total_num = len(groups)
                if sort_num > total_num:
                    return jsonify(errno=-1, errmsg='参数错误,传入的sort_num值超出范围')

                for group in groups:
                    # 往前调 10-->1
                    if obj.sort_num > sort_num:
                        # 选取修改范围
                        if sort_num <= group.sort_num < obj.sort_num:
                            # 先加再赋值
                            group.sort_num += 1
                            db.session.add(group)

                    # 往后调 1-->10
                    elif obj.sort_num < sort_num:
                        # 选取修改范围
                        if obj.sort_num < group.sort_num <= sort_num:
                            # 先减再赋值
                            group.sort_num -= 1
                            db.session.add(group)

                    else:
                        # 文章位置不变
                        obj.sort_num = sort_num
                # 赋值
                obj.sort_num = sort_num
                db.session.add(obj)

        else:
            # 新增
            if not name:
                return jsonify(errno=-1, errmsg='请传入新增的类别名')

            groups = Group.query.all()
            if not sort_num:
                count = len(groups)
                obj = Group()
                obj.name = name
                obj.sort_num = count + 1
                db.session.add(obj)

            else:
                # 自定义排序
                try:
                    sort_num = int(sort_num)
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                total_num = len(groups) + 1
                if sort_num > total_num:
                    return jsonify(errno=-1, errmsg='参数错误,传入的sort_num值超出范围')

                for group_obj in groups:
                    if group_obj.sort_num >= sort_num:
                        group_obj.sort_num += 1
                        db.session.add(group_obj)

                obj = Group()
                obj.name = name
                obj.sort_num = sort_num
                db.session.add(obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc爆料库启用或禁用文章分类类别
@api_article.route('/start_group', methods=['POST'])
@login_required
@admin_required
def start_group():
    res = request.get_json()
    group_id = res.get('group_id')

    Logging.logger.info('request_args:{0}'.format(res))
    if not group_id:
        return jsonify(errno=-1, errmsg='参数错误,请传入设置类型的group_id')

    obj = Group.query.get(group_id)
    if not obj:
        return jsonify(errno=-1, errmsg='参数错误,该分类不存在')

    if obj.is_show == 1:
        obj.is_show = 0
    else:
        obj.is_show = 1

    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
    return jsonify(errno=0, errmsg="OK")


# pc根据文章类别关键字模糊搜索
@api_article.route('/group_search', methods=['POST'])
@login_required
@admin_required
def group_search():
    try:
        res = request.get_json()
        words = res.get('words')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if words:
            all_results = Group.query.filter(Group.name.like("%" + words + "%")
                                             ).order_by(Group.id.desc()).paginate(page, pagesize, False)
        else:
            all_results = Group.query.filter().order_by(Group.id.desc()).paginate(page, pagesize, False)

        res_count = all_results.total
        group_list = list()
        for group in all_results.items:
            group_dict = dict()
            group_dict['group_id'] = "BL" + str(group.id).zfill(6)
            group_dict['group_name'] = group.name
            group_dict['is_show'] = group.is_show
            group_dict['sort_num'] = group.sort_num
            group_list.append(group_dict)

        return jsonify(errno=0, errmsg="OK", count=res_count, data=group_list)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章搜索失败')


# pc删除爆料库文章分类类别
@api_article.route('/del_group', methods=['POST'])
@login_required
@admin_required
def del_group():
    try:
        res = request.get_json()
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            jsonify(errno=-1, errmsg='参数错误,请传入删除的文章类别的group_id')
        obj = Group.query.get(group_id)
        if not obj:
            return jsonify(errno=-1, errmsg='参数错误,该分类不存在')

        # 修改所有类型的sort_num
        groups = Group.query.all()
        for group in groups:
            if group.sort_num > obj.sort_num:
                group.sort_num -= 1
                db.session.add(group)
        db.session.delete(obj)

        # 移除当前分组下所有的文章
        results = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).all()
        for result in results:
            article_id = result.article_id
            db.session.delete(result)

            group = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
            num = len(group)
            if num == 0:
                article = Article.query.get(article_id)
                article.is_show = 0
                article.zj_art_date = ""
                db.session.add(article)

        # 移除当前分组下面的所有关键词
        redis_client = RedisClient.create_redis_cli()
        keys = ArticleKeyWords.query.filter(ArticleKeyWords.article_group_id == group_id).all()
        for key in keys:
            first_keywords = key.first_keywords
            second_keywords = key.second_keywords
            for first_word in first_keywords.split(','):
                redis_client.hdel('group_id_of_keyword', first_word)

            for second_word in second_keywords.split(','):
                redis_client.hdel('group_id_of_keyword', second_word)
            db.session.delete(key)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc上线和未上线的全部文章列表
@api_article.route('/articles', methods=['POST'])
@login_required
@admin_required
def articles():
    res = request.get_json()
    page = res.get('page', 1)
    pagesize = res.get('pagesize', 10)
    is_show = res.get('is_show')

    Logging.logger.info('request_args:{0}'.format(res))
    try:
        page = int(page)
        pagesize = int(pagesize)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        page, pagesize = 1, 10

    try:
        is_show = int(is_show)
        if is_show not in [0, 1]:
            return jsonify(errno=-1, errmsg='is_show参数错误')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))

    try:
        if is_show == 0:
            articles = Article.query.filter(Article.is_show == is_show).order_by(
                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
        else:
            articles = Article.query.filter(Article.is_show == is_show).order_by(
                Article.zj_art_date.desc()).paginate(page, pagesize, False)

        count = articles.total
        article_list = list()
        for article in articles.items:
            article_dict = dict()
            article_dict['article_id'] = article.id
            article_dict['title'] = article.title
            article_dict['author'] = article.web_name
            if is_show == 0:
                article_dict['wechat_art_date'] = str(article.wechat_art_date)
            elif is_show == 1:
                stamp_time = get_time(str(article.zj_art_date))
                article_dict['wechat_art_date'] = stamp_time
                # 当前文章所属分类
                group_name_list = list()
                results = db.session.query(Group).join(ArticleGroup, ArticleGroup.article_id == article.id).filter(
                    ArticleGroup.group_id == Group.id).all()
                for group_obj in results:
                    group_name = group_obj.name
                    group_name_list.append(group_name)
                article_dict['group_name_list'] = group_name_list

            article_dict['summary'] = article.summary
            article_dict['min_pic'] = article.min_pic
            article_dict['is_big'] = article.is_big
            article_dict['is_read'] = article.is_read

            article_list.append(article_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=article_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章列表查询失败')


# 小程序--文章详情页
@api_article.route('/article_details', methods=['POST'])
# @auth_required
def article_details():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的文章的article_id')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg='参数错误,该文章不存在')

        docs = mongo_store.articles.find({'title': str(article.title)})
        doc = docs[0]
        article_dict = {}
        # for doc in docs:
        content = doc.get('content')
        div = doc.get('div', '')
        article_dict['title'] = article.title
        article_dict['author'] = article.web_name
        article_dict['min_pic'] = article.min_pic
        article_dict['wechat_art_date'] = str(article.wechat_art_date)
        article_dict['content'] = content
        article_dict['div'] = div
        article_dict['link'] = article.link
        article_dict['mp3_url'] = article.mp3_url
        article_dict['is_read'] = article.is_read
        article_dict['round_head_img'] = article.round_head_img
        article.read_num += 1
        db.session.add(article)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", data=article_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章详情查询失败')


# pc文章详情页
@api_article.route('/pc_article_details', methods=['POST'])
@login_required
@admin_required
def pc_article_details():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的文章的article_id')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg='参数错误,该文章不存在')

        # client = MongoClient('47.100.63.158', 27017)
        # my_db = client.wechat
        docs = mongo_store.articles.find({'title': article.title})
        doc = docs[0]
        article_dict = {}
        # for doc in docs:
        content = doc.get('content')
        div = doc.get('div', '')
        article_dict['title'] = article.title
        article_dict['author'] = article.web_name
        article_dict['min_pic'] = article.min_pic
        article_dict['wechat_art_date'] = str(article.wechat_art_date)
        article_dict['content'] = content
        article_dict['div'] = div
        article_dict['link'] = article.link
        article_dict['mp3_url'] = article.mp3_url
        article_dict['is_read'] = article.is_read
        article_dict['round_head_img'] = article.round_head_img
        return jsonify(errno=0, errmsg="OK", data=article_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章详情查询失败')


# PC文章上线到小程序
@api_article.route('/upload_article', methods=['POST'])
@login_required
@admin_required
def upload_article():
    try:
        res = request.get_json()
        article_id_list = res.get('article_id_list')
        group_id_list = res.get('group_id_list')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([article_id_list, group_id_list]):
            return jsonify(errno=-1, errmsg="参数不完整")

        for group_id in group_id_list:
            group_obj = Group.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该类别不存在")
            else:
                for article_id in article_id_list:
                    article = Article.query.get(article_id)
                    if not article:
                        return jsonify(errno=-1, errmsg="参数错误,该文章不存在", article_id=article_id)

                    result = ArticleGroup.query.filter(ArticleGroup.article_id == article_id,
                                                       ArticleGroup.group_id == group_id).first()
                    if result:
                        return jsonify(errno=-1, errmsg="参数错误,该文章已上线", article_id=article_id)
                    else:
                        # 当前分类下的所有文章
                        # articles = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).all()
                        # for article_obj in articles:
                        #     # 先更改文章的自定义排序数值
                        #     article_obj.sort_num += 1
                        #     db.session.add(article_obj)

                        obj = ArticleGroup()

                        article.is_show = 1
                        article.zj_art_date = datetime.datetime.now()

                        obj.article_id = article_id
                        obj.group_id = group_id
                        # 再给新上线的文章的自定义排序数值赋值,显示在最前
                        # obj.sort_num = 1
                        obj.admin_id = admin_id

                        # 记录小程序文章有更新,发送通知
                        records = UserBTN.query.filter(UserBTN.btn_num == 1).all()
                        for record in records:
                            record.is_new = 1
                            record.is_send = 0
                            db.session.add(record)

                        # 记录更新的时间
                        today = datetime.datetime.today().date()
                        up_obj = UpdateTime.query.filter(UpdateTime.type == 1).filter(
                            UpdateTime.create_time.like(str(today) + "%")).first()
                        if not up_obj:
                            time_obj = UpdateTime()
                            time_obj.type = 1
                            db.session.add(time_obj)

                        db.session.add(article)
                        db.session.add(obj)
                        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='上线失败')


# 上线文章分类列表
@api_article.route('/article_group', methods=['POST'])
# @auth_required
def article_group():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 7)
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入当前查询类型group_id")

        try:
            group_id = int(group_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg="参数错误,请传入int类型group_id")

        try:
            # if page == 1:
            #     page = 1
            # else:
            #     page = int(page - 1) * 10
            # pagesize = int(pagesize)
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 7

        group_obj = Group.query.get(group_id)
        if not group_obj:
            return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

        group_objs = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).order_by(
            ArticleGroup.create_time.desc()).paginate(page, pagesize, False)
        count = group_objs.total

        article_list = list()
        i = (page - 1) * pagesize + 1
        for obj in group_objs.items:
            # 根据文章id筛选文章
            article_dict = dict()
            article = Article.query.filter(Article.is_show == 1, Article.id == obj.article_id).first()
            article_dict['article_id'] = obj.article_id
            article_dict['title'] = article.title
            article_dict['author'] = article.web_name
            article_dict['min_pic'] = article.min_pic
            article_dict['is_big'] = article.is_big
            article_dict['is_read'] = article.is_read
            article_dict['mp3_url'] = article.mp3_url
            article_dict['group_name'] = group_obj.name
            read_num = article.read_num
            if not read_num:
                read_num = random.randint(1000, 12000)
                article_dict['read_num'] = read_num
                article.read_num = read_num
                db.session.add(article)
                db.session.commit()
            else:
                article_dict['read_num'] = read_num

            article_dict['sort_num'] = i
            i += 1

            stamp_time = get_time(str(article.zj_art_date))
            article_dict['zj_art_date'] = stamp_time

            article_list.append(article_dict)
        return jsonify(errno=0, errmsg="OK", count=count, data=article_list)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章列表查询失败')


# pc上线文章分类列表
@api_article.route('/pc_article_group', methods=['POST'])
@login_required
@admin_required
def pc_article_group():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入当前查询类型group_id")

        try:
            group_id = int(group_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg="参数错误,请传入int类型group_id")

        try:
            pagesize = int(pagesize)
        except Exception as e:
            pagesize = 10

        group_obj = Group.query.get(group_id)
        if not group_obj:
            return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

        try:
            page = int(page)
        except Exception as e:
            page = 1

        group_objs = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).order_by(
            ArticleGroup.create_time.desc()).paginate(page, pagesize, False)
        count = group_objs.total

        article_list = list()
        i = (page - 1) * pagesize + 1
        for obj in group_objs.items:
            article = Article.query.filter(Article.is_show == 1, Article.id == obj.article_id).first()
            article_dict = dict()
            article_dict['article_id'] = obj.article_id
            article_dict['title'] = article.title
            article_dict['author'] = article.web_name
            article_dict['min_pic'] = article.min_pic
            article_dict['is_big'] = article.is_big
            article_dict['is_read'] = article.is_read
            article_dict['mp3_url'] = article.mp3_url
            article_dict['group_name'] = group_obj.name
            article_dict['sort_num'] = i
            i += 1

            stamp_time = get_time(str(article.zj_art_date))
            article_dict['zj_art_date'] = stamp_time

            article_list.append(article_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=article_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章列表查询失败')


# PC上线文章标题分类列表
@api_article.route('/pc_article_title', methods=['POST'])
# @login_required
# @admin_required
def pc_article_title():
    try:
        res = request.get_json()
        group_id = res.get('group_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 100)

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入当前查询类型group_id")

        try:
            group_id = int(group_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg="参数错误,请传入int类型group_id")

        article_list = list()

        # group_objs = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).order_by(
        #     ArticleGroup.create_time.desc()).paginate(page, pagesize, False)
        #
        # for obj in group_objs.items:
        #     article = Article.query.filter(Article.is_show == 1, Article.id == obj.article_id).first()
        #     article_dict = dict()
        #     article_dict['article_id'] = obj.article_id
        #     article_dict['title'] = article.title
        #     article_list.append(article_dict)

        results = db.session.query(Article).join(ArticleGroup, ArticleGroup.article_id == Article.id).filter(
            ArticleGroup.group_id == group_id, Article.is_show == 1).order_by(
            ArticleGroup.create_time.desc()).paginate(page, pagesize, False)

        for obj in results.items:
            article_dict = dict()
            article_dict['article_id'] = obj.id
            article_dict['title'] = obj.title
            article_list.append(article_dict)

        return jsonify(errno=0, errmsg="OK", data=article_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章列表查询失败')


# pc根据标题模糊搜索未上线文章(爆料库搜索功能)
@api_article.route('/article_search', methods=['POST'])
@login_required
@admin_required
def article_search():
    try:
        res = request.get_json()
        words = res.get('words')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        web_name = res.get('web_name')
        start_time = res.get('start_time')
        end_time = res.get('end_time')
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if group_id:
            # 传入group_id
            # 直接在当前类型下搜索
            all_results = Article.query.filter(Article.is_show == 1).order_by(Article.zj_art_date.desc()).paginate(page,
                                                                                                                   pagesize,
                                                                                                                   False)
            article_list = []
            for article in all_results.items:
                article_dict = dict()
                article_dict['article_id'] = article.id
                article_dict['title'] = article.title
                article_list.append(article_dict)
            return jsonify(errno=0, errmsg="OK", data=article_list)
        else:
            # 筛选
            # 传入web_name
            if web_name:
                print(('传入来源:', web_name))
                # 有开始时间
                if start_time:
                    print(('传入开始时间:', start_time))
                    try:
                        if ":" in start_time:
                            time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(start_time, "%Y-%m-%d")

                    except:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                    # 有关键字
                    if words:
                        print(('传入关键字:', words))
                        # 有结束时间
                        if end_time:
                            print(('传入结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")
                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.wechat_art_date <= end_time,
                                                               Article.web_name == web_name).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.web_name == web_name).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                    # 无关键字
                    else:
                        print('无关键字')
                        # 有结束时间
                        if end_time:
                            print(('传入结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")
                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.wechat_art_date <= end_time,
                                                               Article.web_name == web_name).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.web_name == web_name).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                # 无开始时间
                else:
                    print('无开始时间')
                    # 有关键字
                    if words:
                        print(('传入关键字:', words))
                        # 有结束时间
                        if end_time:
                            print(('传入结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")
                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date <= end_time,
                                                               Article.web_name == web_name).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.web_name == web_name).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                    # 无关键字
                    else:
                        print('无关键字')
                        # 有结束时间
                        if end_time:
                            print(('传入结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")
                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date <= end_time,
                                                               Article.web_name == web_name).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.web_name == web_name).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
            # 无web_name
            else:
                print('无文章来源')
                # 有筛选的开始时间
                if start_time:
                    print(('传入开始时间:', start_time))
                    try:
                        if ":" in start_time:
                            time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(start_time, "%Y-%m-%d")

                    except:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                    # 有关键字
                    if words:
                        print(('传入关键字:', words))
                        # 有结束时间
                        if end_time:
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")

                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.wechat_art_date <= end_time).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                            print(('传入结束时间:', end_time))
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                    # 无关键字
                    else:
                        print('无关键字')
                        # 有结束时间
                        if end_time:
                            print(('传入结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")

                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time,
                                                               Article.wechat_art_date <= end_time).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date >= start_time).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                # 无筛选的开始时间
                else:
                    print('无开始时间')
                    # 有关键字
                    if words:
                        print(('有关键字:', words))
                        # 有结束时间
                        if end_time:
                            print(('有结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")

                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date <= end_time).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间')
                            all_results = Article.query.filter(Article.is_show == 0).filter(
                                Article.title.like("%" + words + "%")).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)

                    # 无关键字
                    else:
                        print('无关键字')
                        # 有结束时间
                        if end_time:
                            print(('有结束时间:', end_time))
                            try:
                                if ":" in end_time:
                                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                                else:
                                    time.strptime(end_time, "%Y-%m-%d")

                            except:
                                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                            all_results = Article.query.filter(Article.is_show == 0,
                                                               Article.wechat_art_date <= end_time).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)
                        # 无结束时间
                        else:
                            print('无结束时间,搜全部')
                            all_results = Article.query.filter(Article.is_show == 0).order_by(
                                Article.wechat_art_date.desc()).paginate(page, pagesize, False)

            # all_results = all_results[(page - 1) * pagesize:page * pagesize]
            article_list = list()
            for article in all_results.items:
                article_dict = dict()
                article_dict['article_id'] = article.id
                article_dict['mp3_url'] = article.mp3_url
                article_dict['is_read'] = article.is_read
                article_dict['title'] = article.title
                article_dict['author'] = article.web_name
                article_dict['summary'] = article.summary
                article_dict['min_pic'] = article.min_pic
                article_dict['is_big'] = article.is_big
                article_dict['wechat_art_date'] = str(article.wechat_art_date)

                article_list.append(article_dict)

            article_count = all_results.total
            return jsonify(errno=0, errmsg="OK", count=article_count, data=article_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章搜索失败')


# pc根据标题模糊搜索上线文章(爆料列表搜索功能)
@api_article.route('/online_article_search', methods=['POST'])
@login_required
@admin_required
def online_article_search():
    try:
        res = request.get_json()
        words = res.get('words')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if words:
            all_results = Article.query.filter(Article.is_show == 1).filter(
                Article.title.like("%" + words + "%")).order_by(
                Article.zj_art_date.desc()).paginate(page, pagesize, False)
        else:
            all_results = Article.query.filter(Article.is_show == 1).order_by(
                Article.zj_art_date.desc()).paginate(page, pagesize, False)

        article_count = all_results.total
        article_list = list()
        for article in all_results.items:
            article_dict = dict()
            article_dict['article_id'] = article.id
            article_dict['mp3_url'] = article.mp3_url
            article_dict['is_read'] = article.is_read
            article_dict['title'] = article.title
            article_dict['author'] = article.web_name
            article_dict['summary'] = article.summary
            article_dict['min_pic'] = article.min_pic
            article_dict['is_big'] = article.is_big
            article_dict['wechat_art_date'] = str(article.zj_art_date)

            # 当前文章所属分类
            group_name_list = list()
            # article_groups = ArticleGroup.query.filter(ArticleGroup.article_id == article.id).all()
            # for article_group_obj in article_groups:
            #     group_id = article_group_obj.group_id
            #     group_obj = Group.query.get(group_id)
            #     group_name = group_obj.name
            #     group_name_list.append(group_name)
            # article_dict['group_name_list'] = group_name_list
            results = db.session.query(Group).join(ArticleGroup, ArticleGroup.article_id == article.id).filter(
                ArticleGroup.group_id == Group.id).all()
            for group_obj in results:
                group_name = group_obj.name
                group_name_list.append(group_name)
            article_dict['group_name_list'] = group_name_list
            article_list.append(article_dict)

        return jsonify(errno=0, errmsg="OK", count=article_count, data=article_list)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章搜索失败')


# pc下线文章
@api_article.route('/down_line', methods=['POST'])
@login_required
@admin_required
def down_line():
    try:
        res = request.get_json()
        article_id_list = res.get('article_id_list')
        group_id = res.get('group_id')
        # admin_id = g.user_id
        admin_id = 1

        now = datetime.datetime.now()
        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id_list:
            return jsonify(errno=-1, errmsg="参数错误,请传入下线文章的article_id")

        if group_id:
            # 传group_id
            # 下线当前文章所在的当前类型
            group_obj = Group.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该分类不存在")

            for article_id in article_id_list:
                article = Article.query.get(article_id)
                if not article:
                    return jsonify(errno=-1, errmsg="参数错误,该文章不存在", article_id=article_id)

                if article.is_show != 1:
                    return jsonify(errno=-1, errmsg="参数错误,该文章未上线", article_id=article_id)

                obj = ArticleGroup.query.filter(ArticleGroup.group_id == group_id,
                                                ArticleGroup.article_id == article_id).first()
                if not obj:
                    return jsonify(errno=-1, errmsg="该文章已上线，但不在该分类", article_id=article_id)

                # articles = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).all()
                # for art in articles:
                #     if art.sort_num > obj.sort_num:
                #         art.sort_num -= 1
                #         db.session.add(art)
                # db.session.commit()

                db.session.delete(obj)
                group = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
                num = len(group)
                if num == 0:
                    # db.session.delete(obj)
                    article.is_show = 0
                    article.zj_art_date = now
                    article.admin_id = admin_id
                    db.session.add(article)
                    Logging.logger.info("文章:{0} 在 {1} 被admin= {2} 全部下线成功".format(article.title, now, admin_id))

        else:
            # 不传group_id 下线当前文章所在的全部类型
            for article_id in article_id_list:
                article = Article.query.get(article_id)
                if not article:
                    return jsonify(errno=-1, errmsg="参数错误,该文章不存在", article_id=article_id)

                if article.is_show != 1:
                    return jsonify(errno=-1, errmsg="参数错误,该文章未上线", article_id=article_id)

                objs = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
                for obj in objs:
                    # 修改当前类型下所属文章的sort_num
                    # articles = ArticleGroup.query.filter(ArticleGroup.group_id == obj.group_id).all()
                    # for art in articles:
                    #     if art.sort_num > obj.sort_num:
                    #         art.sort_num -= 1
                    #         db.session.add(art)

                    db.session.delete(obj)
                article.is_show = 0
                article.zj_art_date = now
                article.admin_id = admin_id
                db.session.add(article)
                Logging.logger.info("文章:{0} 在 {1} 被admin= {2} 全部下线成功".format(article.title, now, admin_id))

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='下线文章失败')


# pc设置/修改文章主图
@api_article.route('/min_pic', methods=['POST'])
@login_required
@admin_required
def min_pic():
    try:
        res = request.get_json()
        article_id = res.get('article_id')
        img = res.get('img')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入设置或修改文章的article_id")

        article_obj = Article.query.get(article_id)
        if not article_obj:
            return jsonify(errno=-1, errmsg="参数错误,该文章不存在")

        if not img:
            img = article_obj.min_pic
        res = re.match(r'^https://cdn.max-digital.cn/.*', img)
        # res = re.match(r'^http://maxpr.oss-cn-shanghai.aliyuncs.com/.*', img)
        if not res:
            return jsonify(errno=-1, errmsg='参数错误,请传入正确的图片url')

        article_obj.min_pic = img
        article_obj.admin_id = admin_id
        try:
            db.session.add(article_obj)
            db.session.commit()
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            db.session.rollback()
            return jsonify(errno=-1, errmsg='网络异常')

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
    return jsonify(errno=-1, errmsg='设置/修改文章主图失败')


# pc获取当前文章内的所有图片
@api_article.route('/get_pics', methods=['POST'])
@login_required
@admin_required
def get_pics():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        if not article_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入当前文章的article_id")

        article_obj = Article.query.get(article_id)
        if not article_obj:
            return jsonify(errno=-1, errmsg="参数错误,该文章不存在")

        try:
            client = MongoClient('47.100.63.158', 27017)
            my_db = client.wechat
            docs = my_db.articles.find({'title': article_obj.title, 'name': article_obj.author})
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='网络异常')

        pic_list = []
        for doc in docs:
            article_dict = {}
            content = doc.get('content')
            # article_dict['title'] = article_obj.title
            # article_dict['author'] = article_obj.author
            # article_dict['wechat_art_date'] = str(article_obj.wechat_art_date)
            for item in content:
                if item.get('img'):
                    img = item.get('img')
                    img = img.replace('http', 'https')
                    pic_list.append(img)

        return jsonify(errno=0, errmsg="OK", data=pic_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
    return jsonify(errno=-1, errmsg='获取文章图片失败')


# pc爆料库删除文章
@api_article.route('/del_article', methods=['POST'])
@login_required
@admin_required
def del_article():
    res = request.get_json()
    article_id_list = res.get('article_id_list')

    Logging.logger.info('request_args:{0}'.format(res))
    try:
        for article_id in article_id_list:
            if not article_id:
                return jsonify(errno=-1, errmsg="参数错误,请传入删除文章的article_id")

            obj = Article.query.get(article_id)
            if not obj:
                return jsonify(errno=-1, errmsg="参数错误,该文章不存在")

            db.session.delete(obj)

            article_objs = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
            for article_obj in article_objs:
                db.session.delete(article_obj)

            banner_obj = Banner.query.filter(Banner.article_id == article_id).all()
            for banner in banner_obj:
                banner.article_id = None
                db.session.add(banner)

            tops = Top.query.filter(Top.article_id == article_id).all()
            for top in tops:
                top.article_id = None
                db.session.add(top)

            my_query = {"article_id": obj.id}
            mongo_store.articles.delete_one(my_query)

            db.session.commit()
            Logging.logger.info("文章:{0},删除成功".format(obj.title))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc设置文章是否突出显示
@api_article.route('/show_big', methods=['POST'])
@login_required
@admin_required
def show_big():
    try:
        res = request.get_json()
        article_id = res.get('article_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg="参数错误,请设置传入文章的article_id")
        else:
            obj = Article.query.get(article_id)
            if obj:
                if obj.is_big == 0:
                    obj.is_big = 1
                else:
                    obj.is_big = 0
                obj.admin_id = admin_id
                db.session.add(obj)
                db.session.commit()
            else:
                return jsonify(errno=-1, errmsg="参数错误,该文章不存在")
        return jsonify(errno=0, errmsg="OK")

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# pc通过微信公众号文章链接,爬虫直接获取文章
@api_article.route('/wechat_url', methods=['POST'])
@login_required
@admin_required
def wechat_url():
    try:
        res = request.get_json()
        url = res.get('url')
        admin_id = g.user_id
        # admin_id = 6

        Logging.logger.info('request_args:{0}'.format(res))
        if url:
            res = re.match(r'^https://mp.weixin.qq.com/s/.*', url)
            if res:
                try:
                    wechat = wechat_url_spider()
                    # wechat = WechatUrlSpider()
                    res = wechat.start(url, admin_id)
                    if res == -1:
                        return jsonify(errno=-1, errmsg="文章已存在")
                    elif res == 1:
                        return jsonify(errno=-1, errmsg="该文章资源不存在")
                    elif res == 2:
                        return jsonify(errno=-1, errmsg="已存在相似度大于0.6的文章")

                    return jsonify(errno=0, errmsg="OK")
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))
                    return jsonify(errno=-1, errmsg='获取文章失败')

            else:
                return jsonify(errno=-1, errmsg='参数错误,请传入正确的微信文章的url')

        else:
            return jsonify(errno=-1, errmsg='参数错误,请传入请求的微信文章的url')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# pc爆料列表设置
# 点击设置,显示当前文章所在分类
@api_article.route('/current_group', methods=['POST'])
@login_required
@admin_required
def current_group():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入设置的文章article_id")

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg="参数错误,该文章不存在")

        group_obj_ls = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
        group_ls = list()
        for group_obj in group_obj_ls:
            group_dict = dict()
            group_id = group_obj.group_id
            group_dict['group_id'] = group_id
            obj = Group.query.get(group_id)
            group_dict['group_name'] = obj.name
            group_ls.append(group_dict)
        return jsonify(errno=0, errmsg="OK", data=group_ls)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='显示当前文章所在分类失败')


# pc爆料列表设置
# 设置自定义顺序及修改上线类型
@api_article.route('/set_article', methods=['POST'])
@login_required
@admin_required
def set_article():
    try:
        res = request.get_json()
        article_id = res.get('article_id')
        group_id_list = res.get('group_id_list')
        # sort_num = res.get('sort_num', 1)

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg="参数错误,请传入设置文章的article_id")

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg="参数错误,该文章不存在")
        article_obj = Article.query.filter(Article.is_show == 1, Article.id == article_id).first()
        if not article_obj:
            return jsonify(errno=-1, errmsg="参数错误,该文章未上线")

        if group_id_list:
            # 修改当前文章所属类型
            try:
                objs = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
                obj_id_list = list()
                # 删除文章所属类型修改后,对比修改前不存在的类型
                for obj in objs:
                    if obj.group_id not in group_id_list:
                        # 修改该类型下所有文章的sort_num
                        # articles = ArticleGroup.query.filter(ArticleGroup.group_id == obj.group_id).all()
                        # for art in articles:
                        #     if art.sort_num > obj.sort_num:
                        #         art.sort_num -= 1
                        #         db.session.add(art)
                        db.session.delete(obj)
                    else:
                        obj_id_list.append(obj.group_id)

                # 判断当前文章是否有新的分类
                for group_id in group_id_list:
                    if group_id not in obj_id_list:
                        # 文章有新的类型
                        group_obj = Group.query.get(group_id)
                        if group_obj:
                            try:
                                article_group = ArticleGroup()
                                article_group.article_id = article_id
                                article_group.group_id = group_id

                                db.session.add(article)
                                db.session.add(article_group)
                                db.session.commit()
                            except Exception as e:
                                Logging.logger.error('errmsg:{0}'.format(e))
                                db.session.rollback()
                                return jsonify(errno=-1, errmsg='网络异常')
                        else:
                            return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg="修改上线类型失败")

        # if sort_num:
        #     # 自定义当前文章的排序
        #     try:
        #         sort_num = int(sort_num)
        #     except Exception as e:
        #         Logging.logger.error('errmsg:{0}'.format(e))
        #         return jsonify(errno=-1, errmsg="sort_num参数错误")
        #
        #     try:
        #         # 当前文章所属的分类对象
        #         group_list = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
        #         for group in group_list:
        #             group_id = group.group_id
        #             article_obj = ArticleGroup.query.filter(ArticleGroup.article_id == article_id,
        #                                                     ArticleGroup.group_id == group_id).first()
        #             # 当前分类下所有的文章对象
        #             articles = ArticleGroup.query.filter(ArticleGroup.group_id == group_id).all()
        #             total_num = len(articles)
        #             if sort_num > total_num:
        #                 return jsonify(errno=-1, errmsg='参数错误,传入的sort_num值超出范围')
        #
        #             for art in articles:
        #                 # 文章往前调 10-->1
        #                 if article_obj.sort_num > sort_num:
        #                     # 选取修改范围
        #                     if sort_num <= art.sort_num < article_obj.sort_num:
        #                         # 先加再赋值
        #                         art.sort_num += 1
        #                         db.session.add(art)
        #                         db.session.commit()
        #
        #                 # 文章往后调 1-->10
        #                 elif article_obj.sort_num < sort_num:
        #                     # 选取修改范围
        #                     if article_obj.sort_num < art.sort_num <= sort_num:
        #                         # 先减再赋值
        #                         art.sort_num -= 1
        #                         db.session.add(art)
        #                         db.session.commit()
        #
        #                 else:
        #                     # 文章位置不变
        #                     article_obj.sort_num = sort_num
        #             # 赋值
        #             article_obj.sort_num = sort_num
        #             db.session.add(article_obj)
        #             db.session.commit()
        #     except Exception as e:
        #         Logging.logger.error('errmsg:{0}'.format(e))
        #         db.session.rollback()
        #         return jsonify(errno=-1, errmsg="修改自定义排序失败")

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='设置失败')


# pc爆料库或爆料列表显示所有的文章来源
@api_article.route('/article_source', methods=['POST'])
@login_required
@admin_required
def article_source():
    try:
        res = request.get_json()
        is_show = res.get('is_show')

        try:
            is_show = int(is_show)
            if is_show not in [0, 1]:
                return jsonify(errno=-1, errmsg='is_show参数错误,请传入0或1')
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))

        # all_results = Article.query.filter_by(is_show=is_show).all()

        # article_source_list = list()
        # for article in all_results:
        #     article_source_list.append(article.web_name)  # 来源
        #
        # article_source_list = list(set(article_source_list))  # 去重
        # source_count = len(article_source_list)

        article_source_list = db.session.query(Article.web_name).filter(Article.is_show == is_show).distinct().all()
        article_source_list = [x[0] for x in article_source_list]

        return jsonify(errno=0, errmsg="OK", data=article_source_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询失败')


# 接受神箭手微信文章数据
@api_article.route('/get_data', methods=['POST'])
def get_data():
    try:
        ret = request.form
        sign = ret.get('__sign')
        Logging.logger.info('sign:{0}'.format(sign))
        secret_key = KeysConfig.get_shenjianshou_secret_key()
        Logging.logger.info('secret_key:{0}'.format(secret_key))

        if sign != secret_key:
            return jsonify(result=2, data='发布失败')
        else:
            link = ret.get('__crawlUrl')
            title = ret.get('article_title')
            summary = ret.get('article_brief')
            author = ret.get('article_author')
            min_pic = ret.get('article_thumbnail')
            is_original = ret.get('is_original')
            if is_original == "是":
                is_original = 1
            else:
                is_original = 0
            wechat_art_date = int(ret.get('article_publish_time'))
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wechat_art_date))
            web_name = ret.get('weixin_nickname')
            alias = ret.get('weixin_name')
            round_head_img = ret.get('weixin_avatar')
            article_images = ret.get('article_images')

            table = ret.get('article_content')
            data1 = table.replace(
                '<br style="max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;"/>', '')
            data1 = data1.replace('<br/>', '')
            div = data1.replace('!important', '')
            content = ret.get('content')
            content = json.loads(content)
            Logging.logger.info('接收到文章:{0}'.format(title))

            if not content:
                Logging.logger.info('抓取到的文章内容是空,标题是:{0}'.format(title))
                return jsonify(result=1, data='发布成功')

            # 调小程序接口敏感词过滤,图片过滤,
            # 本地敏感关键词过滤
            article_filter_obj = ArticleFilter(title, content)
            resp = article_filter_obj.sensitive_words_filter()
            if resp:
                Logging.logger.info('抓取到的文章中含有敏感词,标题是:{0}'.format(title))
                return jsonify(result=1, data='发布成功')

            # 相似度去重
            # sim_ls = ArticleModel().run(content)
            # Logging.logger.info('对比文章相似度的结果:{0}'.format(sim_ls))
            # if sim_ls:
            #     redis_client = RedisClient.create_redis_cli()
            #     sim_article_ids = [redis_client.lindex('article_id_list', item[0]) for item in sim_ls]
            #     Logging.logger.info('已存在相似度大于0.6的文章,相似文章ID:{0}'.format(sim_article_ids))
            # else:
            obj = Upload()
            num = obj.get_title_list(title)
            if num != 0:
                Logging.logger.info('文章已存在mysql中,标题是:{0}'.format(title))
                return jsonify(result=1, data='发布成功')
            else:
                # # 公众号自动分类上传mysql
                # result = obj.upload_mysql_by_webname(title, author, date, min_pic, summary, web_name, link,
                #                                      round_head_img, alias, is_original)
                # 关键词自动分类上传mysql
                Logging.logger.info('准备分类')
                # article_filter_obj = ArticleFilter(title, content)
                group_id_list = article_filter_obj.article_filter()
                Logging.logger.info('获取到文章预分类ID:{0}'.format(group_id_list))
                result = obj.upload_mysql_by_keyword(title, author, date, min_pic, summary, web_name, link,
                                                     round_head_img, alias, is_original, group_id_list)
                Logging.logger.info('自动分类完成')
                if isinstance(result, list):
                    # print result
                    # mysql上传成功再传MongoDB
                    article_dict = dict()
                    article_dict['article_id'] = result[0]
                    article_dict['min_pic'] = min_pic
                    article_dict['title'] = title
                    article_dict['summary'] = summary
                    article_dict['date'] = date
                    article_dict['content'] = content
                    article_dict['name'] = author
                    article_dict['web_name'] = web_name
                    article_dict['url'] = link
                    article_dict['div'] = div
                    article_dict['round_head_img'] = round_head_img
                    article_dict['alias'] = alias
                    obj.upload_mongo(article_dict, title)
                    # 上传es
                    # es_store.index(index="wechat_article", doc_type="article", body=article_dict)
                    # if len(result) == 2:
                    #     # 生成音频
                    #     get_audio_baidu.delay(result[0], content)

                else:
                    return jsonify(result=2, data='发布失败')

            return jsonify(result=1, data='发布成功')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(result=2, data='发布失败')


# 接收神箭手知乎问答数据
@api_article.route('/get_data_zhihu', methods=['POST'])
def get_data_zhihu():
    try:
        ret = request.form
        sign = ret.get('__sign')
        secret_key = KeysConfig.get_shenjianshou_secret_key()
        if sign != secret_key:
            # print '接收到数据:', ret
            link = ret.get('__crawlUrl')
            question_title = ret.get('question_title')
            question_detail = ret.get('question_detail')
            question_topics = ret.get('question_topics')
            question_publish_time = ret.get('question_publish_time')
            question_update_time = ret.get('question_update_time')
            question_author = ret.get('question_author')
            question_author_avatar = ret.get('question_author_avatar')
            question_visit_count = ret.get('question_visit_count')
            question_follower_count = ret.get('question_follower_count')
            keyword = ret.get('keyword')
            question_answer = ret.get('question_answer')

            question_publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(question_publish_time)))
            question_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(question_update_time)))
            question_answer = json.loads(question_answer)
            for answer in question_answer:
                question_answer_publish_time = answer.get('question_answer_publish_time')
                if question_answer_publish_time:
                    answer['question_answer_publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                        int(question_answer_publish_time)))

            obj = ZhiHuData()
            obj.link = link
            obj.title = question_title
            obj.content = question_detail
            obj.theme = question_topics
            obj.publish_time = question_publish_time
            obj.updated_time = question_update_time
            obj.author = question_author
            obj.img = question_author_avatar
            obj.view_num = question_visit_count
            obj.attention_num = question_follower_count
            obj.keywords = keyword
            # obj.answer = question_answer

            db.session.add(obj)
            db.session.commit()
            print('上传到mysql成功')

            client = MongoClient('47.100.63.158', 27017)
            question_data = dict()
            question_data['link'] = link
            question_data['question_title'] = question_title
            question_data['question_detail'] = question_detail
            question_topics = json.loads(question_topics)
            question_data['question_topics'] = question_topics
            question_data['question_publish_time'] = question_publish_time
            question_data['question_update_time'] = question_update_time
            question_data['question_author'] = question_author
            question_data['question_author_avatar'] = question_author_avatar
            question_data['question_visit_count'] = question_visit_count
            question_data['question_follower_count'] = question_follower_count
            question_data['keyword'] = keyword
            question_data['question_answer'] = question_answer

            # my_db = client.will
            my_db = client.zhihu
            my_db.questions.insert_one(question_data)
            print('上传到mongo成功')

            return jsonify(result=1, data='发布成功')
        else:
            return jsonify(result=2, data='发布失败')
    except Exception as e:
        Logging.logger.error('[api/get_data_zhihu] errmsg:{0}'.format(e))
        return jsonify(result=2, data='发布失败')


# PC根据文章发布日期清理数据库文章(暂无)
@api_article.route('/clear_articles', methods=['POST'])
def clear_articles():
    try:
        res = request.get_json()
        start_date = res.get('start_date')
        end_date = res.get('end_date')
        is_show = res.get('is_show', 0)

        Logging.logger.info('request_args:{0}'.format(res))

        results = Article.query.filter(Article.is_show == is_show,
                                       Article.wechat_art_date >= start_date,
                                       Article.wechat_art_date <= end_date).all()
        count = len(results)
        if is_show == 0:
            for result in results:
                Logging.logger.info('article_id:{0}'.format(result.id))
                mongo_store.articles.delete_one({'article_id': '%s' % result.id})
                db.session.delete(result)

        elif is_show == 1:
            for result in results:
                article_id = result.id
                groups = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
                for group in groups:
                    db.session.delete(group)

                banners = Banner.query.filter(Banner.article_id == article_id).all()
                for banner in banners:
                    banner.article_id = None
                    db.session.add(banner)

                tops = Top.query.filter(Top.article_id == article_id).all()
                for top in tops:
                    top.article_id = None
                    db.session.add(top)

                mongo_store.articles.delete_one({'article_id': '%s' % article_id})
                db.session.delete(result)
        db.session.commit()
        Logging.logger.info("成功清理了%s篇文章" % count)
        return jsonify(errno=0, errmsg="成功清理了%s篇文章" % count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(result=-1, data='网络异常')


# 根据日期下线文章
@api_article.route('/down_article_by_date', methods=['POST'])
def down_article_by_date():
    try:
        res = request.get_json()
        start_date = res.get('start_date')
        end_date = res.get('end_date')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([start_date, end_date]):
            return jsonify(errno=-1, errmsg="参数不完整")

        results = Article.query.filter(Article.is_show == 1, Article.zj_art_date <= end_date,
                                       Article.zj_art_date >= start_date).all()
        count = len(results)
        id_ls = list()
        for result in results:
            article_id = result.id
            id_ls.append(article_id)
            objs = ArticleGroup.query.filter(ArticleGroup.article_id == article_id).all()
            for obj in objs:
                db.session.delete(obj)

            now = datetime.datetime.now()
            article = Article.query.get(article_id)
            article.is_show = 0
            article.zj_art_date = now
            db.session.add(article)

        db.session.commit()
        print(("成功下线了%s篇文章" % count))
        return jsonify(errno=0, errmsg="OK", id_ls=id_ls, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='下线文章失败')


# 爆料列表搜索功能--连表查询
@api_article.route('/article_search_search', methods=['POST'])
@login_required
@admin_required
def article_search_search():
    try:
        res = request.get_json()
        words = res.get('words')
        group_id = res.get('group_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page = 1

        try:
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            pagesize = 10

        if words:
            new_results = db.session.query(Article).join(ArticleGroup, ArticleGroup.article_id == Article.id).filter(
                ArticleGroup.group_id == group_id).filter(Article.title.like("%" + words + "%")).order_by(
                Article.zj_art_date.desc()).all()
        else:
            new_results = db.session.query(Article).join(ArticleGroup, ArticleGroup.article_id == Article.id).filter(
                ArticleGroup.group_id == group_id).order_by(
                Article.zj_art_date.desc()).all()

        article_count = len(new_results)
        new_results = new_results[(page - 1) * pagesize:page * pagesize]
        article_list = list()
        for article in new_results:
            article_dict = dict()
            article_dict['article_id'] = article.id
            article_dict['mp3_url'] = article.mp3_url
            article_dict['is_read'] = article.is_read
            article_dict['title'] = article.title
            article_dict['author'] = article.web_name
            article_dict['summary'] = article.summary
            article_dict['min_pic'] = article.min_pic
            article_dict['is_big'] = article.is_big
            article_dict['zj_art_date'] = str(article.zj_art_date)

            article_list.append(article_dict)

        return jsonify(errno=0, errmsg="OK", count=article_count, data=article_list)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章搜索失败')


# es文章详情页
@api_article.route('/es_article_details', methods=['POST'])
def es_article_details():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的文章的article_id')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg='参数错误,该文章不存在')

        article_dict = {}
        body = {
            "query": {
                "match": {
                    "article_id": article_id
                }
            }
        }
        res = es_store.search(index="wechat_article", doc_type="article", body=body)
        for doc in res['hits']['hits']:
            score = doc.get('_score')
            article_dict['score'] = score

            source = doc.get('_source')
            print(source)
            article_dict['content'] = source.get('content')

        article_dict['title'] = article.title
        article_dict['author'] = article.web_name
        article_dict['min_pic'] = article.min_pic
        article_dict['wechat_art_date'] = str(article.wechat_art_date)
        article_dict['link'] = article.link
        article_dict['mp3_url'] = article.mp3_url
        article_dict['is_read'] = article.is_read
        article_dict['round_head_img'] = article.round_head_img
        return jsonify(errno=0, errmsg="OK", data=article_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章详情查询失败')
