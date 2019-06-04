# @File    : __init__.py.py
# @Software: PyCharm
import time
from flask import json, request, jsonify
from app.Tvzhijian.pcvideos import api_video
from app import db
from app.models import VideoInfo, VideoType


def VideoQuery(result):
    info_list = []
    if result:
        for results in result:
            dicts = {}
            dicts['id'] = results.id
            dicts['title'] = results.title
            dicts['play_nums'] = results.play_nums
            dicts['create_time'] = str(results.create_time)
            dicts['pic_url'] = results.pic_url
            dicts['is_show'] = results.is_show
            info_list.append(dicts)
    return info_list


# 视频分类1
@api_video.route('/type_list', methods=['POST'])
def TypeList():
    try:
        res = request.get_json()
        result = VideoType.query.filter(VideoType.status == 1).all()
        sumNum = VideoType.query.filter(VideoType.status == 1).count()
        info_list = [{'id': 0, 'title': '全部', 'url': '0000'}]
        if result:
            for results in result:
                num = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == results.id).count()
                dicts = {}
                dicts['id'] = results.id
                dicts['title'] = results.title
                dicts['url'] = results.url
                dicts['create_time'] = str(results.create_time)
                dicts['num'] = num
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', info_list=info_list, sumNum=sumNum)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频分类2
@api_video.route('/type_info', methods=['POST'])
def TypeInfo():
    try:
        res = request.get_json()
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 10
        result = VideoType.query.filter(VideoType.status == 1).limit(pagesize).offset((page - 1) * pagesize)
        sumNum = VideoType.query.filter(VideoType.status == 1).count()
        info_list = []
        if result:
            for results in result:
                num = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == results.id).count()
                dicts = {}
                dicts['id'] = results.id
                dicts['title'] = results.title
                dicts['url'] = results.url
                dicts['create_time'] = str(results.create_time)
                dicts['num'] = num
                info_list.append(dicts)
        return jsonify(errno=0, errmsg='查询成功', info_list=info_list, sumNum=sumNum)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频分类删除
@api_video.route('/type_delete', methods=['POST'])
def TypeDelete():
    try:
        res = request.get_json()
        id = res.get('id')
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoType.query.filter(VideoType.status == 1, VideoType.id == id).first()
        video = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == id).all()
        if video:
            return jsonify(errno=-1, errmsg='该分类下有视频，无法删除')
        result.status = 0
        db.session.add(result)
        db.session.commit()
        return jsonify(errno=0, errmsg='删除成功')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频分类修改
@api_video.route('/type_update', methods=['POST'])
def TypeUpdate():
    try:
        res = request.get_json()
        id = res.get('id')
        title = res.get('title')
        url = res.get('url')
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoType.query.filter(VideoType.status == 1, VideoType.id == id).first()

        result.title = title
        result.url = url
        db.session.add(result)
        db.session.commit()
        return jsonify(errno=0, errmsg='修改成功')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 视频列表页
@api_video.route('/video_list_info', methods=['POST'])
def VideoListInfo():
    try:
        res = request.get_json()
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 10
        result = VideoInfo.query.filter(VideoInfo.status == 1).limit(pagesize).offset((page - 1) * pagesize)
        vnum = VideoInfo.query.filter(VideoInfo.status == 1).count()
        info_list = VideoQuery(result)
        return jsonify(errno=0, errmsg='查询成功', info_list=info_list, vnum=vnum)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 修改视频信息
@api_video.route('/video_update_info', methods=['POST'])
def VideoUpdate():
    try:
        res = request.get_json()
        id = res.get('id')
        title = res.get('title')
        summary = res.get('summary')
        url = res.get('url')
        pic_url = res.get('pic_url')
        play_nums = res.get('play_nums')
        vtype = res.get('vtype')
        is_show = res.get('is_show')
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.id == id).first()
        result.title = title
        result.summary = summary
        result.url = url
        result.pic_url = pic_url
        result.play_nums = play_nums
        result.vtype = vtype
        result.is_show = is_show
        db.session.add(result)
        db.session.commit()
        return jsonify(errno=0, errmsg='修改成功')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 删除视频
