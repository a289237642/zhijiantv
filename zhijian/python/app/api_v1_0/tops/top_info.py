# -*- coding:utf-8 -*-
# author: will
import datetime
import logging
from flask import request, jsonify, g

from app import db
from app.models import Top, Article, ArticleGroup, Group, UserBTN, UpdateTime
from utils.user_service.login import login_required, admin_required
from . import api_top


# 头条的添加和修改,自定义排序
@api_top.route('/add_top', methods=['POST'])
@login_required
@admin_required
def add_top():
    try:
        res = request.get_json()
        content = res.get('content')
        top_id = res.get('top_id')
        sort_num = res.get('sort_num')
        group_id = res.get('group_id')
        article_id = res.get('article_id')
        admin_id = g.user_id

        print('请求参数:', request.data)
        if not top_id:
            # 新增 (不传id)
            # 默认隐藏,显示在所有隐藏头条的最前,所有已显示头条的后面
            if not content:
                return jsonify(errno=-1, errmsg='参数错误,请传入新增头条的内容')

            if group_id:
                group = Group.query.get(group_id)
                if not group:
                    return jsonify(errno=-1, errmsg='参数错误,传入的文章类型不存在')

                if not article_id:
                    return jsonify(errno=-1, errmsg='参数错误,请传入选择要跳转的文章')

                try:
                    article_id = int(article_id)
                except Exception as e:
                    logging.error(e)
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                article = Article.query.get(article_id)
                if not article:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章不存在')

                if article.is_show == 0:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章未上线')

                article_obj = ArticleGroup.query.filter(ArticleGroup.group_id == group_id,
                                                        ArticleGroup.article_id == article_id).first()
                if not article_obj:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章和文章所属类型不对照')

            tops = Top.query.all()
            obj = Top()
            if not sort_num:
                show_tops = Top.query.filter(Top.is_show == 1).all()
                no_show_tops = Top.query.filter(Top.is_show == 0).all()
                count = len(show_tops)
                obj.sort_num = count + 1
                obj.content = content
                obj.group_id = group_id
                obj.article_id = article_id
                obj.admin_id = admin_id
                db.session.add(obj)
                for top in no_show_tops:
                    top.sort_num += 1
                    db.session.add(top)

            else:
                # 自定义排序
                try:
                    sort_num = int(sort_num)
                except Exception as e:
                    logging.error(e)
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                total_num = len(tops) + 1
                if sort_num > total_num:
                    return jsonify(errno=-1, errmsg='参数错误,传入的sort_num值超出范围')

                for top_obj in tops:
                    if top_obj.sort_num >= sort_num:
                        top_obj.sort_num += 1
                        db.session.add(top_obj)

                obj.content = content
                obj.group_id = group_id
                obj.article_id = article_id
                obj.sort_num = sort_num
                obj.admin_id = admin_id
                db.session.add(obj)

        else:
            # 修改（传id）
            try:
                top_id = int(top_id)
            except Exception as e:
                logging.error(e)
                return jsonify(errno=-1, errmsg='参数错误,请传入int类型的top_id')

            top_obj = Top.query.get(top_id)
            if not top_obj:
                return jsonify(errno=-1, errmsg='参数错误,该头条不存在')

            if not content:
                content = top_obj.content

            if group_id:
                group = Group.query.get(group_id)
                if not group:
                    return jsonify(errno=-1, errmsg='参数错误,传入的文章类型不存在')

                if not article_id:
                    article_id = top_obj.article_id

                try:
                    article_id = int(article_id)
                except Exception as e:
                    logging.error(e)
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                article = Article.query.get(article_id)
                if not article:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章不存在')

                if article.is_show == 0:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章未上线')

                article_obj = ArticleGroup.query.filter(ArticleGroup.group_id == group_id,
                                                        ArticleGroup.article_id == article_id).first()
                if not article_obj:
                    return jsonify(errno=-1, errmsg='参数错误,跳转的文章和文章所属类型不对照')
            else:
                group_id = top_obj.group_id
                article_id = top_obj.article_id

            if sort_num:
                # 自定义排序
                try:
                    sort_num = int(sort_num)
                except Exception as e:
                    logging.error(e)
                    return jsonify(errno=-1, errmsg='参数错误,请传入int类型的sort_num')

                tops = Top.query.all()
                total_num = len(tops)
                if sort_num > total_num:
                    return jsonify(errno=-1, errmsg='参数错误,传入的sort_num值超出范围')

                for top in tops:
                    # 往前调 10-->1
                    if top_obj.sort_num > sort_num:
                        # 选取修改范围
                        if sort_num <= top.sort_num < top_obj.sort_num:
                            # 先加再赋值
                            top.sort_num += 1
                            db.session.add(top)

                    # 往后调 1-->10
                    elif top_obj.sort_num < sort_num:
                        # 选取修改范围
                        if top_obj.sort_num < top.sort_num <= sort_num:
                            # 先减再赋值
                            top.sort_num -= 1
                            db.session.add(top)
                    else:
                        # 头条位置不变
                        top_obj.sort_num = sort_num
                    # 赋值
                top_obj.sort_num = sort_num
            else:
                # 不传sort_num,值不变
                top_obj.sort_num = top_obj.sort_num

            top_obj.content = content
            top_obj.group_id = group_id
            top_obj.article_id = article_id
            top_obj.admin_id = admin_id
            db.session.add(top_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg='OK')
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='添加头条失败')


