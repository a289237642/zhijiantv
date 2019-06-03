# -*- coding:utf-8 -*-
import base64
import json
import random
import time

import requests


# url上传
def storage_by_url(file_url):
    url = 'http://api.max-digital.cn/Api/oss/uploadByUrl'

    file_path = 'miniprogram/zjlive/download/image'
    params = {
        'fileurl': file_url,
        'filepath': file_path,
    }
    data = requests.post(url=url, data=params)

    data = data.json()
    # print 123, json.dumps(data, ensure_ascii=False)

    if data.get('code') == 'OK':
        oss_url = data.get('oss_file_url')
        oss_url = oss_url.replace('maxpr.oss-cn-shanghai.aliyuncs.com', 'cdn.max-digital.cn')
        oss_url = oss_url.replace('http', 'https')
        return oss_url
    else:
        # 表示上传失败
        return False


# base64上传
def storage_by_bs64(file_data, type):
    url = 'http://api.max-digital.cn/Api/oss/baseUpload'
    file_path = 'miniprogram/zjlive/download/image'
    params = {
        'imgdata': file_data,
        'filepath': file_path,
        'type': type
    }
    data = requests.post(url=url, data=params)
    data = data.json()
    print((123, json.dumps(data, ensure_ascii=False)))

    if data.get('code') == 'OK':
        oss_url = data.get('oss_file_url')
        oss_url = oss_url.replace('maxpr.oss-cn-shanghai.aliyuncs.com', 'cdn.max-digital.cn')
        oss_url = oss_url.replace('http', 'https')
        return oss_url
    else:
        # 表示上传失败
        return False


# 文件上传
def storage_by_file(image_file):
    try:
        num = int(time.time() * 1000)
        image_file.save('/www/zhijian_live_miniprogram/storage/image/%s.jpg' % num)
        url = 'https://zj-live.max-digital.cn/storage/image/' + str(num) + '.' + 'jpg'
        oss_url = storage_by_url(url)
        return oss_url
    except Exception as e:
        return False


# base64图片保存在本地
def base_img(imagedata):
    try:
        imagedata = imagedata.split(',')
        imagedata = base64.b64decode(imagedata)
        with open('1.jpg', 'wb') as f:
            f.write(imagedata)

        return True
    except Exception as e:
        return False

