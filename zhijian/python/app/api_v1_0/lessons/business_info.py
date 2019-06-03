# Author:zcc
# -*- coding:utf-8 -*-
from flask import request
from flask.json import jsonify

from app import db
from app.api_v1_0.lessons import api_lesson
from app.models import BusinessCollege
from utils.user_service.login import login_required, admin_required


# 新增修改商学院
@api_lesson.route('/create_bussiness', methods=['POST'])
@login_required
@admin_required
def create_bussiness():
    params = request.get_json()
    pic = params.get('pic')
    jump_url = params.get('jump_url')
    is_show = params.get('is_show')
    appid = params.get('appid')
    bussiness_lesson_id = params.get('bussiness_lesson_id')
    try:
        if bussiness_lesson_id:
            bl_obj = BusinessCollege.query.get(bussiness_lesson_id)
            if bl_obj:
                bl_obj.pic = pic
                bl_obj.jump_url = jump_url
                bl_obj.is_show = 1
                bl_obj.appid = appid
                db.session.add(bl_obj)
                db.session.commit()
                return jsonify(errno=0, errmsg='修改成功')
            else:
                return jsonify(errno=-1, errmsg='课程不存在')
        else:
            bl_obj = BusinessCollege()
            bl_obj.pic = pic
            bl_obj.jump_url = jump_url
            bl_obj.is_show = 1
            bl_obj.appid = appid
            db.session.add(bl_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='新增成功')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg="网络异常")


# pc修改商学院状态
@api_lesson.route('/change_bussiness', methods=['POST'])
@login_required
@admin_required
def change_bussiness():
    params = request.get_json()
    bussiness_lesson_id = params.get('bussiness_lesson_id')
    try:
        bl_obj = BusinessCollege.query.get(bussiness_lesson_id)
        if bl_obj:
            state = 0 if bl_obj.is_show else 1
            bl_obj.is_show = state
            db.session.add(bl_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='修改成功')
        else:
            return jsonify(errno=-1, errmsg='课程不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg="网络异常")


# pc删除商学院
@api_lesson.route('/delete_bussiness', methods=['POST'])
@login_required
@admin_required
def delete_bussiness():
    params = request.get_json()
    bussiness_lesson_id = params.get('bussiness_lesson_id')
    try:
        bl_obj = BusinessCollege.query.get(bussiness_lesson_id)
        if bl_obj:
            db.session.delete(bl_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='删除成功')
        else:
            return jsonify(errno=-1, errmsg='课程不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg="网络异常")


# pc商学院列表
@api_lesson.route('/get_pc_bussiness', methods=['POST'])
@login_required
@admin_required
def get_pc_bussiness():
    res = request.get_json()
    page = int(res.get('page', 1))
    pagesize = int(res.get('pagesize', 3))
    try:
        result = BusinessCollege.query.order_by(BusinessCollege.create_time.asc()).paginate(page, pagesize, False)
        count = result.total
        arr = list()
        for item in result.items:
            data = dict()
            data['pic'] = item.pic
            data['bussiness_lesson_id'] = item.id
            data['jump_url'] = item.jump_url
            data['is_show'] = item.is_show
            data['appid'] = item.appid
            arr.append(data)
        return jsonify(errno=0, data=arr, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序商学院列表
@api_lesson.route('/get_bussiness', methods=['POST'])
def get_bussiness():
    res = request.get_json()
    try:
        result = BusinessCollege.query.filter(BusinessCollege.is_show == 1).paginate(1, 3, False)
        count = result.total
        arr = list()
        for item in result.items:
            data = dict()
            data['pic'] = item.pic
            data['bussiness_lesson_id'] = item.id
            data['jump_url'] = item.jump_url
            data['appid'] = item.appid
            arr.append(data)
        return jsonify(errno=0, data=arr, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')
