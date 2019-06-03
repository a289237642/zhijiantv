# -*- coding:utf-8 -*-
# author: will
import datetime
import random

from flask import request, jsonify, g

from app import db, mongo_store
from app.models import NewsGroup, NewsGroupInfo, NewsData
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required, auth_required
from . import api_news


# PC--更新快讯类型
@api_news.route('/news_update_group', methods=['POST'])
@login_required
@admin_required
def news_update_group():
    try:
        res = request.get_json()
        news_group_name = res.get('news_group_name')
        group_id = res.get('group_id')
        sort_num = res.get('sort_num', 1)

        Logging.logger.info('request_args:{0}'.format(res))
        if group_id:
            # 修改
            try:
                group_id = int(group_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg='参数错误,请传入int类型的group_id')

            obj = NewsGroup.query.get(group_id)
            if not obj:
                return jsonify(errno=-1, errmsg='参数错误,该分类不存在')

            if news_group_name:
                obj.name = news_group_name

            if sort_num:
                # 自定义排序
                try:
                    sort_num = int(sort_num)
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                groups = NewsGroup.query.all()
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
                        # 快讯位置不变
                        obj.sort_num = sort_num
                # 赋值
                obj.sort_num = sort_num
                db.session.add(obj)

        else:
            # 新增
            if not news_group_name:
                return jsonify(errno=-1, errmsg='请传入新增的类别名')

            groups = NewsGroup.query.all()
            if not sort_num:
                count = len(groups)
                obj = NewsGroup()
                obj.name = news_group_name
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

                obj = NewsGroup()
                obj.name = news_group_name
                obj.sort_num = sort_num
                db.session.add(obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC快讯类型状态切换
@api_news.route('/news_chmod', methods=['POST'])
# @login_required
# @admin_required
def news_chmod():
    try:
        res = request.get_json()
        group_id = res.get('group_id')
        try:
            group_id = int(group_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误,请传入int类型的group_id')

        obj = NewsGroup.query.get(group_id)
        if not obj:
            return jsonify(errno=-1, errmsg='参数错误,该分类不存在')

        if obj.is_show == 0:
            obj.is_show = 1
        else:
            obj.is_show = 0

        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC快讯类型删除
@api_news.route('/del_news_groups', methods=['POST'])
@login_required
@admin_required
def del_news_groups():
    try:
        res = request.get_json()
        news_id_list = res.get('news_id_list')

        Logging.logger.info('request_args:{0}'.format(res))
        for news_id in news_id_list:
            if not news_id:
                return jsonify(errno=-1, errmsg="参数错误,请传入删除快讯的news_id")

            obj = NewsData.query.get(news_id)
            if not obj:
                return jsonify(errno=-1, errmsg="参数错误,该快讯不存在")

            db.session.delete(obj)

            news_objs = NewsGroupInfo.query.filter(NewsGroupInfo.news_id == news_id).all()
            for news_obj in news_objs:
                db.session.delete(news_obj)

            db.session.commit()
            Logging.logger.info("快讯:{0},删除成功".format(obj.title))
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC快讯库和已上线全部列表
@api_news.route('/pc_news', methods=['POST'])
@login_required
@admin_required
def pc_news():
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
            results = NewsData.query.filter(NewsData.is_show == is_show).order_by(
                NewsData.publish_time.desc()).all()
        else:
            results = NewsData.query.filter(NewsData.is_show == is_show).order_by(
                NewsData.zj_art_date.desc()).all()

        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]

        news_list = list()
        for news in results:
            news_dict = {}

            news_dict['news_id'] = news.id
            news_dict['title'] = news.title
            news_dict['web_name'] = news.web_name
            news_dict['audio_url'] = news.audio_url
            news_dict['listen_num'] = news.listen_num
            news_dict['base_url'] = news.base_url
            news_dict['is_read'] = news.is_read

            if is_show == 0:
                news_dict['publish_time'] = str(news.publish_time)
            elif is_show == 1:
                # stamp_time = get_time(str(news.zj_art_date))  # 计算为几小时前
                news_dict['publish_time'] = str(news.zj_art_date)
                # 当前快讯所属分类
                group_name_list = list()
                news_groups = NewsGroupInfo.query.filter(NewsGroupInfo.news_id == news.id).all()
                for news_group_obj in news_groups:
                    group_id = news_group_obj.group_id
                    group_obj = NewsGroup.query.get(group_id)
                    group_name = group_obj.name
                    group_name_list.append(group_name)
                news_dict['group_name_list'] = group_name_list

            news_list.append(news_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=news_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='快讯列表查询失败')
    

# PC线上快讯分类列表
@api_news.route('/news_group_list', methods=['POST'])
@login_required
@admin_required
def news_group_list():
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
            page = int(page)
        except Exception as e:
            page, pagesize = 1, 10

        group_obj = NewsGroup.query.get(group_id)
        if not group_obj:
            return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

        # 查询当前分组下的快讯id_list 分页
        group_objs = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == group_id).order_by(
            NewsGroupInfo.create_time.desc()).all()
        count = len(group_objs)

        news_id_list = []
        for obj in group_objs:
            news_id_list.append(obj.news_id)
        news_id_list = news_id_list[(page - 1) * pagesize:page * pagesize]

        # 根据快讯id筛选快讯
        news_ls = []
        i = (page - 1) * pagesize + 1
        for news_id in news_id_list:
            news = NewsData.query.get(news_id)
            news_dict = {}
            news_dict['news_id'] = news_id
            news_dict['title'] = news.title
            news_dict['web_name'] = news.web_name
            news_dict['audio_url'] = news.audio_url
            news_dict['listen_num'] = news.listen_num
            news_dict['is_read'] = news.is_read
            news_dict['base_url'] = news.base_url
            news_dict['group_name'] = group_obj.name
            news_dict['location'] = i

            # stamp_time = get_time(str(news.zj_art_date))
            news_dict['zj_art_date'] = str(news.zj_art_date)
            i += 1

            news_ls.append(news_dict)
        return jsonify(errno=0, errmsg="OK", count=count, data=news_ls)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='快讯列表查询失败')


