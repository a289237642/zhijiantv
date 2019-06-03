# -*- coding:utf-8 -*-
# author: will

# 创建蓝图对象
from flask import Blueprint

api_activity = Blueprint('api_activity', __name__)

import app.api_v1_0.activities.activity_info


@api_activity.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
