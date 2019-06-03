# -*- coding:utf-8 -*-
import hashlib

import redis

from config.db_config import DBConfig
from config.keys_config import KeysConfig


class Config(object):
    # 随机的生成secret_key, PC登录权限验证生成token
    SECRET_KEY = KeysConfig.get_secret_key()

    # 更改flask的session位置为Redis
    REDIS_HOST = DBConfig.get_redis_host()
    REDIS_PORT = DBConfig.get_redis_port()


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://maxpr_mysql:COFdjwD*$*m8bd!HtMLP4+Az0eE9m@rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com/zjlivedev'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/shande'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # 更改flask的session位置为Redis
    # REDIS_HOST = DBConfig.get_test_redis_host()
    # REDIS_PORT = DBConfig.get_test_redis_port()

    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀

    SESSION_REDIS = redis.StrictRedis(port=Config.REDIS_PORT, host=Config.REDIS_HOST, db=7)
    PERMANENT_SESSION_LIFETIME = 86400 * 2

    DEBUG = True


class ProductionConfig(Config):
    # 正式版
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://maxpr_mysql:COFdjwD*$*m8bd!HtMLP4+Az0eE9m@rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com/zjlivenew'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/shande'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # 更改flask的session位置为Redis
    # REDIS_HOST = DBConfig.get_redis_host()
    # REDIS_PORT = DBConfig.get_redis_port()

    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀

    SESSION_REDIS = redis.StrictRedis(port=Config.REDIS_PORT, host=Config.REDIS_HOST, db=7)
    PERMANENT_SESSION_LIFETIME = 86400 * 2

    DEBUG = False