# PC快讯上线
@api_news.route('/news_upload', methods=['POST'])
@login_required
@admin_required
def news_upload():
    try:
        res = request.get_json()
        news_id_list = res.get('news_id_list')
        group_id_list = res.get('group_id_list')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([news_id_list, group_id_list]):
            return jsonify(errno=-1, errmsg="参数不完整")

        for group_id in group_id_list:
            group_obj = NewsGroup.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该类别不存在")
            else:
                for news_id in news_id_list:
                    news = NewsData.query.get(news_id)
                    if not news:
                        return jsonify(errno=-1, errmsg="参数错误,该快讯不存在", news_id=news_id)

                    result = NewsGroupInfo.query.filter(NewsGroupInfo.news_id == news_id,
                                                        NewsGroupInfo.group_id == group_id).first()
                    if result:
                        return jsonify(errno=-1, errmsg="参数错误,该快讯已上线", news_id=news_id)
                    else:
                        obj = NewsGroupInfo()

                        news.is_show = 1
                        news.zj_art_date = datetime.datetime.now()

                        obj.news_id = news_id
                        obj.group_id = group_id
                        obj.admin_id = admin_id

                        db.session.add(news)
                        db.session.add(obj)
                db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='上线失败')


# PC快讯下线
@api_news.route('/news_down_line', methods=['POST'])
@login_required
@admin_required
def news_down_line():
    try:
        res = request.get_json()
        news_id_list = res.get('news_id_list')
        group_id = res.get('group_id')
        admin_id = g.user_id

        now = datetime.datetime.now()
        Logging.logger.info('request_args:{0}'.format(res))
        if not news_id_list:
            return jsonify(errno=-1, errmsg="参数错误,请传入下线快讯的news_id")

        if group_id:
            # 传group_id
            # 下线当前快讯所在的当前类型
            group_obj = NewsGroup.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该分类不存在")

            for news_id in news_id_list:
                news = NewsData.query.get(news_id)
                if not news:
                    return jsonify(errno=-1, errmsg="参数错误,该快讯不存在", news_id=news)

                if news.is_show != 1:
                    return jsonify(errno=-1, errmsg="参数错误,该快讯未上线", news_id=news_id)

                obj = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == group_id,
                                                 NewsGroupInfo.news_id == news_id).first()
                if not obj:
                    return jsonify(errno=-1, errmsg="该快讯已上线，但不在该分类", news_id=news_id)

                db.session.delete(obj)
                group = NewsGroupInfo.query.filter(NewsGroupInfo.news_id == news_id).all()
                num = len(group)
                if num == 0:
                    # db.session.delete(obj)
                    news.is_show = 0
                    news.zj_art_date = now
                    news.admin_id = admin_id
                    db.session.add(news)
                    Logging.logger.info("快讯:{0} 在 {1} 被admin= {2} 全部下线成功".format(news.title, now, admin_id))

        else:
            # 不传group_id 下线当前快讯所在的全部类型
            for news_id in news_id_list:
                news = NewsData.query.get(news_id)
                if not news:
                    return jsonify(errno=-1, errmsg="参数错误,该快讯不存在", news_id=news_id)

                if news.is_show != 1:
                    return jsonify(errno=-1, errmsg="参数错误,该快讯未上线", news_id=news_id)

                objs = NewsGroupInfo.query.filter(NewsGroupInfo.news_id == news_id).all()
                for obj in objs:
                    # # 修改当前类型下所属快讯的sort_num
                    # results = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == obj.group_id).all()
                    # for art in results:
                    #     if art.sort_num > obj.sort_num:
                    #         art.sort_num -= 1
                    #         db.session.add(art)

                    db.session.delete(obj)
                news.is_show = 0
                news.zj_art_date = now
                news.admin_id = admin_id
                db.session.add(news)
                Logging.logger.info("快讯:{0} 在 {1} 被admin= {2} 全部下线成功".format(news.title, now, admin_id))

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='下线快讯失败')


