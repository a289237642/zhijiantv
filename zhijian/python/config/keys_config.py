# -*- coding:utf-8 -*-
# author: will
import hashlib


class KeysConfig(object):

    # 随机的生成secret_key, PC登录权限验证生成token
    _SECRET_KEY = '3HASoi6Lte9fiLUgQmP0fvFSCU7qG2Ke'
    # _SECRET_KEY = 'a502f2867f2cd6fee7cbf684bc1c2e1c'

    # 用于小程序生成验证token
    _MY_SECRET = 'smartdata'

    # 集成日志sentry
    _sentry_dsn = "https://12c5cec9563f4adcbeb7c5a175d882f6@sentry.io/1366557"

    # 随机的生成secret_key,神箭手验证使用
    res = hashlib.md5()
    res.update(("1qaz2wsx" + 'shenjianshou.cn').encode('utf-8'))
    _secret_key = res.hexdigest()

    @classmethod
    def get_secret_key(cls):
        return cls._SECRET_KEY

    @classmethod
    def get_my_secret(cls):
        return cls._MY_SECRET

    @classmethod
    def get_sentry_dsn(cls):
        return cls._sentry_dsn

    @classmethod
    def get_shenjianshou_secret_key(cls):
        return cls._secret_key
