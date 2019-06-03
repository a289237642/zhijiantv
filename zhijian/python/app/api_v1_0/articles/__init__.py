# -*- coding:utf-8 -*-
# author: will

# 创建蓝图对象
from flask import Blueprint

api_article = Blueprint('api_article', __name__)
import app.api_v1_0.articles.article_info
import app.api_v1_0.articles.article_to_audio
import app.api_v1_0.articles.article_tag
import app.api_v1_0.articles.article_coins
import app.api_v1_0.articles.article_keyword_filter
import app.api_v1_0.articles.wechat_name_info


@api_article.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
