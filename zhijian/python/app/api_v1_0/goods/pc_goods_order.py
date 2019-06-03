# -*- coding:utf-8 -*-
# author: will
import datetime
import json
import re
import time

import requests
from flask import request, jsonify, g

from app import db
from app.models import GoodsOrder, Goods, UserAddress, GoodsImage, ExpressInfo, Admin
from common.error_code import ErrorCode
from common.response import build_response
from params_service.goods.pc_goods_order_service import LsParamsCheck, DetailParamsCheck, ExpressParamsCheck
from utils.log_service import Logging
from utils.time_service import unix_time
from utils.to_dict import query_to_dict
from utils.user_service.login import login_required, admin_required
from utils.user_service.wechat_pay import OrderQuery
from view_service.goods.pc_goods_order_service import ls_data_service, detail_data_service, close_data_service, \
    express_data_service
from . import api_goods


# PC--订单分类列表
@api_goods.route('/pc_goods_order_ls', methods=['POST'])
@login_required
@admin_required
def pc_goods_order_ls():
    try:
        res = request.get_json()
        Logging.logger.info('request_args:{0}'.format(res))

        params_status, (code, msg) = LsParamsCheck.ls_params_check(res)
        if not params_status:
            return build_response(errno=code, errmsg=msg)

        data_status, data = ls_data_service(res)
        if not data_status:
            return build_response(errno=data[0], errmsg=data[1])
        doc = dict(order_list=data[0], count=data[1])

        return build_response(doc)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return build_response(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])


# PC--订单搜索
@api_goods.route('/pc_goods_order_query', methods=['POST'])
@login_required
@admin_required
def pc_goods_order_query():
    try:
        res = request.get_json()
        order_num = res.get('order_num')
        goods_name = res.get('goods_name')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))

        params_status, (code, msg) = LsParamsCheck.params_check(res)
        if not params_status:
            return jsonify(errno=code, errmsg=msg)

        if order_num:
            if goods_name:
                goods = Goods.query.filter(Goods.name.like("%" + goods_name + "%")).all()
                goods_id_ls = [x.id for x in goods]
                orders = GoodsOrder.query.filter(GoodsOrder.goods_id.in_(goods_id_ls),
                                                 GoodsOrder.order_num == order_num).order_by(
                    GoodsOrder.create_time.desc()).paginate(page, pagesize, False)
            else:
                orders = GoodsOrder.query.filter_by(order_num=order_num).order_by(GoodsOrder.create_time.desc()).paginate(page, pagesize, False)
        else:
            if goods_name:
                goods = Goods.query.filter(Goods.name.like("%" + goods_name + "%")).all()
                goods_id_ls = [x.id for x in goods]

                orders = GoodsOrder.query.filter(GoodsOrder.goods_id.in_(goods_id_ls)).order_by(
                    GoodsOrder.create_time.desc()).paginate(page, pagesize, False)
            else:
                orders = GoodsOrder.query.paginate(page, pagesize, False)

        count = orders.total
        # orders = orders[(page - 1) * pagesize:page * pagesize]
        order_list = list()
        for order in orders.items:
            order_dict = dict()
            order_dict['order_id'] = order.id
            order_dict['order_num'] = order.order_num
            order_dict['price'] = order.price
            order_dict['postage'] = order.postage
            order_dict['order_status'] = order.order_status
            order_dict['create_time'] = str(order.create_time)

            goods_id = order.goods_id
            goods_obj = Goods.query.get(goods_id)
            order_dict['goods_name'] = goods_obj.name

            img_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_id, GoodsImage.is_min == 1).first()
            order_dict['img_url'] = img_obj.img_url

            address_id = order.address_id
            address = UserAddress.query.get(address_id)
            address_dict = dict()
            address_dict['name'] = address.name
            address_dict['phone'] = address.phone
            address_dict['provence'] = address.provence
            address_dict['city'] = address.city
            address_dict['area'] = address.area
            address_dict['detail'] = address.detail
            address_dict['post_num'] = address.post_num

            order_dict['address_data'] = address_dict
            order_list.append(order_dict)

        return jsonify(errno=0, errmsg='ok', order_list=order_list, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg="网络错误")


