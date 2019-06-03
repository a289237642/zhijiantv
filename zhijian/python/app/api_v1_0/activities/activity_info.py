# -*- coding:utf-8 -*-
# author: will
import time
from flask import json, request, jsonify
# from flask.ext.restful import reqparse

from app import db
from app.models import Activity, UserImage, ImageLesson
from utils.user_service.login import login_required, admin_required
from utils.oss_service.storage import storage_by_bs64, storage_by_url
from . import api_activity


# 上传图片
@api_activity.route('/up_image', methods=['POST'])
# @login_required
# @admin_required
def upload():
    try:
        image_file = request.files.get('image')
        print(image_file)
        now = time.time()
        # image_file.save('../storage/image/%s.jpg' % str(now))
        image_file.save('/www/zjlive/zhijian_live_miniprogram/storage/image/%s.jpg' % str(now))

        url = 'https://zj-live-dev.max-digital.cn/storage/image/' + str(now) + '.' + 'jpg'
        oss_url = storage_by_url(url)
        # newurl = oss_url.replace('http', 'https')
        return jsonify(errno=0, errmsg="OK", img_url=oss_url)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='上传图片失败')


@api_activity.route('/uploadimage', methods=['POST'])
# @login_required
# @admin_required
def upload_image():
    res = json.loads(request.data)
    # try:
    #     if not all([res['data'], res['type']]):
    #         return jsonify(status="-2", errmsg='参数错误')
    # except Exception as e:
    #     return jsonify(status="-2", errmsg='参数错误')
    imgtype = res['data'][11:14]
    if imgtype == 'png':
        imgtype = 'png'
    else:
        imgtype = 'jpg'
    print(imgtype)
    res = storage_by_bs64(res['data'], imgtype)
    # res = res.replace('http', 'https')
    if res:
        data = {
            'status': '0',
            'url': res
        }
    else:
        data = {
            'status': '-2',
            'msg': 'Fail'
        }

    return jsonify(data)


@api_activity.route('/createactivity', methods=['POST'])
@login_required
@admin_required
def create_activity():
    # res = json.loads(request.data)
    res = request.get_json()
    # activity = reqparse.RequestParser()
    # activity.add_argument('title',type=str,required=True,help='title must be provide')
    # activity.add_argument('status',type=int,required=True,help='status must be provide')
    # activity.add_argument('link',type=str,required=True,help='link must be provide')
    # activity.add_argument('main_img',type=str,required=True,help='main_img must be provide')
    # activity.add_argument('sort',type=int,required=True,help='sort must be provide')
    # try:
    #     args = activity.parse_args()
    # except Exception as e:
    #     print(e)
    # print(args['title'])
    # print(res['title'],res['status'],res['link'],res['main_img'],res['sort'])
    try:
        if not all([res['title'], str(res['status']), res['link'], res['main_img'], res['sort']]):
            print((111))
            return jsonify(status=-2, errmsg='参数错误')
    except Exception as e:
        print((222))
        return jsonify(status=-2, errmsg='参数错误')
    newid = 'HD' + str(Activity.query.count() + 1).zfill(6)
    data = Activity(
        activityid=newid,
        title=res['title'],
        tag=res.get('tag', ''),
        link=res['link'],
        main_img=res['main_img'],
        sort=res['sort'],
        status=res['status']
    )
    try:
        db.session.add(data)
        db.session.commit()

        data = {
            'status': '0',
            'msg': 'success'
        }
    except Exception as e:
        db.session.rollback()
        print(e)
        data = {
            'status': '-2',
            'msg': 'Fail'
        }
    return jsonify(data)


@api_activity.route('/changeactivity', methods=['POST'])
@login_required
@admin_required
def change_activity():
    res = request.get_json()
    try:
        if not res['id']:
            return jsonify(status=-2, errmsg='参数错误')
    except Exception as e:
        return jsonify(status=-2, errmsg='参数错误')

    results = Activity.query.filter_by(id=res['id']).first()
    if results:
        results.status = res.get('status')
        results.main_img = res.get('main_img')
        results.sort = res.get('sort')
        results.link = res.get('link')
        results.title = res.get('title')
        results.tag = res.get('tag')
        try:
            db.session.commit()
            data = {
                'status': '0',
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'status': '-2',
            'msg': '活动不存在'
        }
    return jsonify(data)


@api_activity.route('/changestatus', methods=['POST'])
@login_required
@admin_required
def change_status():
    # res = json.loads(request.data)
    res = request.get_json()
    print(res)
    try:
        if not all([res['id'], res['status']]):
            return jsonify(status=-2, errmsg='参数错误')
    except Exception as e:
        return jsonify(status=-2, errmsg='参数错误')
    results = Activity.query.filter_by(id=res['id']).first()
    if results:
        if int(res['status']) == 1:
            cstatus = 0
        else:
            cstatus = 1
        results.status = cstatus
        try:
            db.session.commit()
            data = {
                'status': '0',
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'status': '-2',
            'msg': '活动不存在'
        }
    return jsonify(data)


