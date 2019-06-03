# -*- coding:utf-8 -*-
# 创建蓝图对象
from flask import Blueprint

api_admin = Blueprint('api_admin', __name__)

from . import admin_info


@api_admin.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