# PC快讯删除
@api_news.route('/news_del', methods=['POST'])
@login_required
@admin_required
def news_del():
    try:
        res = request.get_json()
        news_id_list = res.get('news_id_list')

        Logging.logger.info('request_args:{0}'.format(res))
        if not news_id_list:
            return jsonify(errno=-1, errmsg="参数错误,请传入删除快讯的news_id")

        for news_id in news_id_list:
            news = NewsData.query.get(news_id)
            if not news:
                return jsonify(errno=-1, errmsg="快讯不存在", news_id=news_id)
            db.session.delete(news)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='下线快讯失败')


# 小程序--获取快讯分类类别
@api_news.route('/news_groups')
# @auth_required
def news_groups():
    try:
        groups = NewsGroup.query.filter(NewsGroup.is_show == 1).all()
        group_list = []
        for group in groups:
            group_dict = {}
            group_dict['news_group_id'] = group.id
            group_dict['news_group_name'] = group.name

            group_list.append(group_dict)

        return jsonify(errno=0, errmsg="OK", data=group_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--快讯列表
@api_news.route('/news_list')
# @auth_required
def news_list():
    try:
        groups = NewsGroup.query.filter(NewsGroup.is_show == 1).all()
        data = list()
        for group in groups:
            group_list = list()
            group_dict = dict()
            group_id = group.id
            group_name = group.name
            results = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == group_id).order_by(
                NewsGroupInfo.publish_time.desc()).all()
            for result in results:
                news_dict = dict()
                news_id = result.news_id
                news = NewsData.query.get(news_id)
                news_dict['title'] = news.title
                news_dict['news_id'] = news_id
                news_dict['listen_num'] = news.listen_num
                news_dict['audio_url'] = news.audio_url
                news_dict['is_read'] = news.is_read
                news_dict['has_content'] = news.has_content
                zj_art_date = str(news.zj_art_date)
                ch_date = zj_art_date.split(' ')[1].split(':')[:2]
                new_date = ch_date[0] + ':' + ch_date[1]
                news_dict['zj_art_date'] = new_date
                group_list.append(news_dict)
                break
            group_dict['group_name'] = group_name
            group_dict['group_id'] = group_id
            group_dict['group_data'] = group_list
            if group.listen_num:
                group_dict['listen_num'] = group.listen_num
            else:
                listen_num = random.randint(10000, 30001)
                group_dict['listen_num'] = listen_num
                group.listen_num = listen_num
                db.session.add(group)
                db.session.commit()
            data.append(group_dict)
        return jsonify(errno=0, errmsg="OK", data=data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--快讯详情(单篇)
@api_news.route('/news_detail', methods=['POST'])
@auth_required
def news_detail():
    try:
        res = request.get_json()
        news_id = res.get('news_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not news_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的快讯的news_id')

        news = NewsData.query.get(news_id)
        if not news:
            return jsonify(errno=-1, errmsg='参数错误,该快讯不存在')

        docs = mongo_store.news.find({'news_id': news_id})
        doc = docs[0]
        news_dict = dict()
        news_dict['title'] = news.title
        news_dict['content'] = doc.get('content')
        news_dict['audio_url'] = news.audio_url
        news_dict['is_read'] = news.is_read

        return jsonify(errno=0, errmsg="OK", data=news_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序快讯详情(分类列表显示)
@api_news.route('/news_group_detail', methods=['POST'])
# @auth_required
def news_group_detail():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的快讯的group_id')

        try:
            pagesize = int(pagesize)
            page = int(page)
        except Exception as e:
            page = 1
            pagesize = 10

        group = NewsGroup.query.get(group_id)
        if not group:
            return jsonify(errno=-1, errmsg='参数错误,该快讯类别不存在')
        group_name = group.name

        group_list = list()
        results = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == group_id).order_by(
            NewsGroupInfo.publish_time.desc()).all()
        count = len(results)

        results = results[(page - 1) * pagesize:page * pagesize]
        for result in results:
            news_dict = dict()
            news_id = result.news_id
            news = NewsData.query.get(news_id)
            news_dict['title'] = news.title
            news_dict['news_id'] = news_id
            news_dict['audio_url'] = news.audio_url
            news_dict['is_read'] = news.is_read
            if news.has_content == 1:
                docs = mongo_store.news.find({'news_id': news_id})
                doc = docs[0]
                news_dict['content'] = doc.get('content')
            else:
                news_dict['content'] = ''
            group_list.append(news_dict)

        return jsonify(errno=0, errmsg="OK", data=group_list, count=count, group_name=group_name)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--分类获取音频信息
@api_news.route('/news_audios', methods=['POST'])
# @auth_required
def news_audios():
    try:
        res = request.get_json()
        group_id = res.get('group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not group_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的快讯的group_id')

        group = NewsGroup.query.get(group_id)
        if not group:
            return jsonify(errno=-1, errmsg='参数错误,该快讯类别不存在')

        group_list = list()
        results = NewsGroupInfo.query.filter(NewsGroupInfo.group_id == group_id).order_by(
            NewsGroupInfo.publish_time.desc()).all()
        for result in results:
            news_id = result.news_id
            news = NewsData.query.get(news_id)
            group_list.append(news.audio_url)

        group.listen_num += 1
        db.session.add(group)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", data=group_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')