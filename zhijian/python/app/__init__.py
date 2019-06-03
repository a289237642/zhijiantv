# -*- coding:utf-8 -*-
import logging
import os

import redis
from elasticsearch import Elasticsearch
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

from config.db_config import DBConfig
from utils.log_service import Logging

db = SQLAlchemy()

redis_store = None
mongo_store = None
es_store = None

# 日志设置
root_path = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(root_path, 'logs', 'zj.log')  # 正式日志
# log_file_path = os.path.join(root_path, 'logs', 'zj_test.log')  # 测试日志
Logging.addTimedRotatingFileHandler(filename=log_file_path, when='W0', interval=1, backupCount=5)
Logging.logger.setLevel(logging.DEBUG)


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_name)

    db.init_app(app)

    global redis_store, mongo_store, es_store

    redis_store = redis.StrictRedis(host=DBConfig.get_redis_host(), port=DBConfig.get_redis_port(), db=8)

    mg_client = MongoClient(host=DBConfig.get_mongo_host(), port=DBConfig.get_mongo_port(), connect=False)
    # 正式
    mongo_store = mg_client.wechat
    # 测试
    # mongo_store = mg_client.will

    es_store = Elasticsearch(hosts=[DBConfig.get_es_host()], port=DBConfig.get_es_port())

    Session(app)

    # 蓝图注册
    from app.api_v1_0.users import api_user
    from app.api_v1_0.articles import api_article
    from app.api_v1_0.admins import api_admin
    from app.api_v1_0.activities import api_activity
    from app.api_v1_0.banners import api_banner
    from app.api_v1_0.tops import api_top
    from app.api_v1_0.lessons import api_lesson
    from app.api_v1_0.orders import api_order
    from app.api_v1_0.news import api_news
    from app.api_v1_0.goods import api_goods
    from app.api_v1_0.tuiguang import api_spread

    app.register_blueprint(api_user, url_prefix='/api/v1_0')
    app.register_blueprint(api_article, url_prefix='/api/v1_0')
    app.register_blueprint(api_admin, url_prefix='/api/v1_0')
    app.register_blueprint(api_activity, url_prefix='/api/v1_0')
    app.register_blueprint(api_banner, url_prefix='/api/v1_0')
    app.register_blueprint(api_top, url_prefix='/api/v1_0')
    app.register_blueprint(api_lesson, url_prefix='/api/v1_0')
    app.register_blueprint(api_order, url_prefix='/api/v1_0')
    app.register_blueprint(api_news, url_prefix='/api/v1_0')
    app.register_blueprint(api_goods, url_prefix='/api/v1_0')
    app.register_blueprint(api_spread, url_prefix='/api/v1_0')

    return app, db
