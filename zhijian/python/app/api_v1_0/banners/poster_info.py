# -*- coding:utf-8 -*-
# author: will
import datetime

from app.models import Poster
from utils.user_service.login import login_required, admin_required
from . import api_banner

import logging

from flask import jsonify, request, g
from app import db


# 小程序海报显示
@api_banner.route('/poster')
def poster():
    try:
        poster_obj = Poster.query.filter_by(is_show=1).first()
        if not poster_obj:
            return jsonify(errno=-1, errmsg='请启用海报')

        if poster_obj.end_time < datetime.datetime.now():
            return jsonify(errno=-1, errmsg='当前海报已过期')

        poster_dict = dict()
        poster_dict['id'] = poster_obj.id
        poster_dict['pic'] = poster_obj.pic
        poster_dict['is_show'] = poster_obj.is_show
        poster_dict['jump_url'] = poster_obj.jump_url

        return jsonify(errno=0, errmsg="OK", data=poster_dict)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc海报列表
@api_banner.route('/pc_poster_list')
@login_required
@admin_required
def pc_poster_list():
    try:
        results = Poster.query.all()
        poster_list = list()
        for result in results:
            poster_dict = dict()
            poster_dict['id'] = result.id
            poster_dict['is_show'] = result.is_show
            poster_dict['pic'] = result.pic
            poster_dict['jump_url'] = result.jump_url
            poster_dict['start_time'] = str(result.start_time)
            poster_dict['end_time'] = str(result.end_time)

            poster_list.append(poster_dict)
        return jsonify(errno=0, errmsg="OK", data=poster_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 增加或修改海报
@api_banner.route('/update_poster', methods=['POST'])
@login_required
@admin_required
def update_poster():
    try:
        res = request.get_json()
        poster_id = res.get('poster_id')
        pic = res.get('pic')
        is_show = res.get('is_show')
        jump_url = res.get('jump_url')
        start_time = res.get('start_time')
        end_time = res.get('end_time')
        admin_id = g.user_id

        print("请求参数:", request.data)
        if not all([pic, jump_url, start_time, end_time]):
            return jsonify(errno=-1, errmsg='参数不完整')

        if poster_id:
            # 修改
            poster_obj = Poster.query.get(poster_id)
            if not poster_obj:
                return jsonify(errno=-1, errmsg='海报不存在')

            poster_obj.pic = pic
            poster_obj.jump_url = jump_url
            poster_obj.start_time = start_time
            poster_obj.end_time = end_time
            poster_obj.is_show = is_show
            poster_obj.admin_id = admin_id

            db.session.add(poster_obj)
        else:
            obj = Poster()
            obj.pic = pic
            obj.jump_url = jump_url
            obj.start_time = start_time
            obj.end_time = end_time
            obj.is_show = is_show
            obj.admin_id = admin_id
            db.session.add(obj)

        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 删除海报
@api_banner.route('/del_poster', methods=['POST'])
@login_required
@admin_required
def del_poster():
    try:
        res = request.get_json()
        poster_id = res.get('poster_id')

        print("请求参数:", request.data)
        poster_obj = Poster.query.get(poster_id)
        if not poster_obj:
            return jsonify(errno=-1, errmsg='海报不存在')

        db.session.delete(poster_obj)
        print("删除的海报的ID:", poster_id)

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