# 小程序获取头条信息
@api_top.route('/tops', methods=['POST'])
def tops():
    res = request.get_json()
    page = res.get('page', 1)
    pagesize = res.get('pagesize', 3)

    print('请求参数:', request.data)
    try:
        page = int(page)
    except Exception as e:
        print(e)
        page = 1

    try:
        pagesize = int(pagesize)
    except Exception as e:
        print(e)
        pagesize = 3

    try:
        tops = Top.query.filter(Top.is_show == 1).order_by(
            Top.sort_num, Top.create_time.desc()).all()

        count = Top.query.filter(Top.is_show == 1).count()
        tops = tops[(page - 1) * pagesize:page * pagesize]

        top_list = []
        for top in tops:
            top_dict = {}
            top_dict['top_id'] = top.id
            top_dict['content'] = top.content
            top_dict['create_time'] = str(top.create_time)
            # top_dict['sort_num'] = top.sort_num
            top_dict['jump_article_group_id'] = top.group_id
            top_dict['jump_article_id'] = top.article_id
            article = Article.query.get(top.article_id)
            if article:
                top_dict['jump_article_title'] = article.title

            top_list.append(top_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=top_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='头条查询失败')


# 隐藏或发布头条
@api_top.route('/upload_top', methods=['POST'])
@login_required
@admin_required
def upload_top():
    res = request.get_json()
    top_id = res.get('top_id')
    is_show = res.get('is_show')
    admin_id = g.user_id

    print('请求参数:', request.data)
    top_obj = Top.query.get(top_id)
    if not top_obj:
        return jsonify(errno=-1, errmsg='参数错误,该头条不存在')

    is_show = int(is_show)
    if is_show not in [0, 1]:
        return jsonify(errno=-1, errmsg='is_show参数错误,请传入1或0')

    obj = Top.query.filter(Top.is_show == is_show, Top.id == top_id).first()
    if not obj:
        return jsonify(errno=-1, errmsg='参数错误,该头条当前状态错误')

    try:
        if is_show == 0:
            # 显示
            top_obj.is_show = 1
            top_obj.top_date = datetime.datetime.now()

            # 记录小程序头条有更新,发送通知
            records = UserBTN.query.filter(UserBTN.btn_num == 3).all()
            for record in records:
                record.is_new = 1
                record.is_send = 0
                db.session.add(record)

            # 记录更新的时间
            today = datetime.datetime.today().date()
            up_obj = UpdateTime.query.filter(UpdateTime.type == 4).filter(
                UpdateTime.create_time.like(str(today) + "%")).first()
            if not up_obj:
                time_obj = UpdateTime()
                time_obj.type = 4
                db.session.add(time_obj)
        else:
            # 隐藏
            top_obj.is_show = 0
        top_obj.admin_id = admin_id
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='设置失败')

    try:
        db.session.add(top_obj)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
    return jsonify(errno=0, errmsg="OK")


# pc端头条信息列表
@api_top.route('/pc_tops', methods=['POST'])
@login_required
@admin_required
def pc_tops():
    res = request.get_json()
    page = res.get('page', 1)
    pagesize = res.get('pagesize', 10)

    print('请求参数:', request.data)
    try:
        page = int(page)
    except Exception as e:
        print(e)
        page = 1

    try:
        pagesize = int(pagesize)
    except Exception as e:
        print(e)
        pagesize = 10

    try:
        # 已显示的头条在前面,且显示排序号
        is_show_tops = Top.query.filter(Top.is_show == 1).order_by(
            Top.sort_num, Top.create_time.desc()).all()

        tops = Top.query.all()
        count = len(tops)

        top_list = []
        for top in is_show_tops:
            top_dict = {}
            top_dict['top_id'] = top.id
            top_dict['content'] = top.content
            top_dict['create_time'] = str(top.create_time)
            top_dict['is_show'] = top.is_show
            top_dict['sort_num'] = top.sort_num
            top_dict['jump_article_group_id'] = top.group_id
            top_dict['jump_article_id'] = top.article_id
            article = Article.query.get(top.article_id)
            if article:
                top_dict['jump_article_title'] = article.title
            top_list.append(top_dict)
        # 隐藏的头条在显示的头条后面,且不显示排序号,默认时间由近到远
        no_show_tops = Top.query.filter(Top.is_show == 0).order_by(
            Top.create_time.desc()).all()

        for top in no_show_tops:
            top_dict = {}
            top_dict['top_id'] = top.id
            top_dict['content'] = top.content
            top_dict['create_time'] = str(top.create_time)
            top_dict['is_show'] = top.is_show
            top_dict['sort_num'] = top.sort_num
            top_dict['jump_article_group_id'] = top.group_id
            top_dict['jump_article_id'] = top.article_id

            article = Article.query.get(top.article_id)
            if article:
                top_dict['jump_article_title'] = article.title

            top_list.append(top_dict)

        top_list = top_list[(page - 1) * pagesize:page * pagesize]

        return jsonify(errno=0, errmsg="OK", count=count, data=top_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='头条查询失败')


# pc端删除头条信息
@api_top.route('/del_top', methods=['POST'])
@login_required
@admin_required
def del_top():
    res = request.get_json()
    top_id = res.get("top_id")

    print('请求参数:', request.data)
    if not top_id:
        return jsonify(errno=-1, errmsg='参数错误,请传入要删除头条的top_id')

    top_obj = Top.query.get(top_id)
    if not top_obj:
        return jsonify(errno=-1, errmsg='参数错误,该头条不存在')

    try:
        # 修改所有头条的sort_num
        tops = Top.query.all()
        for top in tops:
            if top.sort_num > top_obj.sort_num:
                top.sort_num -= 1
                db.session.add(top)
        db.session.delete(top_obj)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
    return jsonify(errno=0, errmsg="OK")
