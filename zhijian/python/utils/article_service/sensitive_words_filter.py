# -*- coding:utf-8 -*-
# author: will
import json

import requests

from utils.log_service import Logging
from utils.redis_service.Redis_Client import RedisClient
from utils.user_service.auth import Token


class SensitiveFilter(object):
    def __init__(self):
        access_token = Token().get_access_token()
        self.content_check_url = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token=%s" % access_token
        self.img_check_url = "https://api.weixin.qq.com/wxa/img_sec_check?access_token=%s" % access_token

    def content_check(self, content):
        Logging.logger.info('小程序违规文字检测')
        # content = json.dumps(content)
        res = requests.post(url=self.content_check_url, data=content)
        print(res.text)
        return res.text

    def img_check(self, data):
        res = requests.post(url=self.img_check_url, data=data)
        print(res)
        return res
