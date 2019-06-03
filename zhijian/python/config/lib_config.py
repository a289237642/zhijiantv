# -*- coding:utf-8 -*-
# author: will
import hashlib


class LibConfig(object):
    # 智见小程序
    _zjlive_config = {
        'appid': 'wx8068c95c08b3b464',
        # 'appsecret': '684fb42ed1fb9e2fd7f2a5855cbf0e5c'
        'appsecret': 'a502f2867f2cd6fee7cbf684bc1c2e1c'
    }

    # 百度语音实例
    _baidu_audio_config = {
        'secret_key': '3HASoi6Lte9fiLUgQmP0fvFSCU7qG2Ke',
        'api_key': 'MgIVWMwpcSOh9rBQgmWihguA',
        'app_id': '11754282'
    }

    # 百度自然语言处理实例
    _baidu_language_config = {
        'secret_key': 'WGA4yePAUdnnqURyRld5LfbSZiiAvrZx',
        'api_key': 'guOvg9dfPRK0elElizWZz7ja',
        'app_id': '15282674'
    }

    # 讯飞语音实例
    _xunfei_config = {
        'api_key': '9371e0f7a97333f7859b75bf5c5385e7',
        'app_id': '5b90def2'
    }

    @classmethod
    def get_zjlive_appid(cls):
        return cls._zjlive_config.get('appid')

    @classmethod
    def get_zjlive_appsecret(cls):
        return cls._zjlive_config.get('appsecret')

    @classmethod
    def get_baidu_audio_secret_key(cls):
        return cls._baidu_audio_config.get('secret_key')

    @classmethod
    def get_baidu_audio_api_key(cls):
        return cls._baidu_audio_config.get('api_key')

    @classmethod
    def get_baidu_audio_app_id(cls):
        return cls._baidu_audio_config.get('app_id')

    @classmethod
    def get_baidu_language_secret_key(cls):
        return cls._baidu_language_config.get('secret_key')

    @classmethod
    def get_baidu_language_api_key(cls):
        return cls._baidu_language_config.get('api_key')

    @classmethod
    def get_baidu_language_app_id(cls):
        return cls._baidu_language_config.get('app_id')

    @classmethod
    def get_xunfei_api_key(cls):
        return cls._xunfei_config.get('api_key')

    @classmethod
    def get_xunfei_app_id(cls):
        return cls._xunfei_config.get('app_id')