@api_activity.route('/getpcactivity', methods=['POST'])
@login_required
@admin_required
def get_pcactivitylist():
    # res = json.loads(request.data)
    res = request.get_json()
    page = int(res.get('page', 1))
    size = int(res.get('size', 10))
    try:
        total = Activity.query.count()
        result = Activity.query.order_by(Activity.sort.asc()).paginate(page, size, False)
    except Exception as e:
        print(e)
        return jsonify(status="-2", errmsg='数据库错误')
    if result:
        try:
            arr = []
            for item in result.items:
                data = {
                    'id': item.id,
                    'activityid': item.activityid,
                    'sort': item.sort,
                    'title': item.title,
                    'main_img': item.main_img,
                    'link': item.link,
                    'tag': item.tag,
                    'status': str(item.status)
                }
                arr.append(data)
        except Exception as e:
            print(e)
            return jsonify(status="-2", errmsg='网络错误')
        data = {
            'status': '0',
            'list': arr,
            'total': total
        }
    else:
        data = {
            'status': '0',
            'list': {},
            'total': total
        }
    return jsonify(data)


# 小程序活动列表
@api_activity.route('/getactivity', methods=['POST'])
def get_activity():
    # res = json.loads(request.data)
    res = request.get_json()
    page = int(res.get('page', 1))
    size = int(res.get('size', 10))
    try:
        total = Activity.query.filter_by(status=1).count()
        result = Activity.query.filter_by(status=1).order_by(Activity.sort.asc()).paginate(page, size, False)
    except Exception as e:
        print(e)
        return jsonify(status="-2", errmsg='数据库错误')
    if result:
        try:
            arr = []
            for item in result.items:
                data = {
                    'id': item.id,
                    'title': item.title,
                    'main_img': item.main_img,
                    'link': item.link,
                    'tag': item.tag
                }
                arr.append(data)
        except Exception as e:
            print(e)
            return jsonify(status="-2", errmsg='网络错误')
        data = {
            'status': '0',
            'list': arr,
            'total': total
        }
    else:
        data = {
            'status': '0',
            'list': {},
            'total': total
        }
    return jsonify(data)


# 上传图片到头像库
@api_activity.route('/upupup', methods=['POST'])
@login_required
@admin_required
def upupup():
    try:
        # image_file = request.files.get('image')
        # print(image_file)
        # now = time.time()
        # image_file.save('/www/zjdev/zhijian_live_miniprogram/storage/image/%s.jpg' % str(now))
        #
        # url = 'https://zj-live-dev.max-digital.cn/storage/image/' + str(now) + '.' + 'jpg'
        # print url
        # oss_url = storage_by_url(url)
        # newurl = oss_url.replace('http', 'https')

        res = json.loads(request.data)
        img_type = res['data'][11:14]
        print(img_type)
        if img_type == 'png':
            imgtype = 'png'
        else:
            imgtype = 'jpg'
        new_url = storage_by_bs64(res['data'], imgtype)
        # new_url = new_url.replace('http', 'https')

        obj = UserImage()
        obj.pic = new_url
        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", img_url=new_url)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='上传图片失败')


# 头像库列表
@api_activity.route('/image_store', methods=['POST'])
@login_required
@admin_required
def image_store():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print (e)
            return jsonify(errno=-1, errmsg='参数错误')

        results = UserImage.query.all()
        count = len(results)
        results = results[(page - 1) * pagesize : page * pagesize]
        image_list = list()
        i = (page - 1) * pagesize + 1
        for result in results:
            image_dict = dict()
            image_dict['location'] = i
            image_dict['image_id'] = result.id
            image_dict['pic'] = result.pic
            image_list.append(image_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", image_list=image_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='查询头像库失败')


# 头像库删除
@api_activity.route('/del_image', methods=['POST'])
@login_required
@admin_required
def del_image():
    try:
        res = request.get_json()
        image_id = res.get('image_id')

        try:
            image_id = int(image_id)
        except Exception as e:
            print (e)
            return jsonify(errno=-1, errmsg='参数错误')

        image_obj = UserImage.query.get(image_id)
        if not image_obj:
            return jsonify(errno=-1, errmsg='ID不存在')

        results = ImageLesson.query.filter(ImageLesson.image_id == image_id).all()
        for result in results:
            db.session.delete(result)

        db.session.delete(image_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='查询头像库失败')
