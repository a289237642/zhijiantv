# -*- coding:utf-8 -*-
# author: will
import base64
import hashlib
import json
import logging
import random
import time

import requests

from config.lib_config import LibConfig


def get_audio_xf(data):
    try:
        URL = "http://api.xfyun.cn/v1/service/v1/tts"

        param = {
            "auf": "audio/L16;rate=16000",
            "aue": "lame",
            "voice_name": "xiaoyan",
            "speed": "50",
            "volume": "50",
            "pitch": "50",
            "engine_type": "intp65",
            "text_type": "text"
        }

        curTime = str(int(time.time()))
        param = json.dumps(param)
        paramBase64 = base64.b64encode(param)
        m2 = hashlib.md5()
        m2.update(LibConfig.get_xunfei_api_key() + curTime + paramBase64)
        checkSum = m2.hexdigest()
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': LibConfig.get_xunfei_app_id(),
            'X-CheckSum': checkSum,
            'X-Real-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }

        num = random.randint(100000, 999999)
        with open('../storage/media/%s.mp3' % num, 'ab+') as f:
            # for res in data:
            # text = data.get('text')
            r = requests.post(URL,headers=header,data={'text':data})
            contentType = r.headers['Content-Type']
            if contentType == "audio/mpeg":
                f.write(r.content)
                print("success")
            else:
                print(r.text)
                logging.error(r.text)
                return False

        mp3_url = 'https://zj-live-dev.max-digital.cn/storage/media/%s.mp3' % num
        return mp3_url

    except Exception as e:
        print(e)
        return False
