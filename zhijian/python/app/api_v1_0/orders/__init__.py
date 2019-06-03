# -*- coding:utf-8 -*-
# author: will
from flask import Blueprint

api_order = Blueprint('api_order', __name__)

from . import order_info


@api_order.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
