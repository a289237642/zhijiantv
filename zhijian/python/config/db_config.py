# -*- coding:utf-8 -*-
# author: will


class DBConfig(object):
    """redis的db配置:
    db=6:测试商品
    db=7:session
    db=8:商品限制
    db=9:用户openID和ip限制
    """
    _redis_conf = {
        'host': '101.132.186.25',
        # 'host': '47.100.63.158',
        # 'host': '127.0.0.1',
        'port': 6379,
        'password': '',
    }

    # _redis_conf_test = {
    #     # 'host': '47.100.63.158',
    #     'host': '127.0.0.1',
    #     'port': 6379,
    #     'password': '',
    # }

    _mongo_conf = {
        'host': '47.100.63.158',
        'port': 27017,
        'password': '',
    }

    _es_conf = {
        'host': '101.132.69.1',
        'port': 5200,
        'password': '',
    }

    @classmethod
    def get_redis_host(cls):
        return cls._redis_conf.get('host')

    # @classmethod
    # def get_test_redis_host(cls):
    #     return cls._redis_conf_test.get('host')

    @classmethod
    def get_redis_port(cls):
        return cls._redis_conf.get('port')

    # @classmethod
    # def get_test_redis_port(cls):
    #     return cls._redis_conf_test.get('port')

    @classmethod
    def get_mongo_host(cls):
        return cls._mongo_conf.get('host')

    @classmethod
    def get_mongo_port(cls):
        return cls._mongo_conf.get('port')

    @classmethod
    def get_es_host(cls):
        return cls._es_conf.get('host')

    @classmethod
    def get_es_port(cls):
        return cls._es_conf.get('port')

