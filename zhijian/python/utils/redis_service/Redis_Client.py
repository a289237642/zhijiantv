# -*- coding:utf-8 -*-
# author: will
import redis

from config.db_config import DBConfig


class RedisClient(object):

    __redis_cli = redis.StrictRedis(host=DBConfig.get_redis_host(), port=DBConfig.get_redis_port(), db=9)

    @classmethod
    def create_redis_cli(cls):
        return cls.__redis_cli