# PC--查询用户微信支付状态
@api_goods.route('/wechat_pay_query', methods=['POST'])
# @login_required
# @admin_required
def wechat_pay_query():
    try:
        res = request.get_json()
        order_num = res.get('order_num')

        Logging.logger.info('request_args:{0}'.format(res))
        order_obj = GoodsOrder.query.filter_by(order_num=order_num).first()
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        # order_status = order_obj.order_status
        # if order_status == 1:
        #     return jsonify(errno=-1, errmsg='当前查询订单未支付')

        transaction_id = order_obj.transaction_id

        pay = OrderQuery()
        # 微信订单查询接口
        url = pay.url

        # 拿到封装好的xml数据
        body_data = pay.get_xml_data(transaction_id)

        # 请求微信订单查询接口
        result = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
        content = pay.xmlToArray(result.content)

        Logging.logger.info('微信订单查询返回数据:{0}'.format(content))
        return jsonify(errno=0, errmsg="OK", data=content)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# PC--发货
@api_goods.route('/bulk_send_goods', methods=['POST'])
@login_required
@admin_required
def bulk_send_goods():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        express_num = res.get('express_num')
        company = res.get('company')
        remark = res.get('remark')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在', order_id=order_id)

        if order_obj.order_status != 2:
            return jsonify(errno=-1, errmsg='当前订单状态不支持该操作', order_id=order_id)

        now = datetime.datetime.now()
        order_obj.order_status = 3
        order_obj.send_time = now

        express_obj = ExpressInfo()
        express_obj.admin_id = admin_id
        express_obj.order_id = order_id
        express_obj.express_num = express_num
        express_obj.company = company
        express_obj.remark = remark

        db.session.add(order_obj)
        db.session.add(express_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC--订单详情
@api_goods.route('/pc_goods_order_detail', methods=['POST'])
@login_required
@admin_required
def pc_goods_order_detail():
    try:
        res = request.get_json()
        order_id = res.get('order_id')

        Logging.logger.info('request_args:{0}'.format(res))

        if not isinstance(order_id, int):
            return jsonify(errno=-1, errmsg='参数错误')

        order = GoodsOrder.query.get(order_id)
        if not order:
            return jsonify(errno=-1, errmsg='订单不存在', order_id=order_id)

        # params_status, result = DetailParamsCheck.detail_params_check(res)
        # if not params_status:
        #     return jsonify(errno=result[0], errmsg=result[1])

        order_data = detail_data_service(res)
        return jsonify(errno=0, errmsg="ok", data=order_data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])


# PC--订单关闭
@api_goods.route('/pc_goods_order_close', methods=['POST'])
@login_required
@admin_required
def pc_goods_order_close():
    try:
        res = request.get_json()
        admin_id = g.user_id
        Logging.logger.info('request_args:{0}'.format(res))

        params_status, result = DetailParamsCheck.detail_params_check(res)
        if not params_status:
            return jsonify(errno=result[0], errmsg=result[1])

        close_data_service(res, admin_id)
        return jsonify(errno=0, errmsg="ok")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])


# PC--订单的物流信息
@api_goods.route('/pc_express_info', methods=['POST'])
@login_required
@admin_required
def pc_express_info():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        Logging.logger.info('request_args:{0}'.format(res))

        if not isinstance(order_id, int):
            return jsonify(errno=ErrorCode.params_type_error[0], errmsg=ErrorCode.params_type_error[1])

        order = GoodsOrder.query.get(order_id)
        if not order:
            return jsonify(errno=ErrorCode.order_not_exist[0], errmsg=ErrorCode.order_not_exist[1])

        if order.order_status in [1, 2]:
            return jsonify(errno=ErrorCode.order_status_error[0], errmsg=ErrorCode.order_status_error[1])

        express = ExpressInfo.query.filter_by(order_id=order_id).first()
        if express:
            express_dict = query_to_dict(express)
        else:
            express_dict = None

        return jsonify(errno=0, errmsg="ok", data=express_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])



# PC--订单的物流信息
@api_goods.route('/express_info', methods=['POST'])
def express_info():
    try:
        res = request.get_json()
        Logging.logger.info('request_args:{0}'.format(res))
        params_status, result = ExpressParamsCheck.express_params_check(res)
        if not params_status:
            return jsonify(errno=result[0], errmsg=result[1])
        print("---")
        express_dict = express_data_service(res)

        return jsonify(errno=0, errmsg="ok", data=express_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])


# PC退款申请审核
@api_goods.route('/goods_order_refund_check', methods=['POST'])
@login_required
@admin_required
def refund_check():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        admin_id = g.admin_id

        Logging.logger.info('request_args:{0}'.format(res))

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        if order_obj.order_status not in [1, 2]:
            return jsonify(errno=-1, errmsg='当前订单状态不支持该操作')
        admin = Admin.query.get(admin_id)
        refund_person = admin.username

        order_obj.order_status = -1
        order_obj.admin_id = admin_id
        order_obj.refund_person = refund_person
        db.session.add(order_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="ok")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=ErrorCode.Internet_error[0], errmsg=ErrorCode.Internet_error[1])
