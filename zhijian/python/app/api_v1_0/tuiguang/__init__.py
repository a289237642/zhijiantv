# -*- coding:utf-8 -*-
# 创建蓝图对象
from flask import Blueprint

api_spread = Blueprint('api_spread', __name__)

from . import spread_info, spread_data


@api_spread.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
