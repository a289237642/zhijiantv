# -*- coding:utf-8 -*-
# author: will
import base64
import hashlib
import json
import logging
import os
import time

import oss2
import requests
from pymysql import connect
from aip import AipSpeech
from celery import Celery
from pydub import AudioSegment

from config.lib_config import LibConfig
from utils.is_zh import remove_emoji

my_celery = Celery(broker='redis://localhost:6379/2', backend='redis://localhost:6379/3')


# celery -A celery_tasks.tasks worker -l info >> /tmp/celery_log/log 2>&1
# 任务1,正式
@my_celery.task
def get_audio_baidu(article_id, content):
    APP_ID = LibConfig.get_baidu_audio_app_id()
    API_KEY = LibConfig.get_baidu_audio_api_key()
    SECRET_KEY = LibConfig.get_baidu_audio_secret_key()

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 生成新语音
    # num = random.randint(100000, 999999)
    # mp3_url = 'https://zj-live-dev.max-digital.cn/storage/media/result/%s.mp3' % num
    num = int(time.time() * 1000)
    mp3_url = 'https://cdn.max-digital.cn/miniprogram/zjlive/download/mp3/%s.mp3' % str(num)

    # with open('../storage/media/article/%s.mp3' % num, 'ab+') as f:
    with open('/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num, 'ab+') as f:
        for res in content:
            if res.get('text'):
                tex = res.get('text')
                # 移除表情特殊符号
                bul = remove_emoji(tex)
                if bul:
                    result = client.synthesis(bul, 'zh', 1, {
                        'vol': 5,  # 音量，取值0-15，默认为5中音量
                        'spd': 5,  # 语速，取值0-9，默认为5中语速
                        'pit': 5,  # 音调，取值0-9，默认为5中语调
                        'per': 3,  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
                    })
                    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
                    if not isinstance(result, dict):
                        f.write(result)
                    else:
                        logging.error(result)

    # 合成语音(加郭老师音频)
    basic_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/basic/123456.mp3'
    article_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num
    result_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/result/%s.mp3' % num

    # 加载MP3文件
    print('开始加载MP3文件')
    song1 = AudioSegment.from_mp3(basic_mp3_path)
    song2 = AudioSegment.from_mp3(article_mp3_path)
    print('加载成功')

    # 拼接两个音频文件
    song = song1 + song2
    t = song.duration_seconds  # 音频时长/秒
    t = int(t)
    print(t)

    # 导出音频文件
    song.export(result_mp3_path, format="mp3")  # 导出为MP3格式

    # 存入mysql
    conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                   db='zjlivenew', user='maxpr_mysql',
                   passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    sql = 'UPDATE zj_article_info SET is_read="%s",mp3_url="%s" where id="%s"' % (1, mp3_url, article_id)
    cs1.execute(sql)
    print('执行了sql:', sql)

    conn.commit()
    cs1.close()
    conn.close()

    # 上传服务器语音文件到os,删除服务器本地文件
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIx8UTwV9vqIJS')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LeQIFKJrp6fQQp0sAcmRIvh0IJxJZ9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'maxpr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')

    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    ossname = "miniprogram/zjlive/download/mp3/" + str(num) + ".mp3"
    print('oss_name:', ossname)
    bdname = "/www/celery_tasks/zhijian_live_miniprogram/storage/media/result/" + str(num) + ".mp3"
    bucket.put_object_from_file(ossname, bdname)
    os.remove(bdname)
    print('bdname:', bdname)


# 任务2,测试
@my_celery.task
def get_audio_baidu_test(article_id, content):
    APP_ID = LibConfig.get_baidu_audio_app_id()
    API_KEY = LibConfig.get_baidu_audio_api_key()
    SECRET_KEY = LibConfig.get_baidu_audio_secret_key()

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 生成新语音
    # num = random.randint(100000, 999999)
    # mp3_url = 'https://zj-live-dev.max-digital.cn/storage/media/result/%s.mp3' % num
    num = int(time.time() * 1000)
    mp3_url = 'https://cdn.max-digital.cn/miniprogram/zjlive/download/mp3/%s.mp3' % str(num)

    # with open('../storage/media/article/%s.mp3' % num, 'ab+') as f:
    with open('/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num, 'ab+') as f:
        for res in content:
            if res.get('text'):
                tex = res.get('text')
                # 移除表情特殊符号
                bul = remove_emoji(tex)
                if bul:
                    print(bul)
                    result = client.synthesis(bul, 'zh', 1, {
                        'vol': 5,  # 音量，取值0-15，默认为5中音量
                        'spd': 5,  # 语速，取值0-9，默认为5中语速
                        'pit': 5,  # 音调，取值0-9，默认为5中语调
                        'per': 3,  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
                    })
                    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
                    if not isinstance(result, dict):
                        f.write(result)
                    else:
                        print(result)
                        logging.error(result)

    # 合成语音(加郭老师音频)
    basic_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/basic/123456.mp3'
    article_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num
    result_mp3_path = '/www/celery_tasks/zhijian_live_miniprogram/storage/media/result/%s.mp3' % num
    # basic_mp3_path = '../storage/media/basic/123456.mp3'
    # article_mp3_path = '../storage/media/article/%s.mp3' % num
    # result_mp3_path = '../storage/media/result/%s.mp3' % num

    # 加载MP3文件
    song1 = AudioSegment.from_mp3(basic_mp3_path)
    song2 = AudioSegment.from_mp3(article_mp3_path)

    # 拼接两个音频文件
    song = song1 + song2
    t = song.duration_seconds  # 音频时长/秒
    t = int(t)
    print(t)

    # 导出音频文件
    song.export(result_mp3_path, format="mp3")  # 导出为MP3格式

    conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                   db='zjlive', user='maxpr_mysql',
                   passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    sql = 'UPDATE zj_article_info SET is_read="%s",mp3_url="%s" where id="%s"' % (1, mp3_url, article_id)
    cs1.execute(sql)
    print('执行了sql:', sql)

    conn.commit()
    cs1.close()
    conn.close()

    # 上传服务器语音文件到os,删除服务器本地文件
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIx8UTwV9vqIJS')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LeQIFKJrp6fQQp0sAcmRIvh0IJxJZ9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'maxpr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')

    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    ossname = "miniprogram/zjlive/download/mp3/" + str(num) + ".mp3"
    print('oss_name:', ossname)
    bdname = "/www/celery_tasks/zhijian_live_miniprogram/storage/media/result/" + str(num) + ".mp3"
    bucket.put_object_from_file(ossname, bdname)
    os.remove(bdname)
    print('bdname:', bdname)


# 任务3,上传音频
@my_celery.task
def upload_file(filename):
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIx8UTwV9vqIJS')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LeQIFKJrp6fQQp0sAcmRIvh0IJxJZ9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'maxpr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'cdn.max-digital.cn')

    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    ossname = "miniprogram/zjlive/download/mp3/" + filename
    print('oss_name:', ossname)
    bdname = "/www/celery_tasks/zhijian_live_miniprogram/storage/media/lesson/" + filename
    # bdname = '/Users/will/Desktop/workspace/zhijian_live/storage/media/lesson/' + filename
    bucket.put_object_from_file(ossname, bdname)
    # res = bucket.put_object(ossname, data)
    os.remove(bdname)
    print('bdname:', bdname)


# 任务4,讯飞转音频--测试
@my_celery.task
def get_audio_xf_test(content, news_id):
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

    num = int(time.time() * 1000)
    mp3_url = 'https://cdn.max-digital.cn/miniprogram/zjlive/download/mp3/%s.mp3' % str(num)

    # with open('../storage/media/%s.mp3' % num, 'ab+') as f:
    with open('/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num, 'ab+') as f:

        for res in content:
            if res.get('text'):
                r = requests.post(URL, headers=header, data=res)
                contentType = r.headers['Content-Type']
                if contentType == "audio/mpeg":
                    f.write(r.content)
                    print("success")
                else:
                    print(r.text)
                    logging.error(r.text)
                    return False

    conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                   db='zjlive', user='maxpr_mysql',
                   passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    sql = 'UPDATE zj_news_info SET is_read="%s",audio_url="%s" where id="%s"' % (1, mp3_url, news_id)
    cs1.execute(sql)
    print('执行了sql:', sql)

    conn.commit()
    cs1.close()
    conn.close()

    # 上传服务器语音文件到os,删除服务器本地文件
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIx8UTwV9vqIJS')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LeQIFKJrp6fQQp0sAcmRIvh0IJxJZ9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'maxpr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')

    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    ossname = "miniprogram/zjlive/download/mp3/" + str(num) + ".mp3"
    print('oss_name:', ossname)
    bdname = "/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/" + str(num) + ".mp3"
    bucket.put_object_from_file(ossname, bdname)
    os.remove(bdname)
    print('bdname:', bdname)


# 任务5,讯飞转音频--正式
@my_celery.task
def get_audio_xf(content, news_id):
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

    num = int(time.time() * 1000)
    mp3_url = 'https://cdn.max-digital.cn/miniprogram/zjlive/download/mp3/%s.mp3' % str(num)

    # with open('../storage/media/%s.mp3' % num, 'ab+') as f:
    with open('/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/%s.mp3' % num, 'ab+') as f:

        for res in content:
            if res.get('text'):
                r = requests.post(URL, headers=header, data=res)
                contentType = r.headers['Content-Type']
                if contentType == "audio/mpeg":
                    f.write(r.content)
                    print("success")
                else:
                    print(r.text)
                    logging.error(r.text)
                    return False

    conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                   db='zjlivenew', user='maxpr_mysql',
                   passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    sql = 'UPDATE zj_news_info SET is_read="%s",audio_url="%s" where id="%s"' % (1, mp3_url, news_id)
    cs1.execute(sql)
    print('执行了sql:', sql)

    conn.commit()
    cs1.close()
    conn.close()

    # 上传服务器语音文件到os,删除服务器本地文件
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIx8UTwV9vqIJS')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LeQIFKJrp6fQQp0sAcmRIvh0IJxJZ9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'maxpr')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')

    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    ossname = "miniprogram/zjlive/download/mp3/" + str(num) + ".mp3"
    print('oss_name:', ossname)
    bdname = "/www/celery_tasks/zhijian_live_miniprogram/storage/media/article/" + str(num) + ".mp3"
    # bdname = "../storage/media/" + str(num) + ".mp3"
    bucket.put_object_from_file(ossname, bdname)
    os.remove(bdname)
    print('bdname:', bdname)
