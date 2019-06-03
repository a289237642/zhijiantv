# -*- coding:utf-8 -*-
# author: will
import logging

from flask import jsonify, request, g

from app import db
from app.models import Icon
from utils.user_service.login import login_required, admin_required
from . import api_lesson


# 小程序icon列表
@api_lesson.route('/icon_list')
def icon_list():
    try:
        results = Icon.query.all()
        icon_list = list()
        for result in results:
            icon_dict = dict()
            icon_dict['id'] = result.id
            icon_dict['name'] = result.name
            icon_dict['pic'] = result.pic
            icon_dict['jump_url'] = result.jump_url
            icon_list.append(icon_dict)
        return jsonify(errno=0, errmsg="OK", data=icon_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc_icon列表
@api_lesson.route('/pc_icon_list')
@login_required
@admin_required
def pc_icon_list():
    try:
        results = Icon.query.all()
        icon_list = list()
        for result in results:
            icon_dict = dict()
            icon_dict['id'] = result.id
            icon_dict['name'] = result.name
            icon_dict['pic'] = result.pic
            icon_dict['jump_url'] = result.jump_url
            icon_list.append(icon_dict)
        return jsonify(errno=0, errmsg="OK", data=icon_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 增加或修改icon
@api_lesson.route('/update_icon', methods=['POST'])
@login_required
@admin_required
def update_icon():
    try:
        res = request.get_json()
        icon_id = res.get('icon_id')
        name = res.get('name')
        pic = res.get('pic')
        jump_url = res.get('jump_url')
        admin_id = g.user_id

        print("请求参数:", request.data)
        if not all([name, pic, jump_url]):
            return jsonify(errno=-1, errmsg='参数不完整')

        if icon_id:
            # 修改
            icon_obj = Icon.query.get(icon_id)
            if not icon_obj:
                return jsonify(errno=-1, errmsg='icon不存在')

            icon_obj.name = name
            icon_obj.pic = pic
            icon_obj.jump_url = jump_url
            icon_obj.admin_id = admin_id

            db.session.add(icon_obj)
        else:
            obj = Icon()
            obj.name = name
            obj.pic = pic
            obj.jump_url = jump_url
            obj.admin_id = admin_id
            db.session.add(obj)

        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# icon删除
@api_lesson.route('/del_icon', methods=['POST'])
@login_required
@admin_required
def del_icon():
    try:
        res = request.get_json()
        icon_id = res.get('icon_id')

        print("请求参数:", request.data)
        icon_obj = Icon.query.get(icon_id)
        if not icon_obj:
            return jsonify(errno=-1, errmsg='icon不存在')

        db.session.delete(icon_obj)
        print("删除的icon的ID:", icon_id)

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