@api_video.route('/video_delete_info', methods=['POST'])
def VideoDelete():
    try:
        res = request.get_json()
        id = res.get('id')
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.id == id).first()
        db.session.delete(result)
        db.session.commit()
        return jsonify(errno=0, errmsg='删除成功')
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 排序方式
@api_video.route('/video_sort_info', methods=['POST'])
def VideoSort():
    try:
        res = request.get_json()
        type = res.get('type')  # 0--升序 1--降序
        vnum = res.get('vnum')  # 0--按照时间排序 1--按照播放的数量
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 10
        # 按照时间排序
        if type == 0 and vnum == 0:
            result = VideoInfo.query.filter(VideoInfo.status == 1).order_by(VideoInfo.update_time).limit(
                pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        if type == 1 and vnum == 0:
            result = VideoInfo.query.filter(VideoInfo.status == 1).order_by(VideoInfo.update_time.desc()).limit(
                pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 按照播放次数排序
        if type == 0 and vnum == 1:
            result = VideoInfo.query.filter(VideoInfo.status == 1).order_by(VideoInfo.play_nums).limit(
                pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        if type == 1 and vnum == 1:
            result = VideoInfo.query.filter(VideoInfo.status == 1).order_by(VideoInfo.play_nums.desc()).limit(
                pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 通过条件查询
@api_video.route('/video_search_info', methods=['POST'])
def VideoSearch():
    try:
        res = request.get_json()
        vtype = res.get('vtype')
        is_show = res.get('is_show')
        title = res.get('title')
        page = int(res.get('page', 1))
        pagesize = int(res.get('pagesize', 10))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            page, pagesize = 1, 10
        # 1.三个参数都不为空
        if vtype != "" and title != "" and is_show != "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == vtype,
                                            VideoInfo.title.contains(title), VideoInfo.is_show == is_show,
                                            ).limit(pagesize).offset((page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 2.第一个参数不为空，其他两个参数为空
        elif vtype != "" and is_show == "" and title == "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == vtype).limit(pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 3.第一个参数和三个参数为空，第二个参数不为空
        elif vtype == "" and is_show != "" and title == "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.is_show == is_show).limit(pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 4.第一个参数和二个参数为空，第三个参数不为空
        elif vtype == "" and is_show == "" and title != "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.title.contains(title)).limit(
                pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 5.第一个参数和二个参数不为空，第三个参数为空
        elif vtype != "" and is_show != "" and title == "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == vtype,
                                            VideoInfo.is_show == is_show).limit(pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 6.第一个参数和三个参数不为空，第二个参数为空
        elif vtype != "" and is_show == "" and title != "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.vtype == vtype,
                                            VideoInfo.title.contains(title)).limit(pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 7.第二个参数和三个参数不为空，第一个参数为空
        elif vtype == "" and is_show != "" and title != "":
            result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.is_show == is_show,
                                            VideoInfo.title.contains(title)).limit(pagesize).offset(
                (page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
        # 8.全部
        else:
            result = VideoInfo.query.filter(VideoInfo.status == 1).limit(pagesize).offset((page - 1) * pagesize)
            info_list = VideoQuery(result)
            return jsonify(errno=0, errmsg='查询成功', info_list=info_list)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')


# 上下架
@api_video.route('/is_show_update', methods=['POST'])
def IsShowUpdate():
    try:
        res = request.get_json()
        id = res.get('id')
        is_show = res.get('is_show')
        if not all([id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        result = VideoInfo.query.filter(VideoInfo.status == 1, VideoInfo.id == id).first()
        if is_show == 1:
            result.is_show = 0
        if is_show == 0:
            result.is_show = 1

        db.session.add(result)
        db.session.commit()
        is_show = result.is_show
        return jsonify(errno=0, errmsg='修改成功', is_show=is_show)
    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')
