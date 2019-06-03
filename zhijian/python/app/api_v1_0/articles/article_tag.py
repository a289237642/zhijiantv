# -*- coding:utf-8 -*-
# author: will

from aip import AipNlp
from flask import request, jsonify

from app import mongo_store
from app.models import Article
from config.lib_config import LibConfig
from utils.log_service import Logging
from . import api_article


@api_article.route('/article_tag', methods=['POST'])
def article_tag():
    try:
        res = request.get_json()
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的文章的article_id')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg='参数错误,该文章不存在')

        docs = mongo_store.articles.find({'title': article.title})
        doc = docs[0]
        title = doc.get('title')
        content_ls = doc.get('content')
        text = ''
        for content in content_ls:
            if content.get('text'):
                text += content.get('text')
        print(text)
        # text = text.encode('gbk')
        client = AipNlp(LibConfig.get_baidu_language_app_id(), LibConfig.get_baidu_language_api_key(),
                        LibConfig.get_baidu_language_secret_key())
        result_tag = client.keyword(title, text)
        print(result_tag)
        result_topic = client.topic(title, text)
        print(result_topic)

        return jsonify(errno=0, errmsg="OK", result_topic=result_topic, result_tag=result_tag)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')
