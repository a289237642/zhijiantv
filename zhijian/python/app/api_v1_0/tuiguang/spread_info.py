# -*- coding:utf-8 -*-
# author: will
from flask import request, jsonify, g

from app import db
from app.models import SpreadName, SpreadType, SpreadRecord
from utils.log_service import Logging
from utils.qr_service import get_qr_func
from utils.user_service.login import login_required, admin_required
from . import api_spread


# 渠道推广方式
@api_spread.route('/spread_type')
@login_required
@admin_required
def spread_type():
    try:
        results = SpreadType.query.all()
        type_list = list()
        for res in results:
            type_dict = dict()
            type_dict['spread_type_id'] = res.id
            type_dict['spread_type_name'] = res.name
            type_list.append(type_dict)

        return jsonify(errno=0, errmsg="OK", data=type_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 渠道增加/修改
@api_spread.route('/spread_name_update', methods=['POST'])
@login_required
@admin_required
def spread_name_update():
    try:
        res = request.get_json()
        spread_name = res.get('spread_name')
        spread_type_id = res.get('spread_type_id')
        spread_id = res.get('spread_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))

        if not all([spread_name, spread_type_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        type_obj = SpreadType.query.get(spread_type_id)
        if not type_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if not spread_id:
            # 新增
            obj = SpreadName()
            obj.spread_type_id = spread_type_id
            obj.name = spread_name
            obj.admin_id = admin_id
        else:
            # 修改
            obj = SpreadName.query.get(spread_id)
            if not obj:
                return jsonify(errno=-1, errmsg='参数错误')
            obj.spread_type_id = spread_type_id
            obj.name = spread_name
            obj.admin_id = admin_id

        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", spread_id=obj.id)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 生成渠道链接
@api_spread.route('/generate_spread_url', methods=['POST'])
@login_required
@admin_required
def generate_spread_url():
    try:
        res = request.get_json()
        page = res.get('page')
        scene = res.get('scene')
        path = res.get('path')
        spread_id = res.get('spread_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not spread_id:
            return jsonify(errno=-1, errmsg='请传入渠道ID')

        obj = SpreadName.query.get(spread_id)
        if not obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if page and scene:
            url = get_qr_func(page, scene)
            if url:
                obj.spread_url = url
                obj.admin_id = admin_id
            else:
                return jsonify(errno=-1, errmsg='二维码生成失败')

        elif path:
            obj.spread_url = path
            obj.admin_id = admin_id

        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 渠道列表
@api_spread.route('/spread_name_ls', methods=['POST'])
@login_required
@admin_required
def spread_name_ls():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        results = SpreadName.query.filter(SpreadName.is_del == 1) \
            .order_by(SpreadName.create_time.desc()).paginate(page, pagesize, False)
        count = results.total

        spread_list = list()
        i = (page - 1) * pagesize + 1
        for result in results.items:
            spread_dict = dict()
            spread_dict['spread_id'] = result.id
            spread_dict['spread_name'] = result.name
            spread_dict['spread_type_id'] = result.spread_type_id
            spread_dict['spread_url'] = result.spread_url
            spread_dict['location'] = i
            i += 1
            spread_list.append(spread_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=spread_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 渠道名称搜索
@api_spread.route('/spread_name_search', methods=['POST'])
@login_required
@admin_required
def spread_name_search():
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
            all_results = SpreadName.query.filter(SpreadName.is_del == 1).filter(
                SpreadName.name.like("%" + words + "%")).order_by(
                SpreadName.create_time.desc()).paginate(page, pagesize, False)
        else:
            all_results = SpreadName.query.filter(SpreadName.is_del == 1).order_by(
                SpreadName.create_time.desc()).paginate(page, pagesize, False)

        count = all_results.total
        spread_list = list()
        i = (page - 1) * pagesize + 1
        for result in all_results.items:
            spread_dict = dict()
            spread_dict['spread_id'] = result.id
            spread_dict['spread_name'] = result.name
            spread_dict['spread_type_id'] = result.spread_type_id
            spread_dict['spread_url'] = result.spread_url
            spread_dict['location'] = i
            spread_list.append(spread_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", count=count, data=spread_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 渠道删除
@api_spread.route('/spread_name_del', methods=['POST'])
@login_required
@admin_required
def spread_name_del():
    try:
        res = request.get_json()
        spread_id = res.get('spread_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            spread_id = int(spread_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        obj = SpreadName.query.get(spread_id)
        if not obj:
            return jsonify(errno=-1, errmsg='参数错误')
        obj.is_del = -1
        obj.admin_id = admin_id
        db.session.add(obj)

        results = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id, SpreadRecord.is_del == 1).all()
        if results:
            for result in results:
                result.is_del = -1
                result.admin_id = admin_id
                db.session.add(result)

        db.session.commit()
        Logging.logger.warning('渠道{0}被ID={1}的管理员删除'.format(obj.name, admin_id))
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
