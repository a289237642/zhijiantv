# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 1:01 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : user_info.py
# @Software: PyCharm
import base64, os
from werkzeug.utils import secure_filename
from flask import json, request, jsonify
from utils.qiniuApi import *
from . import wxapi
from app.models import User, VideoInfo, VideoType
from utils.utils_info import *
from pymysql import connect
from urllib import parse
from app import db


# 视频分类列表
@wxapi.route('/video_type_list', methods=['POST'])
def VideoTypeList():
    try:
        res = request.get_json()
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 5))
        if not all([page, pagesize]):
            return jsonify(errno=-1, errmsg="参数不完整")
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 5
        result = VideoType.query.filter(VideoType.status == 1).limit(pagesize).offset(
            (page - 1) * pagesize)
        ids = [x.id for x in result]
        counts = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype.in_(ids)).all()
        nums_list = list()
        for e, m in enumerate(ids):
            dicts = dict()
            nums = 0
            for i in counts:
                if i.vtype == m:
                    nums += 1
            dicts['nums'] = nums
            dicts['ids'] = m
            nums_list.append(dicts)
        info_list = list()
        if result:
            for results in result:
                dicts = dict()
                dicts['id'] = results.id
                dicts['title'] = results.title
                dicts['url'] = results.url
                dicts['times'] = get_time(str(results.update_time))
                for x in nums_list:
                    if x['ids'] == results.id:
                        dicts['nums'] = x['nums']
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频列表页
@wxapi.route('/video_list', methods=['POST'])
def VideoList():
    try:
        res = request.get_json()
        vtype = res.get('vtype')
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        if not all([vtype, page, pagesize]):
            return jsonify(errno=-1, errmsg="参数不完整")
        try:
            page = int(page)
            pagesize = int(pagesize)
            vtype = int(vtype)
        except Exception as e:
            page, pagesize = 1, 10
        result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == vtype).all()
        count = len(result)
        result = result[(page - 1) * pagesize:page * pagesize]
        info_list = list()
        cross_url = VideoType.query.filter(VideoType.id == vtype).first()
        if result:
            for results in result:
                dicts = dict()
                dicts['id'] = results.id
                dicts['vtype'] = results.vtype
                dicts['title'] = results.title
                dicts['summary'] = results.summary
                dicts['url'] = results.url
                dicts['pic_url'] = results.pic_url
                dicts['is_show'] = results.is_show
                dicts['status'] = results.status
                dicts['update_time'] = str(results.update_time)
                dicts['create_time'] = str(results.create_time)
                dicts['play_times'] = str(results.play_times)
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', cross_url=cross_url.cross_url, info_list=info_list, count=count)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 精选list
@wxapi.route('/video_fine_list', methods=['POST'])
def VideoFineList():
    try:
        res = request.get_json()
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        if not all([page, pagesize]):
            return jsonify(errno=-1, errmsg="参数不完整")
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 10
        result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.is_show == 1).all()
        count = len(result)
        result = result[(page - 1) * pagesize:page * pagesize]
        info_list = list()
        if result:
            for results in result:
                dicts = dict()
                dicts['id'] = results.id
                dicts['vtype'] = results.vtype
                dicts['title'] = results.title
                dicts['summary'] = results.summary
                dicts['url'] = results.url
                dicts['pic_url'] = results.pic_url
                dicts['is_show'] = results.is_show
                dicts['update_time'] = str(results.update_time)
                dicts['create_time'] = str(results.create_time)
                dicts['play_times'] = str(results.play_times)
                dicts['status'] = results.status
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', info_list=info_list, count=count)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频详情
@wxapi.route('/video_infos', methods=['POST'])
def VideoInfos():
    try:
        res = request.get_json()
        id = int(res.get('id'))
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoInfo.query.get(id)
        if result:
            video_info = {
                "id": result.id,
                "title": result.title,
                "summary": result.summary,
                "url": result.url,
                "pic_url": result.pic_url,
                "is_show": result.is_show,
                "status": result.status,
                "update_time": str(result.update_time),
                "create_time": str(result.create_time),
                "vtype": result.vtype,
                "play_nums": result.play_nums,
                "play_times": result.play_times
            }
            return jsonify(errno=0, errmsg='查询成功', video_info=video_info)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频推荐列表
@wxapi.route('/recommended_list', methods=['POST'])
def RecommendedList():
    try:
        res = request.get_json()
        id = int(res.get('id'))
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zhijiantv', user='maxpr_mysql',
                       passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # conn = connect(host='127.0.0.1', port=3306,
        #                db='shande', user='root',
        #                passwd='root', charset='utf8')
        cs1 = conn.cursor()
        sql = f"SELECT * FROM tv_video_info WHERE status=1 AND vtype={id} ORDER BY RAND() LIMIT 6"
        cs1.execute(sql)
        info = list(cs1.fetchall())
        cs1.close()
        conn.close()
        l = len(info)
        info_list = list()
        if l > 0:
            for infos in info:
                infos = list(infos)
                dicts = dict()
                dicts['create_time'] = str(infos[0])
                dicts['update_time'] = str(infos[1])
                dicts['admin_id'] = infos[2]
                dicts['id'] = infos[3]
                dicts['vtype'] = infos[4]
                dicts['title'] = infos[5]
                dicts['summary'] = infos[6]
                dicts['url'] = infos[7]
                dicts['pic_url'] = infos[8]
                dicts['play_nums'] = infos[9]
                dicts['play_times'] = infos[10]
                dicts['is_show'] = infos[11]
                dicts['status'] = infos[12]
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', video_info=info_list)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频点击量统计
@wxapi.route('/video_click_amount', methods=['POST'])
def VideoClickAmount():
    try:
        res = request.get_json()
        id = int(res.get('id'))
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoInfo.query.get(id)
        result.play_nums += 1
        db.session.add(result)
        db.session.commit()
        return jsonify(errno=0, errmsg='添加成功')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 生成二维码
@wxapi.route('/create_code', methods=['POST'])
def CreateCode():
    try:
        res = request.get_json()
        page = res.get('page')
        scene = res.get('scene', 'default')
        if not page:
            return jsonify(status="-2", errmsg='参数错误')

        access_token = get_access_token()
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
                return jsonify(errno=0, errmsg='添加成功', new_oss_url=new_oss_url)
            except Exception as e:
                return False
    except Exception as e:
        return jsonify(status="-2", errmsg='qr获取失败')


# wx_test
@wxapi.route('/wx_test', methods=['POST'])
def WxTest():
    data = {
        "day": get_time(str(get_today()))
        # "day": 1
    }
    return jsonify(errno=0, errmsg='查询成功', info_list=data)
