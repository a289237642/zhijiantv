# -*- coding:utf-8 -*-

import time
import requests

from app import redis_store
from config.lib_config import LibConfig


class AccessToken(object):
    __access_token = {
        'access_token': '',
        'update_time': time.time(),
        'expires_in': 7200
    }

    @classmethod
    def get_access_token(cls):
        # 1. 是否存在  2. 是否过期 3. 返回token
        if not cls.__access_token.get('access_token') or \
                (time.time() - cls.__access_token.get('update_time') > cls.__access_token.get('expires_in')):

            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                LibConfig.get_zjlive_appid(), LibConfig.get_zjlive_appsecret())

            resp_data = requests.get(url=url)

            resp_dict = resp_data.json()

            if 'errcode' in resp_dict:
                raise Exception(resp_dict.get('errmsg'))

            cls.__access_token['access_token'] = resp_dict.get('access_token')
            cls.__access_token['expires_in'] = resp_dict.get('expires_in')
            cls.__access_token['update_time'] = time.time()

        return cls.__access_token.get('access_token')


class Token(object):
    __access_token = {
        'access_token': '',
        'update_time': time.time(),
        'expires_in': 7200
    }

    @classmethod
    def get_access_token(cls):

        access_token = redis_store.get('access_token')
        if not access_token:

            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                LibConfig.get_zjlive_appid(), LibConfig.get_zjlive_appsecret())

            resp_data = requests.get(url=url)

            resp_dict = resp_data.json()

            if 'errcode' in resp_dict:
                raise Exception(resp_dict.get('errmsg'))

            access_token = resp_dict.get('access_token')

            redis_store.set('access_token', access_token, ex=resp_dict.get('expires_in') - 10)
            return access_token
        else:
            return access_token


class Openid(object):
    @staticmethod
    def get_openid(code):
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={LibConfig.get_zjlive_appid()}&secret={LibConfig.get_zjlive_appsecret()}&js_code={code}&grant_type=authorization_code"
        # url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' \
        #       % (LibConfig.get_zjlive_appid(), LibConfig.get_zjlive_appsecret(), code)
        resp_data = requests.get(url=url)
        resp_dict = resp_data.json()
        return resp_dict
