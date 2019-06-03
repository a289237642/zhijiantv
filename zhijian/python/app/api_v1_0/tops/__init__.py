# -*- coding:utf-8 -*-
# author: will

# 创建蓝图对象
from flask import Blueprint

api_top = Blueprint('api_top', __name__)

from . import top_info


@api_top.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
