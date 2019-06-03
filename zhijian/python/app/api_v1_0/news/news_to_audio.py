# -*- coding:utf-8 -*-
# author: will
from flask import request, jsonify, g

from celery_tasks.tasks import get_audio_xf_test, get_audio_xf
from app import db, mongo_store
from app.models import NewsData
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required
from . import api_news


# 快讯转语音
@api_news.route('/news_get_audio', methods=['POST'])
@login_required
@admin_required
def get_audio():
    try:
        res = request.get_json()
        news_id_list = res.get('news_id_list')
        is_read = res.get('is_read')  # 传入即修改语音状态
        admin_id = g.user_id
        # admin_id = 6

        Logging.logger.info('request_args:{0}'.format(res))
        for news_id in news_id_list:
            try:
                news_id = int(news_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg='传入快讯ID错误')

            obj = NewsData.query.get(news_id)
            if not obj:
                return jsonify(errno=-1, errmsg='该快讯不存在')

            # 修改语音状态
            if is_read == 1:
                obj.is_read = 0
                obj.admin_id = admin_id
                db.session.add(obj)
                db.session.commit()
                # return jsonify(errno=0, errmsg="取消音频成功")
            else:
                if obj.audio_url:
                    # 已经生成过语音,被取消0状态
                    obj.is_read = 1
                    obj.admin_id = admin_id
                    db.session.add(obj)
                    db.session.commit()
                    # return jsonify(errno=0, errmsg="生成音频成功", mp3_url=obj.mp3_url)
                else:
                    # 生成新语音
                    docs = mongo_store.news.find({'news_id': news_id})
                    doc = docs[0]
                    content = doc.get('content')
                    # get_audio_xf_test.delay(content, news_id)
                    get_audio_xf.delay(content, news_id)
                    obj.is_read = 1
                    obj.admin_id = admin_id
                    db.session.add(obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="ok")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
