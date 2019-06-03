# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 11:05 AM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : __init__.py.py
# @Software: PyCharm
import os
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config.db_config import DBConfig
from flask_cors import CORS

db = SQLAlchemy()
redis_store = None


class Config(object):
    # 更改flask的session位置为Redis
    REDIS_HOST = DBConfig.get_redis_host()
    REDIS_PORT = DBConfig.get_redis_port()


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With,token,application/octet-stream'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return resp


def create_app():
    app = Flask(__name__)
    app.after_request(after_request)
    # 创建连接数据的URI
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/shande'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maxpr_mysql:COFdjwD*$*m8bd!HtMLP4+Az0eE9m@rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com/zhijiantv'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # sessino 相关设置
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SECRET_KEY'] = os.urandom(24)  # 做加密用的，加密一般是加密算法或者加盐
    app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀
    app.config['SESSION_REDIS'] = redis.StrictRedis(port=Config.REDIS_PORT, host=Config.REDIS_HOST, db=1)
    # app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 2
    app.config['PERMANENT_SESSION_LIFETIME'] = 60
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)
    Session(app)
    CORS(app)

    # 蓝图构建
    from app.Tvzhijian.wxapi import wxapi
    from app.Tvzhijian.pcadmin import pcadmin
    from app.Tvzhijian.pcfileinfo import pcfileinfo
    from app.Tvzhijian.pcvideos import api_video
    # =======================================================
    app.register_blueprint(wxapi, url_prefix='/api/tv1_0')
    app.register_blueprint(pcadmin, url_prefix='/api/tv1_0')
    app.register_blueprint(pcfileinfo, url_prefix='/api/tv1_0')
    app.register_blueprint(api_video, url_prefix='/api/tv1_0')
    return app, db

