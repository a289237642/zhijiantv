# -*- coding:utf-8 -*-
# author: will
from flask import request, jsonify, g

from app import db
from app.models import Group, WeChatName, WeChatNameGroup
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required
from . import api_article


# pc添加需要爬取的微信公众号
@api_article.route('/add_wechat_name', methods=['POST'])
@login_required
@admin_required
def add_wechat_name():
    try:
        res = request.get_json()
        wechat_name = res.get('wechat_name')
        alias = res.get('alias')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([wechat_name, alias]):
            return jsonify(errno=-1, errmsg='参数不完整')

        wechat = WeChatName.query.filter(WeChatName.wechat_name == wechat_name, WeChatName.alias == alias).first()
        if wechat:
            return jsonify(errno=-1, errmsg='该公众号已存在')
        else:
            obj = WeChatName()
            obj.wechat_name = wechat_name
            obj.alias = alias
            obj.is_show = 0
            obj.admin_id = admin_id

            db.session.add(obj)
            db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC公众号列表
@api_article.route('/wechat_name_list', methods=['POST'])
@login_required
@admin_required
def wechat_name_list():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        is_show = res.get('is_show', 0)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            pagesize = int(pagesize)
            page = int(page)
            is_show = int(is_show)
        except Exception as e:
            page = 1
            pagesize = 10
            is_show = 0

        results = WeChatName.query.filter(WeChatName.is_show == is_show).order_by(WeChatName.create_time.desc()).paginate(page, pagesize, False)
        count = results.total
        wechat_list = list()
        i = 1 + (page - 1) * pagesize
        for result in results.items:
            wechat_dict = dict()
            wechat_dict['wechat_name'] = result.wechat_name
            wechat_dict['alias'] = result.alias
            wechat_dict['wechat_id'] = result.id
            wechat_dict['location'] = i
            wechat_list.append(wechat_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", count=count, data=wechat_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# pc设置公众号对应文章分类
@api_article.route('/set_wechat_group', methods=['POST'])
@login_required
@admin_required
def set_wechat_group():
    try:
        res = request.get_json()
        wechat_id_list = res.get('wechat_id_list')
        group_id_list = res.get('group_id_list')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([wechat_id_list, group_id_list]):
            return jsonify(errno=-1, errmsg="参数不完整")

        for group_id in group_id_list:
            group_obj = Group.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该类别不存在")
            else:
                for wechat_id in wechat_id_list:
                    wechat = WeChatName.query.get(wechat_id)
                    if not wechat:
                        return jsonify(errno=-1, errmsg="参数错误,该公众号不存在", wechat_id=wechat_id)

                    result = WeChatNameGroup.query.filter(WeChatNameGroup.wechat_id == wechat_id,
                                                          WeChatNameGroup.group_id == group_id).first()
                    if result:
                        return jsonify(errno=-1, errmsg="参数错误,该公众号已有对应分类", wechat_id=wechat_id, group_id=group_id)
                    else:
                        obj = WeChatNameGroup()
                        obj.wechat_id = wechat_id
                        obj.group_id = group_id
                        obj.admin_id = admin_id
                        db.session.add(obj)
                    wechat.is_show = 1
                    db.session.add(wechat)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='上线失败')


# PC公众号重设
@api_article.route('/reset_wechat_group', methods=['POST'])
@login_required
@admin_required
def reset_wechat_group():
    try:
        res = request.get_json()
        wechat_id_list = res.get('wechat_id_list')
        group_id = res.get('group_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not wechat_id_list:
            return jsonify(errno=-1, errmsg="请选择要重设的公众号")

        if not group_id:
            # 不传group_id 下线当前公众号所在的全部类型
            for wechat_id in wechat_id_list:
                wechat = WeChatName.query.get(wechat_id)
                if not wechat:
                    return jsonify(errno=-1, errmsg="参数错误,该公众号不存在", wechat_id=wechat_id)

                if wechat.is_show != 1:
                    return jsonify(errno=-1, errmsg="参数错误,该公众号未设置分类", wechat_id=wechat_id)

                groups = WeChatNameGroup.query.filter(WeChatNameGroup.wechat_id == wechat_id).all()
                for obj in groups:
                    db.session.delete(obj)
                wechat.is_show = 0
                wechat.admin_id = admin_id
                db.session.add(wechat)
        else:
            try:
                group_id = int(group_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg="参数错误,请传入int类型group_id")

            group_obj = Group.query.get(group_id)
            if not group_obj:
                return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

            for wechat_id in wechat_id_list:
                wechat = WeChatName.query.get(wechat_id)
                if not wechat:
                    return jsonify(errno=-1, errmsg="参数错误,该公众号不存在", wechat_id=wechat_id)

                result = WeChatNameGroup.query.filter(WeChatNameGroup.wechat_id == wechat_id,
                                                      WeChatNameGroup.group_id == group_id).first()
                if not result:
                    return jsonify(errno=-1, errmsg="参数错误,该公众号不在该类别", wechat_id=wechat_id, group_id=group_id)

                db.session.delete(result)
                group = WeChatNameGroup.query.filter(WeChatNameGroup.wechat_id == wechat_id).all()
                num = len(group)
                if num == 0:
                    wechat.is_show = 0
                    wechat.admin_id = admin_id
                    db.session.add(wechat)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# pc公众号分类列表
@api_article.route('/wechat_name_group', methods=['POST'])
@login_required
@admin_required
def wechat_name_group():
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

        group_obj = Group.query.get(group_id)
        if not group_obj:
            return jsonify(errno=-1, errmsg="参数错误,该类别不存在")

        results = WeChatNameGroup.query.filter(WeChatNameGroup.group_id == group_id).order_by(
            WeChatNameGroup.create_time.desc()).paginate(page, pagesize, False)
        count = results.total
        wechat_list = list()
        i = 1 + (page - 1) * pagesize
        for result in results.items:
            wechat_dict = dict()
            obj = WeChatName.query.get(result.wechat_id)
            wechat_dict['wechat_name'] = obj.wechat_name
            wechat_dict['alias'] = obj.alias
            wechat_dict['wechat_id'] = result.wechat_id
            wechat_dict['location'] = i
            wechat_list.append(wechat_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", count=count, data=wechat_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 删除公众号
@api_article.route('/del_wechat_name', methods=['POST'])
@login_required
@admin_required
def del_wechat_name():
    try:
        res = request.get_json()
        wechat_id_list = res.get('wechat_id_list')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not wechat_id_list:
            return jsonify(errno=-1, errmsg='请选择要删除的公众号ID')

        for wechat_id in wechat_id_list:
            obj = WeChatName.query.get(wechat_id)
            if not obj:
                return jsonify(errno=-1, errmsg='公众号不存在', wechat_id=wechat_id)
            db.session.delete(obj)
            Logging.logger.info('公众号: {0} 被admin={1} 删除成功'.format(obj.wechat_name, admin_id))

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')
