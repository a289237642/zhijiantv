# -*- coding:utf-8 -*-
# author: will
import datetime
import time

from flask import request, jsonify, g

from app import db
from app.models import Banner, Article, UserBTN, UpdateTime
from utils.user_service.login import login_required, admin_required
from . import api_banner


# @api_banner.route('/uploadimage',methods=['POST'])
# def upload_image():
#     res = json.loads(request.data)
#     try:
#         if not all([res['data'], res['type']]):
#             return jsonify(errno="-2", errmsg='参数错误')
#     except Exception as e:
#         return jsonify(errno="-2", errmsg='参数错误')
#     res = storage_by_bs64(res['data'],res['type'])
#     if res:
#         data = {
#             'errno': '0',
#             'url': res
#         }
#     else:
#         data = {
#             'errno': '-2',
#             'msg': 'Fail'
#         }
#
#     return jsonify(data)
#
# @api_banner.route('/getbanneritem',methods=['POST'])
# def get_item():
#     res = request.get_json()
#     pid = res.get('pid',0)
#     result = Banner_name.query.filter_by(pid=pid).all()
#     if result:
#         try:
#             arr = []
#             for item in result.items:
#                 data = {
#                     'id':item.id,
#                     'name': item.image,
#                     'link': item.target_id
#                 }
#                 arr.append(data)
#         except Exception as e:
#             print(e)
#             return jsonify(errno="-2", errmsg='网络错误')
#         data = {
#             'errno': '0',
#             'list': arr,
#         }
#     else:
#         data = {
#             'errno': '0',
#             'list': {},
#         }
#     return jsonify(data)


# 新增banner
@api_banner.route('/createbanner', methods=['POST'])
@login_required
@admin_required
def create_banner():
    try:
        res = request.get_json()
        status = res.get('status')
        sort = res.get('sort')
        image = res.get('image')
        link = res.get('link')
        article_id = res.get('article_id')
        group_id = res.get('group_id')
        admin_id = g.user_id

        if not all([status, sort, image]):
            return jsonify(errno="-2", errmsg='参数不完整')

        if link and article_id:
            return jsonify(errno="-2", errmsg='不能同时设置文章和外链')

        try:
            status = int(status)
            sort = int(sort)
            article_id = int(article_id)
        except Exception as e:
            print(e)
            return jsonify(errno="-2", errmsg='参数类型错误')

        if status not in [0, 1]:
            return jsonify(errno="-2", errmsg='参数status错误')

        if sort <= 0:
            return jsonify(errno="-2", errmsg='请输入大于0的序号')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno="-2", errmsg='文章不存在')

        # group = Group.query.get('group_id')
        # if not group:
        #     return jsonify(errno="-2", errmsg='文章分类不存在')

        results = Banner.query.all()
        count = len(results)
        if sort > count:
            return jsonify(errno="-2", errmsg='输入的序号超出范围')

        for item in results:
            if item.sort >= sort:
                item.sort += 1

        data = Banner(
            image=image,
            link=link,
            sort=sort,
            status=status,
            article_id=article_id,
            group_id=group_id,
            admin_id=admin_id
        )

        sort_obj = Banner.query.order_by(Banner.sort.asc()).first()
        first_sort = sort_obj.sort
        print(first_sort)
        if sort <= first_sort and status == 1:
            # 记录小程序banner第一张图有更新,发送通知
            records = UserBTN.query.filter(UserBTN.btn_num == 4).all()
            for record in records:
                record.is_new = 1
                record.is_send = 0
                db.session.add(record)

            # 记录更新的时间
            today = datetime.datetime.today().date()
            up_obj = UpdateTime.query.filter(UpdateTime.type == 5).filter(
                UpdateTime.create_time.like(str(today) + "%")).first()
            if not up_obj:
                time_obj = UpdateTime()
                time_obj.type = 5
                db.session.add(time_obj)
        try:
            db.session.add(data)
            db.session.commit()

            data = {'errno': '0', 'msg': 'success'}
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {'errno': '-2', 'msg': 'Fail'}

    except Exception as e:
        print(e)
        data = {'errno': '-2', 'msg': '网络异常'}
        return jsonify(data)


