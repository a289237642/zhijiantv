# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import json
from urllib import parse
import requests
# import urlparse

from app import redis_store
from utils.log_service import Logging
from utils.user_service.auth import Token


def get_qr_func(page, scene):
    try:
        obj = Token()
        access_token = obj.get_access_token()
        url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s" % access_token
        page = parse.unquote(page)
        data = {
            "scene": scene,
            "page": page,
            "width": 430,
            "auto_color": False,
            "line_color": {"r": 0, "g": 0, "b": 0},
            "is_hyaline": True  # Ture,透明色, Flase,显示底色
        }
        r = requests.post(url, data=json.dumps(data))
        if not r.content:
            return False
        else:
            try:
                json.loads(r.content)
                redis_store.delete('access_token')
            except Exception as e:
                doc = base64.b64encode(r.content)

                kw = {
                    'imgdata': doc,
                    'filepath': 'gander_goose/dev/test2'
                }
                try:
                    result = requests.post(url='http://api.max-digital.cn/Api/oss/baseUpload', data=kw)
                    result = result.json()
                    oss_url = result.get('oss_file_url')
                    new_oss_url = oss_url.replace('maxpr.oss-cn-shanghai.aliyuncs.com', 'cdn.max-digital.cn')
                    new_oss_url = new_oss_url.replace('http', 'https')
                    Logging.logger.info('oss_url:{0}'.format(new_oss_url))
                    return new_oss_url
                except Exception as e:
                    Logging.logger.error('errmsg:可能是max-api挂了,{0}'.format(e))
                    return False
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return False
