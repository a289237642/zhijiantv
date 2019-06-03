# -*- coding:utf-8 -*-
# 创建蓝图对象
from flask import Blueprint

api_user = Blueprint('api_user', __name__)

import app.api_v1_0.users.lucky_coins
import app.api_v1_0.users.send_message
import app.api_v1_0.users.sales_info
import app.api_v1_0.users.user_address
import app.api_v1_0.users.user_info
import app.api_v1_0.users.pay_user


@api_user.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