# 修改banner
@api_banner.route('/changebanner', methods=['POST'])
@login_required
@admin_required
def change_banner():
    res = request.get_json()
    admin_id = g.user_id
    print("请求参数:", request.data)
    try:
        if not res['id']:
            return jsonify(errno="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(errno="-2", errmsg='参数错误')
    link = res.get('link')
    article_id = res.get('article_id')
    if link and article_id:
        return jsonify(errno="-2", errmsg='不能同时设置文章和外链')
    sort = res.get('sort', 1)
    resultsort = Banner.query.filter_by(sort=int(sort)).first()
    results = Banner.query.filter_by(id=int(res['id'])).first()
    if results:
        if resultsort:
            if int(results.sort) != int(sort):
                resultsdata = Banner.query.all()
                for item in resultsdata:
                    print((item.sort))
                    if item.sort >= int(res['sort']):
                        print((item.sort))
                        item.sort += 1
        results.status = res.get('status')
        results.image = res.get('image')
        results.sort = res.get('sort', 1)
        results.link = res.get('link')
        results.article_id = res.get('article_id')
        results.group_id = res.get('group_id')
        results.admin_id = admin_id

        sort_obj = Banner.query.order_by(Banner.sort.asc()).first()
        first_sort = sort_obj.sort
        print(first_sort)
        if sort <= first_sort and int(res.get('status')) == 1:
            # 记录小程序banner第一张图有更新,发送通知
            records = UserBTN.query.filter(UserBTN.btn_num == 4).all()
            for record in records:
                record.is_new = 1
                record.is_send = 0
                db.session.add(record)

            # 记录更新的时间
            today = datetime.datetime.today().date()
            up_obj = UpdateTime.query.filter(UpdateTime.type == 5).filter(
                UpdateTime.create_time.like(str(today) + "%")).first()
            if not up_obj:
                time_obj = UpdateTime()
                time_obj.type = 5
                db.session.add(time_obj)

        try:
            db.session.commit()
            data = {
                'errno': '0',
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'errno': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'errno': '-2',
            'msg': 'banner不存在'
        }

    return jsonify(data)


# 删除banner
@api_banner.route('/deletebanner', methods=['POST'])
@login_required
@admin_required
def delete_banner():
    res = request.get_json()
    print("请求参数:", request.data)
    try:
        if not res['id']:
            return jsonify(errno="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(errno="-2", errmsg='参数错误')

    results = Banner.query.filter_by(id=int(res['id'])).first()
    if results:
        try:
            db.session.delete(results)
            db.session.commit()
            data = {
                'errno': '0',
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'errno': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'errno': '-2',
            'msg': 'banner不存在'
        }
    return jsonify(data)


# 改变banner状态
@api_banner.route('/changebannertatus', methods=['POST'])
@login_required
@admin_required
def change_status():
    # res = json.loads(request.data)
    res = request.get_json()
    admin_id = g.user_id
    print("请求参数:", request.data)
    try:
        if not all([res['id'], str(res['status'])]):
            return jsonify(errno="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(errno="-2", errmsg='参数错误')
    results = Banner.query.filter_by(id=int(res['id'])).first()
    if results:
        if int(res['status']) == 1:
            cstatus = 0
        else:
            banner = Banner.query.order_by(Banner.sort.asc()).first()
            print(banner.sort)
            if results.sort <= banner.sort:
                # 记录小程序banner第一张图有更新,发送通知
                records = UserBTN.query.filter(UserBTN.btn_num == 4).all()
                for record in records:
                    record.is_new = 1
                    record.is_send = 0
                    db.session.add(record)

                # 记录更新的时间
                today = datetime.datetime.today().date()
                up_obj = UpdateTime.query.filter(UpdateTime.type == 5).filter(
                    UpdateTime.create_time.like(str(today) + "%")).first()
                if not up_obj:
                    time_obj = UpdateTime()
                    time_obj.type = 5
                    db.session.add(time_obj)

            cstatus = 1
        results.status = cstatus
        results.admin_id = admin_id
        # results.status = res['status']
        try:
            db.session.commit()
            data = {
                'errno': '0',
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'errno': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'errno': '-2',
            'msg': '活动不存在'
        }
    return jsonify(data)


# PC获取banner列表
@api_banner.route('/getpcbanner', methods=['POST'])
@login_required
@admin_required
def get_pcbannerlist():
    # res = json.loads(request.data)
    res = request.get_json()
    print("请求参数:", request.data)

    page = int(res.get('page', 1))
    size = int(res.get('size', 10))
    try:
        total = Banner.query.count()
        result = Banner.query.order_by(Banner.sort.asc()).paginate(page, size, False)
    except Exception as e:
        print(e)
        return jsonify(errno="-2", errmsg='数据库错误')
    if result:
        try:
            arr = []
            print((666))
            location = (page - 1) * size + 1
            for item in result.items:
                data = {
                    'id': item.id,
                    'image': item.image,
                    'link': item.link,
                    'sort': item.sort,
                    'location': location,
                    'status': str(item.status),
                    'article_id': item.article_id,
                    'group_id': item.group_id,
                }
                location += 1
                if item.article_id:
                    print((item.article_id))
                    res = Article.query.filter_by(id=item.article_id).first()

                    data['title'] = res.title
                arr.append(data)
        except Exception as e:
            print(e)
            return jsonify(errno="-2", errmsg='网络错误')
        data = {
            'errno': '0',
            'list': arr,
            'total': total
        }
    else:
        data = {
            'errno': '0',
            'list': {},
            'total': total
        }
    return jsonify(data)


# 小程序获取banner
@api_banner.route('/getbanner', methods=['POST'])
def get_banner():
    # res = json.loads(request.data)
    res = request.get_json()
    print("请求参数:", request.data)

    page = int(res.get('page', 1))
    size = int(res.get('size', 5))
    try:
        # total = Banner.query.filter_by(status=1).count()
        result = Banner.query.filter_by(status=1).order_by(Banner.sort.asc()).paginate(page, size, False)
    except Exception as e:
        print(e)
        return jsonify(errno="-2", errmsg='数据库错误')
    if result:
        try:
            arr = []
            for item in result.items:
                data = {
                    'id': item.id,
                    'image': item.image,
                    'article_id': item.article_id,
                    'group_id': item.group_id,
                    'link': item.link,
                    # 'target_name': item.target_name
                }
                if item.article_id:
                    res = Article.query.filter_by(id=item.article_id).first()
                    if res:
                        data['title'] = res.title
                    else:
                        data['title'] = ''

                arr.append(data)
        except Exception as e:
            print(e)
            return jsonify(errno="-2", errmsg='网络错误')
        data = {
            'status': '0',
            'list': arr,
        }
    else:
        data = {
            'errno': '0',
            'list': {},
        }
    start_time = time.time()
    # print '请求时间:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    # print "banner数据:", data
    return jsonify(data)
