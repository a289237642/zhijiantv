# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 2:29 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : db_config.py
# @Software: PyCharm

class DBConfig(object):
    """redis的db配置:
    db=1:用户登陆
    """
    _redis_conf = {
        'host': '101.132.186.25',
        # 'host': '47.100.63.158',
        # 'host': '127.0.0.1',
        'port': 6379,
        'password': '',
    }

    @classmethod
    def get_redis_host(cls):
        return cls._redis_conf.get('host')

    @classmethod
    def get_redis_port(cls):
        return cls._redis_conf.get('port')
