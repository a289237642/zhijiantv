# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 5:01 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : pc_picinfo.py
# @Software: PyCharm
import time, os, requests ,re
from flask import json, request, jsonify, session
from . import pcfileinfo
from app.models import User, VideoType, VideoInfo
from utils.qiniuApi import *
from werkzeug.utils import secure_filename
from utils.utils_info import *
from app import db


# 新建分类
@pcfileinfo.route('/add_class_info', methods=['POST'])
def AddClassInfo():
    try:
        res = request.get_json()
        url = res.get('url')
        title = res.get('title')
        cross_url = res.get('cross_url')
        if not all([url, title,cross_url]):
            return jsonify(errno=-1, errmsg="参数不完整")
        class_info = VideoType.query.filter_by(title=title).first()
        if class_info:
            return jsonify(errno=-1, errmsg="分类已存在")
        obj = VideoType()
        obj.url = url
        obj.title = title
        obj.cross_url = cross_url
        obj.status = 1
        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 新建视频
@pcfileinfo.route('/add_tv_info', methods=['POST'])
def AddTvInfo():
    try:
        res = request.get_json()
        vtype = res.get('vtype')
        title = res.get('title')
        pic_url = res.get('pic_url')
        url = res.get('url')
        play_times = res.get('play_times')
        if not all([vtype, title, pic_url, url, play_times]):
            return jsonify(errno=-1, errmsg="参数不完整")
        tv_info = VideoInfo.query.filter_by(title=title).first()
        if tv_info:
            return jsonify(errno=-1, errmsg="视频名称已存在")
        obj = VideoInfo()
        obj.vtype = vtype
        obj.title = title
        obj.pic_url = pic_url
        obj.url = url
        obj.play_times = play_times
        obj.status = 1
        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频上传
@pcfileinfo.route('/up_sp_oss', methods=['POST'])
def UpSpOss():
    try:
        file = request.files['file']
        key = f"{int(time.time())}{random_str(10)}{file.filename}"
        # basepath = os.path.dirname(__file__)
        basepath = '/root/zhijian_tv_api/zhijian_tv_api'
        upload_path = os.path.join(basepath, 'up_file/', secure_filename(key))
        file.save(upload_path)
        play_times = get_file_times(upload_path)
        info = file_oss(key=key, localfile=upload_path)
        if info['errmsg'] == 0:
            return jsonify(errno=0, errmsg='上传成功', url=info['url'], play_times=play_times)
        else:
            return jsonify(errno=-1, errmsg='网络异常')
    except Exception as e:
        return jsonify(errno=-1, errmsg='抛出异常')


# 图片上传
@pcfileinfo.route('/up_tp_oss', methods=['POST'])
def UpTpOss():
    try:
        file = request.files['file']
        key = f"{int(time.time())}{random_str(10)}{file.filename}"
        # basepath = os.path.dirname(__file__)
        basepath = '/root/zhijian_tv_api/zhijian_tv_api'
        upload_path = os.path.join(basepath, 'up_file/', secure_filename(key))
        file.save(upload_path)
        info = file_oss(key=key, localfile=upload_path)
        if info['errmsg'] == 0:
            return jsonify(errno=0, errmsg='上传成功', url=info['url'])
        else:
            return jsonify(errno=-1, errmsg='网络异常')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 获取oss toke
@pcfileinfo.route('/get_oss_token', methods=['POST'])
def GETOSSTOKEN():
    try:
        res = request.get_json()
        key = res.get('key')
        if not key:
            return jsonify(errno=-1, errmsg="参数不完整")
        key = f"{int(time.time())}{random_str(10)}{key}"
        token = get_oss_token(key=key)
        if token:
            return jsonify(errno=0, errmsg='操作成功', token=token, key=key)
        else:
            return jsonify(errno=-1, errmsg='网络异常')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 获取 文件信息
@pcfileinfo.route('/get_file_info', methods=['POST'])
def GetFileInfo():
    try:
        res = request.get_json()
        key = res.get('key')
        if not key:
            return jsonify(errno=-1, errmsg="参数不完整")
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        urls = f'http://prjkmnaf0.bkt.clouddn.com/{key}?avinfo'
        infos = json.loads(str(requests.get(urls, data={}, headers=headers).content, 'utf-8'))
        play_times = re.sub(r'(^\d+:|\..*)','',str(datetime.timedelta(seconds=float(infos['format']['duration']))))
        if play_times:
            return jsonify(errno=0, errmsg='操作成功', play_times=play_times)
        else:
            return jsonify(errno=-1, errmsg='网络异常')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')
