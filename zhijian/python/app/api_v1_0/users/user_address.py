# -*- coding:utf-8 -*-
# author: will
import re

from flask import request, jsonify

from app import db
from app.models import User, UserAddress
from utils.log_service import Logging
from utils.user_service.login import auth_required
from . import api_user


# 小程序--更新地址信息
@api_user.route('/update_user_address', methods=['POST'])
@auth_required
def update_user_address():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        name = res.get('name')
        phone = res.get('phone')
        provence = res.get('provence')
        city = res.get('city')
        area = res.get('area')
        detail = res.get('detail')
        post_num = res.get('post_num')
        address_id = res.get('address_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, name, phone, provence, city, area, detail, post_num]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户参数错误')

        ret = re.match(r"^1[35789]\d{9}$", str(phone))
        if not ret:
            return jsonify(errno=-1, errmsg='请输入正确的手机号')

        if not address_id:
            # 新增
            address = UserAddress()
            address.user_id = user_id
            address.name = name
            address.phone = phone
            address.provence = provence
            address.city = city
            address.area = area
            address.detail = detail
            address.post_num = post_num
            db.session.add(address)
        else:
            # 修改
            address = UserAddress.query.filter(UserAddress.user_id == user_id, UserAddress.id == address_id).first()
            if not address:
                return jsonify(errno=-1, errmsg='地址参数错误')

            address.name = name
            address.phone = phone
            address.provence = provence
            address.city = city
            address.area = area
            address.detail = detail
            address.post_num = post_num
            db.session.add(address)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK", address_id=address.id)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--用户地址信息列表
@api_user.route('/user_address_ls', methods=['POST'])
# @auth_required
def user_address_ls():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户参数错误')

        results = UserAddress.query.filter_by(user_id=user_id).all()
        if not results:
            return jsonify(errno=-1, errmsg='请填写收货地址信息')

        count = len(results)
        address_list = list()
        for address in results:
            address_dict = dict()
            address_dict['address_id'] = address.id
            address_dict['name'] = address.name
            address_dict['phone'] = address.phone
            address_dict['provence'] = address.provence
            address_dict['city'] = address.city
            address_dict['area'] = address.area
            address_dict['detail'] = address.detail
            address_dict['post_num'] = address.post_num
            address_list.append(address_dict)

        return jsonify(errno=0, errmsg="OK", data=address_list, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')
