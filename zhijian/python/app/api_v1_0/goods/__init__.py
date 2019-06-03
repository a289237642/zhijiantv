# -*- coding:utf-8 -*-
# author: will

# 创建蓝图对象
from flask import Blueprint

api_goods = Blueprint('api_goods', __name__)

from . import goods_info, goods_order, pc_goods_order


@api_goods.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
