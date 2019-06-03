# -*- coding:utf-8 -*-
# author: will
from flask import Blueprint

api_news = Blueprint('api_news', __name__)

from . import news_info, news_to_audio


@api_news.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
