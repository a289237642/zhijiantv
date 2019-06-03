# -*- coding:utf-8 -*-
# author: will
import base64
import datetime

from app import db
from app.models import GoodsOrder, Goods, GoodsImage, UserAddress, ExpressInfo, User
from common.error_code import ErrorCode
from utils.log_service import Logging
from utils.to_dict import query_to_dict


def ls_data_service(res):
    """PC订单列表"""
    order_status = res.get('order_status')
    page = res.get('page')
    pagesize = res.get('pagesize')

    try:
        if order_status in [1, 2, 3, 4, 5]:
            orders = GoodsOrder.query.filter_by(order_status=order_status).order_by(GoodsOrder.create_time.desc()).all()
        else:
            orders = GoodsOrder.query.order_by(GoodsOrder.create_time.desc()).all()

        count = len(orders)
        orders = orders[(page - 1) * pagesize:page * pagesize]
        order_list = list()
        for order in orders:
            order_dict = query_to_dict(order)

            goods_id = order.goods_id
            goods_obj = Goods.query.get(goods_id)
            order_dict['goods_name'] = goods_obj.name

            img_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_id, GoodsImage.is_min == 1).first()
            order_dict['img_url'] = img_obj.img_url

            address_id = order.address_id
            address = UserAddress.query.get(address_id)
            address_dict = query_to_dict(address)

            order_dict['address_data'] = address_dict
            order_list.append(order_dict)
        return True, (order_list, count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return False, ErrorCode.Internet_error


def detail_data_service(res):
    """PC订单详情"""
    order_id = res.get('order_id')

    order_data = dict()
    order = GoodsOrder.query.get(order_id)
    user_id = order.user_id
    user = User.query.get(user_id)
    user_dict = dict(avatar_url=user.avatar_url,
                     nick_name=base64.b64decode(user.nick_nameemoj))
    order_data['user_data'] = user_dict
    order_dict = query_to_dict(order)
    order_data['order_data'] = order_dict

    goods_id = order.goods_id
    goods = Goods.query.get(goods_id)
    goods_dict = query_to_dict(goods)
    order_data['goods_data'] = goods_dict

    img_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_id, GoodsImage.is_min == 1).first()
    goods_dict['min_pic'] = img_obj.img_url

    address_id = order.address_id
    address = UserAddress.query.get(address_id)
    address_dict = query_to_dict(address)
    order_data['address_data'] = address_dict

    express = ExpressInfo.query.filter_by(order_id=order_id).first()
    if express:
        express_dict = query_to_dict(express)
        order_data['express_data'] = express_dict

    return order_data


def close_data_service(res, admin_id):
    """PC关闭订单"""
    order_id = res.get('order_id')
    order = GoodsOrder.query.get(order_id)
    order_status = order.order_status

    order.order_status = 5
    order.close_time = datetime.datetime.now()
    order.admin_id = admin_id
    db.session.add(order)
    db.session.commit()
    Logging.logger.info('ID为:{0}的订单被管理员:{1}由状态{2}改为关闭状态'.format(order_id, admin_id, order_status))


def express_data_service(res):
    """订单物流信息"""
    order_id = res.get('order_id')
    express = ExpressInfo.query.filter_by(order_id=order_id).first()
    print(express)
    if express:
        print(1111)
        express_dict = query_to_dict(express)
        return express_dict
