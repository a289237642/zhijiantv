# -*- coding:utf-8 -*-
# author: will

# 创建蓝图对象
from flask import Blueprint

api_banner = Blueprint('api_banner', __name__)

from . import banner_info, poster_info


@api_banner.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
