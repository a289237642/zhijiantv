# -*- coding:utf-8 -*-
# author: will
import logging

from flask import request, jsonify, g

from app import db, mongo_store
from app.models import Article
from celery_tasks.tasks import get_audio_baidu_test, get_audio_baidu
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required
from libs.xunfei import get_audio_xf
from . import api_article


# 文章转语音
@api_article.route('/get_audio', methods=['POST'])
@login_required
@admin_required
def get_audio():
    try:
        res = request.get_json()
        article_id_list = res.get('article_id_list')
        is_read = res.get('is_read')  # 传入即修改语音状态
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        for article_id in article_id_list:
            try:
                article_id = int(article_id)
            except Exception as e:
                logging.error(e)
                return jsonify(errno=-1, errmsg='传入文章ID错误')

            obj = Article.query.get(article_id)
            if not obj:
                return jsonify(errno=-1, errmsg='该文章不存在')

            # 修改语音状态
            if is_read == 1:
                obj.is_read = 0
                obj.admin_id = admin_id
                db.session.add(obj)
                db.session.commit()
                # return jsonify(errno=0, errmsg="取消音频成功")
            else:
                if obj.mp3_url:
                    # 已经生成过语音,被取消0状态
                    obj.is_read = 1
                    obj.admin_id = admin_id
                    db.session.add(obj)
                    db.session.commit()
                    # return jsonify(errno=0, errmsg="生成音频成功", mp3_url=obj.mp3_url)
                else:
                    # 生成新语音
                    docs = mongo_store.articles.find({'title': obj.title})
                    doc = docs[0]
                    content = doc.get('content')
                    # get_audio_baidu_test.delay(article_id, content)
                    get_audio_baidu.delay(article_id, content)

                    obj.is_read = 1
                    obj.admin_id = admin_id
                    db.session.add(obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="ok")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 讯飞语音
@api_article.route('/get_audio_xunfei', methods=['POST'])
@login_required
@admin_required
def get_audio_xunfei():
    try:
        res = request.get_json()
        data = res.get('data')
        mp3_url = get_audio_xf(data)
        if mp3_url is False:
            return jsonify(errno=-1, errmsg='合成失败')
        else:
            return jsonify(errno=0, errmsg="OK", mp3_url=mp3_url)

    except Exception as e:
        print(e)
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')
