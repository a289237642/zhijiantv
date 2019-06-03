# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 11:26 AM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : wx_config.py
# @Software: PyCharm

class WxConfig(object):
    _wx_conf = {
        'appid': 'wxe73f0d4f688a4e0b',
        'appsecret': 'edbee0f321e65baf2cba8006d4bb06b3'
    }

    @classmethod
    def get_wx_appid(cls):
        return cls._wx_conf.get('appid')

    @classmethod
    def get_wx_appsecret(cls):
        return cls._wx_conf.get('appsecret')
