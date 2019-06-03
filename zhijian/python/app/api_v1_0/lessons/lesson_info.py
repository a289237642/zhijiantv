# -*- coding:utf-8 -*-
# author: will
import datetime
import logging
import random
import time

from flask import jsonify, request, g

from app import db
from app.models import Lesson, LessonBanner, Module, Lesson_type, NewLesson, LessonOrder, User, LessonTypeShip, Audio, \
    Admin, UserImage, ImageLesson, UserBTN, UpdateTime, DailyBornQrNum, DailyScanQrNum
from utils.user_service.login import login_required, admin_required
from . import api_lesson


# 课程banner
@api_lesson.route('/lesson_banners')
def lesson_banners():
    try:
        docs = LessonBanner.query.all()
        banner_list = list()
        for doc in docs:
            banner_dict = dict()
            banner_dict['name'] = doc.name
            banner_dict['img_url'] = doc.img_url
            banner_dict['jump_url'] = doc.jump_url
            banner_dict['is_big'] = doc.is_big
            banner_list.append(banner_dict)

        return jsonify(errno=0, errmsg="OK", data=banner_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='列表查询失败')


# 课程
@api_lesson.route('/get_lessons', methods=['POST'])
def get_lessons():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        try:
            page = int(page)
        except Exception as e:
            print(e)
            page = 1

        try:
            pagesize = int(pagesize)
        except Exception as e:
            logging.error(e)
            pagesize = 10
        docs = Module.query.all()
        banner_list = list()
        for doc in docs:
            module_id = doc.id
            module_dict = dict()
            module_dict['name'] = doc.name
            module_dict['all_link'] = doc.jump_url
            lessons = Lesson.query.filter(Lesson.module_id == module_id, Lesson.is_show == 1).all()
            lesson_list = list()
            for obj in lessons:
                lesson_dict = dict()
                # lesson_dict['name'] = obj.name
                # lesson_dict['author'] = obj.author
                # lesson_dict['summary'] = obj.summary
                # lesson_dict['price'] = obj.price
                lesson_dict['img_url'] = obj.img_url
                lesson_dict['jump_url'] = obj.jump_url
                # lesson_dict['is_show'] = obj.is_show
                lesson_list.append(lesson_dict)
                module_dict['lessons'] = lesson_list
            banner_list.append(module_dict)
        banner_list = banner_list[(page - 1) * pagesize:page * pagesize]
        return jsonify(errno=0, errmsg="OK", data=banner_list)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='列表查询失败')


# 课程
@api_lesson.route('/get_pclessons', methods=['POST'])
def get_pclessons():
    try:
        res = request.get_json()
        module_id = res.get('module_id')
        # try:
        #     page = int(page)
        # except Exception as e:
        #     print e
        #     page = 1
        #
        # try:
        #     pagesize = int(pagesize)
        # except Exception as e:
        #     logging.error(e)
        #     pagesize = 10
        try:
            module_id = int(module_id)
            if module_id not in [1, 2, 3, 4, 5]:
                return jsonify(errno=-1, errmsg='module_id参数错误')
        except Exception as e:
            print(e)
        moduleres = Module.query.filter_by(id=module_id).first()
        lessons = Lesson.query.filter(Lesson.module_id == module_id).all()
        module_dict = {}
        module_dict['moduleName'] = moduleres.name
        module_dict['path'] = moduleres.jump_url
        lesson_list = []
        for obj in lessons:
            lesson_dict = dict()
            lesson_dict['url'] = obj.img_url
            lesson_dict['val'] = obj.jump_url
            lesson_dict['name'] = obj.name
            lesson_dict['id'] = obj.id
            if obj.is_show:
                lesson_dict['status'] = True
            else:
                lesson_dict['status'] = False
            # lesson_dict['status'] = obj.is_show
            # lesson_dict['status'] = True
            lesson_list.append(lesson_dict)
        module_dict['list'] = lesson_list

        # banner_list = banner_list[(page - 1) * pagesize:page * pagesize]
        return jsonify(errno=0, errmsg="OK", data=module_dict)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='列表查询失败')


@api_lesson.route('/edit_lessons', methods=['POST'])
def edit_lessons():
    try:
        res = request.get_json()
        if not all([res['moduleId'], res['moduleName']]):
            return jsonify(errno=-1, errmsg='参数错误')
        try:
            model_id = res.get('moduleId')
            model_name = res.get('moduleName')
            model_jump_url = res.get('path')
            modelres = Module.query.filter_by(id=model_id).first()
            if modelres:
                modelres.name = model_name
                modelres.jump_url = model_jump_url
                db.session.commit()
            else:
                data = Module(
                    id=int(model_id),
                    name=model_name,
                    jump_url=model_jump_url
                )
                db.session.add(data)
                db.session.commit()
            model_data = res.get('list')
            try:
                for data in model_data:
                    jump_url = data.get('val')
                    image_url = data.get('url')
                    is_show = data.get('status', 0)
                    id = data.get('id', 0)
                    if is_show:
                        is_show = 1
                    else:
                        is_show = 0
                    lessonres = Lesson.query.filter_by(id=id).first()
                    if lessonres:
                        lessonres.img_url = image_url
                        lessonres.jump_url = jump_url
                        lessonres.is_show = is_show
                        db.session.commit()
                    else:
                        data = Lesson(
                            module_id=int(model_id),
                            img_url=image_url,
                            is_show=is_show,
                            jump_url=jump_url
                        )
                        db.session.add(data)
                        db.session.commit()
                return jsonify(errno=0, errmsg='success')
            except Exception as e:
                return jsonify(errno=-1, errmsg='list不能为空')
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='Fail')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络错误')


# 新
# pc新增课程类别
@api_lesson.route('/add_lesson_type', methods=['POST'])
@login_required
def add_lesson_type():
    params = request.get_json()
    name = params.get('name')
    sort = params.get('sort', 1)
    admin_id = g.user_id

    print("请求参数:", request.data)
    if not name:
        return jsonify(errno=-1, errmsg='请传入类别名称')

    try:
        resultsort = Lesson_type.query.filter_by(sort=int(sort)).first()
        if resultsort:
            results = Lesson_type.query.all()
            for item in results:
                print((item.sort))
                if item.sort >= int(params['sort']):
                    print((item.sort))
                    item.sort += 1
                    db.session.add(item)

        type_obj = Lesson_type()
        type_obj.name = name
        type_obj.sort = sort
        type_obj.admin_id = admin_id

        db.session.add(type_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='新增成功')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc修改课程类别状态
@api_lesson.route('/status_lesson_type', methods=['POST'])
@login_required
def status_lesson_type():
    params = request.get_json()
    type_id = params.get('type_id')
    admin_id = g.user_id

    print("请求参数:", request.data)
    if type_id:
        try:
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='类别id错误')
    else:
        return jsonify(errno=-1, errmsg='请传入类别id')
    try:
        type_obj = Lesson_type.query.filter(Lesson_type.id == type_id).first()
        if type_obj:
            state = 0 if type_obj.is_show else 1
            type_obj.is_show = state
            type_obj.admin_id = admin_id
            db.session.add(type_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='修改成功')
        else:
            return jsonify(errno=-1, errmsg='类别不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc修改课程类别
@api_lesson.route('/edit_lesson_type', methods=['POST'])
@login_required
def edit_lesson_type():
    params = request.get_json()
    name = params.get('name')
    type_id = params.get('type_id')
    sort = params.get('sort')
    admin_id = g.user_id

    print("请求参数:", request.data)
    if not name:
        return jsonify(errno=-1, errmsg='请传入类别名称')
    if type_id:
        try:
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='类别id错误')
    else:
        return jsonify(errno=-1, errmsg='请传入类别id')
    try:
        resultsort = Lesson_type.query.filter_by(sort=int(sort)).first()
        if resultsort:
            results = Lesson_type.query.all()
            for item in results:
                print((item.sort))
                if item.sort >= int(params['sort']):
                    print((item.sort))
                    item.sort += 1
                    db.session.add(item)

        type_obj = Lesson_type.query.filter(Lesson_type.id == type_id).first()
        if type_obj:
            type_obj.name = name
            type_obj.sort = sort
            type_obj.admin_id = admin_id
            db.session.add(type_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='修改成功')
        else:
            return jsonify(errno=-1, errmsg='类别不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc删除课程类别
@api_lesson.route('/delete_lesson_type', methods=['POST'])
@login_required
def delete_lesson_type():
    params = request.get_json()
    type_id = params.get('type_id')

    print("请求参数:", request.data)
    if type_id:
        try:
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='类别id错误')
    else:
        return jsonify(errno=-1, errmsg='请传入类别id')
    try:
        type_obj = Lesson_type.query.get(type_id)
        if type_obj:
            results = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).all()
            if results:
                for res in results:
                    lesson_id = res.lesson_id
                    db.session.delete(res)

                    types = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id).all()
                    num = len(types)
                    if num == 0:
                        lesson_obj = NewLesson.query.get(lesson_id)
                        lesson_obj.is_show = 0
                        db.session.add(lesson_obj)

            db.session.delete(type_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg='删除成功')
        else:
            return jsonify(errno=-1, errmsg='类别不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc获取课程类别
@api_lesson.route('/pc_get_lesson_type', methods=['POST'])
@login_required
def pc_get_lesson_type():
    params = request.get_json()
    page = params.get('page', 1)
    pagesize = params.get('pagesize', 10)

    print("请求参数:", request.data)
    try:
        type_obj = Lesson_type.query.order_by(Lesson_type.sort.asc()).paginate(page, pagesize, False)
        count = type_obj.total
        type_list = list()
        if type_obj:

            i = (page - 1) * pagesize + 1
            for item in type_obj.items:
                type_dict = dict()
                type_dict['name'] = item.name
                type_dict['type_id'] = item.id
                type_dict['location'] = i
                type_dict['is_show'] = item.is_show
                type_dict['sort'] = item.sort
                i += 1
                type_list.append(type_dict)
        return jsonify(errno=0, errmsg='查询成功', data=type_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--获取课程类别
@api_lesson.route('/get_lesson_type', methods=['POST'])
def get_lesson_type():
    params = request.get_json()
    page = params.get('page', 1)
    pagesize = params.get('pagesize', 10)

    print("请求参数:", request.data)
    try:
        type_obj = Lesson_type.query.filter(Lesson_type.is_show == 1).order_by(Lesson_type.sort.asc()).paginate(page,
                                                                                                                pagesize,
                                                                                                                False)
        count = type_obj.total
        type_list = list()
        if type_obj:
            for item in type_obj.items:
                type_dict = dict()
                type_dict['name'] = item.name
                type_dict['type_id'] = item.id
                type_list.append(type_dict)
        return jsonify(errno=0, errmsg='查询成功', data=type_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 课程到期后下架
@api_lesson.route('/lesson_down')
def lesson_down():
    try:
        now = time.time()
        now = datetime.datetime.fromtimestamp(int(now))
        print(now)
        results = NewLesson.query.filter(NewLesson.is_show == 1).all()
        for result in results:
            if result.end_time <= now:
                print('课程:%s到期下架,到期日期是:%s' % (result.title, result.end_time))
                result.is_show = 0
                db.session.add(result)

                objs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == result.id).all()
                for obj in objs:
                    # 修改当前类型下所属课程的sort_num
                    lessons = LessonTypeShip.query.filter(LessonTypeShip.type_id == obj.type_id).all()
                    for lesson in lessons:
                        if lesson.sort_num > obj.sort_num:
                            lesson.sort_num -= 1
                            db.session.add(lesson)

                    db.session.delete(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--首页免费领课程列表
@api_lesson.route('/get_lesson_list', methods=['POST'])
def get_lesson_list():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 10)
        user_id = params.get('user_id')
        type_id = params.get('type_id')

        print("请求参数:", request.data)
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print(e)
            page = 1
            pagesize = 10

        if not all([user_id, type_id]):
            return jsonify(errno=-1, errmsg='参数不完整')
        try:
            user_id = int(user_id)
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        type_obj = Lesson_type.query.get(type_id)
        if not type_obj:
            return jsonify(errno=-1, errmsg='该课程类别不存在')

        print('当前用户的user_id:', user_id)
        # 当前用户已参与的课程的ID
        order_lessons_id_list = list()
        order_lessons = LessonOrder.query.filter(LessonOrder.user_id == user_id).all()
        for order_lesson in order_lessons:
            order_lessons_id_list.append(order_lesson.lesson_id)

        # 当前类别下用户未参与的课程ID
        lessons_id_list = list()
        results = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).order_by(LessonTypeShip.sort_num).all()
        for result in results:
            if result.lesson_id not in order_lessons_id_list:
                lessons_id_list.append(result.lesson_id)
            # # 当前用户未参与的课程ID
            # lessons_id_list = list()
            # lessons = NewLesson.query.filter(NewLesson.is_show == 1).order_by(NewLesson.sort_num).all()
            # for lesson in lessons:
            #     if lesson.id not in order_lessons_id_list:
            #         lessons_id_list.append(lesson.id)

        lessons_id_list = lessons_id_list[(page - 1) * pagesize:page * pagesize]
        count = len(lessons_id_list)
        lesson_list = list()
        for lesson_id in lessons_id_list:
            lesson_obj = NewLesson.query.get(lesson_id)
            lesson_dict = dict()
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['lesson_id'] = lesson_id
            lesson_dict['cost_type'] = lesson_obj.cost_type

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                         LessonOrder.is_pay == 1).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--课程详情
@api_lesson.route('/lesson_detail', methods=['POST'])
def lesson_detail():
    params = request.get_json()
    lesson_id = params.get('lesson_id')
    user_id = params.get('user_id')

    print('传入参数:%s' % request.data)
    if not all([lesson_id, user_id]):
        return jsonify(errno=-1, errmsg='参数不完整')

    try:
        user_id = int(user_id)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='user_id错误')

    user_obj = User.query.get(user_id)
    if not user_obj:
        return jsonify(errno=-1, errmsg='用户不存在')

    try:
        lesson_id = int(lesson_id)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='lesson_id错误')

    lesson_obj = NewLesson.query.get(lesson_id)
    if not lesson_obj:
        return jsonify(errno=-1, errmsg='课程不存在')

    try:
        if lesson_obj:
            lesson_dict = dict()
            # 课程信息
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['author'] = lesson_obj.author
            lesson_dict['summary'] = lesson_obj.summary
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['count'] = lesson_obj.count
            lesson_dict['cost_type'] = lesson_obj.cost_type

            order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                 LessonOrder.user_id == user_id).first()
            if order_obj:
                lesson_dict['is_pay'] = order_obj.is_pay
                lesson_dict['order_status'] = order_obj.order_status
                lesson_dict['order_id'] = order_obj.id

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                         LessonOrder.is_pay == 1).order_by(
                LessonOrder.create_time.asc()).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            # 已购买人信息,加入随机头像
            user_list = list()

            results = ImageLesson.query.filter(ImageLesson.lesson_id == lesson_id).all()
            if results:
                for result in results:
                    obj = UserImage.query.get(result.image_id)
                    user_list.append(obj.pic)
                    # user_list = random.sample(user_list, len(user_list))
            else:
                images = UserImage.query.all()
                image_id_list = list()
                for image in images:
                    image_id_list.append(image.id)

                if lesson_obj.base_num <= 10:
                    image_id_list = random.sample(image_id_list, lesson_obj.base_num)
                else:
                    image_id_list = random.sample(image_id_list, 10)

                print("随机头像id:", image_id_list)
                for image_id in image_id_list:
                    image_obj = UserImage.query.get(image_id)

                    image_lesson_obj = ImageLesson()
                    image_lesson_obj.image_id = image_id
                    image_lesson_obj.lesson_id = lesson_id
                    db.session.add(image_lesson_obj)
                    user_list.append(image_obj.pic)

                db.session.commit()

            if buy_lesson_orders:
                for order in buy_lesson_orders:
                    user_obj = User.query.get(order.user_id)
                    if user_obj:
                        user_list.insert(0, user_obj.avatar_url)

            lesson_dict['user_list'] = user_list[0:10]
            return jsonify(errno=0, data=lesson_dict)

    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc新增课程
@api_lesson.route('/add_lesson', methods=['POST'])
@login_required
def add_lesson():
    try:
        params = request.get_json()
        title = params.get('title')
        subtitle = params.get('subtitle')
        min_pic = params.get('min_pic')
        count = params.get('count')
        price = params.get('price')
        summary = params.get('summary')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        cost_type = params.get('cost_type')
        present_num = params.get('present_num')
        base_num = params.get('base_num')
        total_audio_num = params.get('total_audio_num', 0)
        admin_id = g.user_id
        # user_id = 6

        print('请求参数：', request.data)
        if not all(
                [title, subtitle, min_pic, count, price, summary, end_time, cost_type, present_num, base_num]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            count = int(count)
            cost_type = int(cost_type)
            present_num = int(present_num)
            price = int(price)
            base_num = int(base_num)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        # if base_num >= count or present_num >= count:
        #     return jsonify(errno=-1, errmsg='参数错误,拉新赠送数和领取人数基数必须小于库存')

        if present_num > price:
            return jsonify(errno=-1, errmsg='参数错误,拉新赠送数不能大于课程价格')

        results = NewLesson.query.all()
        if results:
            for result in results:
                if result.title == title:
                    return jsonify(errno=-1, errmsg='参数错误,该课程标题已存在')
                result.sort_num += 1
                db.session.add(result)

        user_obj = Admin.query.get(admin_id)

        lesson_obj = NewLesson()
        lesson_obj.admin_id = admin_id
        lesson_obj.title = title
        lesson_obj.subtitle = subtitle
        lesson_obj.min_pic = min_pic
        lesson_obj.author = user_obj.username
        lesson_obj.count = count
        lesson_obj.price = price
        lesson_obj.summary = summary
        lesson_obj.start_time = start_time
        lesson_obj.end_time = end_time
        lesson_obj.cost_type = cost_type
        lesson_obj.present_num = present_num
        lesson_obj.base_num = base_num
        lesson_obj.sort_num = 1
        lesson_obj.total_audio_num = total_audio_num
        db.session.add(lesson_obj)
        db.session.commit()

        return jsonify(errno=0, errmsg='OK', lesson_id=lesson_obj.id)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='新增课程失败')


# pc修改课程
@api_lesson.route('/edit_lesson', methods=['POST'])
@login_required
def edit_lesson():
    try:
        params = request.get_json()
        lesson_id = params.get('lesson_id')
        title = params.get('title')
        subtitle = params.get('subtitle')
        author = params.get('author')
        min_pic = params.get('min_pic')
        count = params.get('count')
        price = params.get('price')
        summary = params.get('summary')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        cost_type = params.get('cost_type')
        present_num = params.get('present_num')
        base_num = params.get('base_num')
        total_audio_num = params.get('total_audio_num')
        admin_id = g.user_id

        print('请求参数：', request.data)
        if not all(
                [lesson_id, title, subtitle, author, min_pic, count, price, summary, end_time, cost_type]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            count = int(count)
            cost_type = int(cost_type)
            present_num = int(present_num)
            base_num = int(base_num)
            lesson_id = int(lesson_id)
            price = int(price)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        lesson_obj = NewLesson.query.filter(NewLesson.id == lesson_id).first()
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='课程不存在')

        if base_num >= count or present_num >= count:
            return jsonify(errno=-1, errmsg='参数错误,拉新赠送数和领取人数基数必须小于库存')

        if present_num > price:
            return jsonify(errno=-1, errmsg='参数错误,拉新赠送数不能大于课程价格')

        lesson_obj.title = title
        lesson_obj.subtitle = subtitle
        lesson_obj.min_pic = min_pic
        lesson_obj.author = author
        lesson_obj.count = count
        lesson_obj.price = price
        lesson_obj.summary = summary
        lesson_obj.start_time = start_time
        lesson_obj.end_time = end_time
        lesson_obj.cost_type = cost_type
        lesson_obj.present_num = present_num
        lesson_obj.base_num = base_num
        lesson_obj.total_audio_num = total_audio_num
        lesson_obj.admin_id = admin_id
        db.session.add(lesson_obj)

        results = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id).all()
        for result in results:
            result.price = price
            db.session.add(result)

        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc课程分类列表
@api_lesson.route('/pc_lesson_list', methods=['POST'])
@login_required
def pc_lesson_list():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 10)
        type_id = params.get('type_id')

        print("请求参数:", request.data)
        if not type_id:
            return jsonify(errno=-1, errmsg='请传入课程分类type_id')

        try:
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='type_id错误')
        type_obj = Lesson_type.query.get(type_id)
        if not type_obj:
            return jsonify(errno=-1, errmsg='type不存在')

        lesson_id_list = list()
        ships_obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).order_by(
            LessonTypeShip.sort_num).all()
        for ship in ships_obj:
            lesson_id_list.append(ship.lesson_id)

        count = len(lesson_id_list)
        print(123, lesson_id_list)
        lesson_id_list = lesson_id_list[(page - 1) * pagesize:page * pagesize]
        lesson_list = list()

        for lesson_id in lesson_id_list:
            lesson_dict = dict()
            lesson_obj = NewLesson.query.filter(NewLesson.is_show == 1, NewLesson.id == lesson_id).first()
            print('lesson_id:', lesson_id)
            lesson_dict['id'] = lesson_id
            lesson_dict['lesson_id'] = "KC" + str(lesson_id).zfill(6)
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['author'] = lesson_obj.author
            lesson_dict['count'] = lesson_obj.count
            lesson_dict['summary'] = lesson_obj.summary
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['is_show'] = lesson_obj.is_show
            # lesson_dict['start_time'] = str(lesson_obj.start_time)
            lesson_dict['end_time'] = str(lesson_obj.end_time)
            lesson_dict['cost_type'] = lesson_obj.cost_type

            obj = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id,
                                              LessonTypeShip.type_id == type_id).first()
            lesson_dict['sort_num'] = obj.sort_num

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

            orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id, LessonOrder.is_pay == 1).all()
            buy_num = len(orders)
            lesson_dict['buy_num'] = buy_num

            # 课程生成二维码的数量(邀友听课)
            listen_bron_qr_num = 0
            now = datetime.datetime.now()
            # l_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 1).first()
            l_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 1,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if l_bron_qr:
                listen_bron_qr_num = l_bron_qr.daily_num
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num
            else:
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num

            # 课程生成二维码的数量(邀友鼓励)
            help_bron_qr_num = 0
            # h_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 2).first()
            h_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 2,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if h_bron_qr:
                help_bron_qr_num = h_bron_qr.daily_num
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num
            else:
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num

            # 识别课程二维码的数量(邀友听课)
            listen_scan_qr_num = 0
            # l_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 1).first()
            l_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 1,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if l_scan_qr:
                listen_scan_qr_num = l_scan_qr.daily_num
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num
            else:
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num

            # 识别课程二维码的数量(邀友鼓励)
            help_scan_qr_num = 0
            # h_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 2).first()
            h_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 2,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if h_scan_qr:
                help_scan_qr_num = h_scan_qr.daily_num
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num
            else:
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num

            # 识别课程二维码的总数
            lesson_dict['scan_qr_num'] = listen_scan_qr_num + help_scan_qr_num

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--课程分类列表
@api_lesson.route('/lesson_list', methods=['POST'])
def lesson_list():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 3)
        type_id = params.get('type_id')
        user_id = params.get('user_id')

        print("请求参数:", request.data)
        if not all([type_id, user_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            user_id = int(user_id)
            type_id = int(type_id)
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        type_obj = Lesson_type.query.get(type_id)
        if not type_obj:
            return jsonify(errno=-1, errmsg='type不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        print('当前用户的user_id:', user_id)

        lesson_id_list = list()
        ships_obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).order_by(
            LessonTypeShip.sort_num).all()
        for ship in ships_obj:
            lesson_id_list.append(ship.lesson_id)

        count = len(lesson_id_list)
        lesson_id_list = lesson_id_list[(page - 1) * pagesize:page * pagesize]
        lesson_list = list()
        for lesson_id in lesson_id_list:
            lesson_dict = dict()
            lesson_obj = NewLesson.query.get(lesson_id)
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['lesson_id'] = lesson_id
            lesson_dict['cost_type'] = lesson_obj.cost_type

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                         LessonOrder.is_pay == 1).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            # 当前用户参与该课程的状态
            order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                 LessonOrder.user_id == user_id).first()
            if order_obj:
                help_num = order_obj.help_num
                price = order_obj.price
                need = int(price) - int(help_num)

                lesson_dict['status'] = order_obj.order_status
                lesson_dict['order_id'] = order_obj.id
                if need >= 0:
                    lesson_dict['need'] = need
                else:
                    lesson_dict['need'] = 0

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--课程分类列表(点换一批)
@api_lesson.route('/change_lesson_list', methods=['POST'])
def change_lesson_list():
    try:
        params = request.get_json()
        type_id = params.get('type_id')
        user_id = params.get('user_id')

        print('请求参数：', request.data)
        if not all([type_id, user_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            user_id = int(user_id)
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        type_obj = Lesson_type.query.get(type_id)
        if not type_obj:
            return jsonify(errno=-1, errmsg='type不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        print('当前用户的user_id:', user_id)

        lesson_id_list = list()
        ships_obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).all()
        for ship in ships_obj:
            lesson_id_list.append(ship.lesson_id)

        count = len(lesson_id_list)
        print(count)
        rand_number = random.randint(0, count - 3)
        print(rand_number)
        lesson_id_list = lesson_id_list[rand_number: rand_number + 3]
        lesson_list = list()
        for lesson_id in lesson_id_list:
            lesson_dict = dict()
            lesson_obj = NewLesson.query.get(lesson_id)
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['lesson_id'] = lesson_id
            lesson_dict['cost_type'] = lesson_obj.cost_type

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                         LessonOrder.is_pay == 1).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            # 当前用户参与该课程的状态
            order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                 LessonOrder.user_id == user_id).first()
            if order_obj:
                help_num = order_obj.help_num
                price = order_obj.price
                need = int(price) - int(help_num)

                lesson_dict['status'] = order_obj.order_status
                lesson_dict['order_id'] = order_obj.id
                if need >= 0:
                    lesson_dict['need'] = need
                else:
                    lesson_dict['need'] = 0

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc课程搜索
@api_lesson.route('/lesson_search', methods=['POST'])
def lesson_search():
    try:
        res = request.get_json()
        words = res.get('words')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        is_show = res.get('is_show')

        print('请求参数：', request.data)
        try:
            page = int(page)
        except Exception as e:
            print(e)
            page = 1

        try:
            pagesize = int(pagesize)
        except Exception as e:
            logging.error(e)
            pagesize = 10

        if words:
            if is_show:
                all_results = NewLesson.query.filter(NewLesson.is_show == is_show).filter(
                    NewLesson.title.like("%" + words + "%")).order_by(
                    NewLesson.create_time.desc()).all()
            else:
                all_results = NewLesson.query.filter(NewLesson.title.like("%" + words + "%")).order_by(
                    NewLesson.create_time.desc()).all()
        else:
            if is_show:
                all_results = NewLesson.query.filter(NewLesson.is_show == is_show).order_by(
                    NewLesson.create_time.desc()).all()
            else:
                all_results = NewLesson.query.order_by(NewLesson.create_time.desc()).all()
        count = len(all_results)
        lessons = all_results[(page - 1) * pagesize:page * pagesize]
        i = (page - 1) * pagesize + 1
        lesson_list = list()
        for lesson_obj in lessons:
            lesson_dict = dict()
            lesson_dict['lesson_id'] = "KC" + str(lesson_obj.id).zfill(6)
            lesson_dict['id'] = lesson_obj.id
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['author'] = lesson_obj.author
            lesson_dict['count'] = lesson_obj.count
            lesson_dict['summary'] = lesson_obj.summary
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['is_show'] = lesson_obj.is_show
            lesson_dict['start_time'] = str(lesson_obj.start_time)
            lesson_dict['end_time'] = str(lesson_obj.end_time)
            lesson_dict['cost_type'] = lesson_obj.cost_type
            lesson_dict['sort_num'] = lesson_obj.sort_num
            lesson_dict['total_audio_num'] = lesson_obj.total_audio_num
            lesson_dict['location'] = i
            i += 1

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_obj.id,
                                                         LessonOrder.is_pay == 1).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            # 课程生成二维码的数量(邀友听课)
            listen_bron_qr_num = 0
            now = datetime.datetime.now()
            # l_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 1).first()
            l_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 1,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if l_bron_qr:
                listen_bron_qr_num = l_bron_qr.daily_num
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num
            else:
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num

            # 课程生成二维码的数量(邀友鼓励)
            help_bron_qr_num = 0
            # h_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 2).first()
            h_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 2,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if h_bron_qr:
                help_bron_qr_num = h_bron_qr.daily_num
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num
            else:
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num

            # 识别课程二维码的数量(邀友听课)
            listen_scan_qr_num = 0
            # l_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 1).first()
            l_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 1,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if l_scan_qr:
                listen_scan_qr_num = l_scan_qr.daily_num
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num
            else:
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num

            # 识别课程二维码的数量(邀友鼓励)
            help_scan_qr_num = 0
            # h_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 2).first()
            h_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 2,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if h_scan_qr:
                help_scan_qr_num = h_scan_qr.daily_num
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num
            else:
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num

            # 识别课程二维码的总数
            lesson_dict['scan_qr_num'] = listen_scan_qr_num + help_scan_qr_num
            lesson_list.append(lesson_dict)

        return jsonify(errno=0, errmsg="OK", count=count, data=lesson_list)

    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='文章搜索失败')


# pc全部课程列表(上架和未上架)
@api_lesson.route('/pc_lessons', methods=['POST'])
@login_required
def pc_lessons():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 10)
        is_show = params.get('is_show')
        user_id = g.user_id

        print('请求参数：', request.data)
        user_obj = Admin.query.get(user_id)
        is_admin = user_obj.is_admin
        if is_show is not None:
            try:
                is_show = int(is_show)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='is_show错误')

            try:
                is_show = int(is_show)
                if is_show not in [0, 1]:
                    return jsonify(errno=-1, errmsg='is_show参数错误')
            except Exception as e:
                print(e)

            if is_admin == 1:
                lessons = NewLesson.query.filter(NewLesson.is_show == is_show).order_by(NewLesson.sort_num).all()
            else:
                lessons = NewLesson.query.filter(NewLesson.is_show == is_show, NewLesson.admin_id == user_id).order_by(
                    NewLesson.sort_num).all()

        else:
            if is_admin == 1:
                lessons = NewLesson.query.order_by(NewLesson.sort_num).all()
            else:
                lessons = NewLesson.query.filter(NewLesson.admin_id == user_id).order_by(NewLesson.sort_num).all()

        count = len(lessons)
        lessons = lessons[(page - 1) * pagesize:page * pagesize]
        lesson_list = list()
        i = (page - 1) * pagesize + 1
        for lesson_obj in lessons:
            lesson_dict = dict()
            lesson_dict['lesson_id'] = "KC" + str(lesson_obj.id).zfill(6)
            lesson_dict['id'] = lesson_obj.id
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['author'] = lesson_obj.author
            lesson_dict['count'] = lesson_obj.count
            lesson_dict['summary'] = lesson_obj.summary
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['is_show'] = lesson_obj.is_show
            # lesson_dict['start_time'] = str(lesson_obj.start_time)
            lesson_dict['end_time'] = str(lesson_obj.end_time)
            lesson_dict['cost_type'] = lesson_obj.cost_type
            lesson_dict['sort_num'] = lesson_obj.sort_num
            lesson_dict['location'] = i
            i += 1

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

            # 已购买人数
            buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_obj.id,
                                                         LessonOrder.is_pay == 1).all()
            buy_num = len(buy_lesson_orders)
            lesson_dict['buy_num'] = buy_num + lesson_obj.base_num

            # 课程所属类型
            objs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_obj.id).all()
            type_id_list = list()
            for obj in objs:
                type_id_list.append(obj.type_id)

            type_list = list()
            for type_id in type_id_list:
                type_obj = Lesson_type.query.get(type_id)
                type_dict = dict()
                type_dict['type_id'] = type_id
                type_dict['name'] = type_obj.name
                type_list.append(type_dict)
            lesson_dict['type_info'] = type_list

            # 课程生成二维码的数量(邀友听课)
            listen_bron_qr_num = 0
            now = datetime.datetime.now()
            # l_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 1).first()
            l_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 1,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if l_bron_qr:
                listen_bron_qr_num = l_bron_qr.daily_num
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num
            else:
                lesson_dict['listen_bron_qr_num'] = listen_bron_qr_num

            # 课程生成二维码的数量(邀友鼓励)
            help_bron_qr_num = 0
            # h_bron_qr = BornQrNum.query.filter(BornQrNum.lesson_id == lesson_obj.id, BornQrNum.btn == 2).first()
            h_bron_qr = DailyBornQrNum.query.filter(DailyBornQrNum.lesson_id == lesson_obj.id,
                                                    DailyBornQrNum.btn == 2,
                                                    DailyBornQrNum.record_time == now.date()).first()
            if h_bron_qr:
                help_bron_qr_num = h_bron_qr.daily_num
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num
            else:
                lesson_dict['help_bron_qr_num'] = help_bron_qr_num

            # 识别课程二维码的数量(邀友听课)
            listen_scan_qr_num = 0
            # l_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 1).first()
            l_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 1,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if l_scan_qr:
                listen_scan_qr_num = l_scan_qr.daily_num
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num
            else:
                lesson_dict['listen_scan_qr_num'] = listen_scan_qr_num

            # 识别课程二维码的数量(邀友鼓励)
            help_scan_qr_num = 0
            # h_scan_qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_obj.id, ScanQrNum.btn == 2).first()
            h_scan_qr = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_obj.id,
                                                    DailyScanQrNum.btn == 2,
                                                    DailyScanQrNum.record_time == now.date()).first()
            if h_scan_qr:
                help_scan_qr_num = h_scan_qr.daily_num
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num
            else:
                lesson_dict['help_scan_qr_num'] = help_scan_qr_num

            # 识别课程二维码的总数
            lesson_dict['scan_qr_num'] = listen_scan_qr_num + help_scan_qr_num

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc课程详情
@api_lesson.route('/pc_lesson_detail', methods=['POST'])
@login_required
def pc_lesson_detail():
    params = request.get_json()
    lesson_id = params.get('lesson_id')

    print("请求参数:", request.data)
    if lesson_id:
        try:
            lesson_id = int(lesson_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='lesson_id错误')
    else:
        return jsonify(errno=-1, errmsg='lesson_id参数缺失')
    try:
        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='课程不存在')
        else:
            lesson_dict = dict()
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['author'] = lesson_obj.author
            lesson_dict['count'] = lesson_obj.count
            lesson_dict['summary'] = lesson_obj.summary
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['price'] = lesson_obj.price
            lesson_dict['lesson_id'] = lesson_obj.id
            lesson_dict['is_show'] = lesson_obj.is_show
            lesson_dict['start_time'] = str(lesson_obj.start_time)
            lesson_dict['end_time'] = str(lesson_obj.end_time)
            lesson_dict['cost_type'] = lesson_obj.cost_type
            lesson_dict['present_num'] = lesson_obj.present_num
            lesson_dict['base_num'] = lesson_obj.base_num
            lesson_dict['total_audio_num'] = lesson_obj.total_audio_num

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

        return jsonify(errno=0, errmsg='查询成功', data=lesson_dict)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc上架课程
@api_lesson.route('/upload_lessons', methods=['POST'])
@login_required
def upload_lessons():
    try:
        params = request.get_json()
        lesson_id_list = params.get('lesson_id_list')
        type_id_list = params.get('type_id_list')
        end_time = params.get('end_time')
        admin_id = g.user_id

        print('请求参数：', request.data)
        if not all([lesson_id_list, type_id_list]):
            return jsonify(errno=-1, errmsg='参数不完整')

        for type_id in type_id_list:
            type_obj = Lesson_type.query.get(type_id)
            if not type_obj:
                return jsonify(errno=-1, errmsg='课程类型不存在', type_id=type_id)

            for lesson_id in lesson_id_list:
                lesson_obj = NewLesson.query.get(lesson_id)
                if not lesson_obj:
                    return jsonify(errno=-1, errmsg='课程不存在', lesson_id=lesson_id)

                result = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id,
                                                     LessonTypeShip.lesson_id == lesson_id).first()
                if result:
                    return jsonify(errno=-1, errmsg='该课程已上架', lesson_id=lesson_id)

                results = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).all()
                for res in results:
                    res.sort_num += 1
                    db.session.add(res)

                obj = LessonTypeShip()
                obj.lesson_id = lesson_id
                obj.type_id = type_id
                obj.sort_num = 1
                lesson_obj.is_show = 1
                lesson_obj.admin_id = admin_id
                if end_time:
                    lesson_obj.end_time = end_time
                db.session.add(lesson_obj)
                db.session.add(obj)

                # 记录小程序课程有更新,发送通知
                records = UserBTN.query.filter(UserBTN.btn_num == 2).all()
                for record in records:
                    record.is_new = 1
                    record.is_send = 0
                    db.session.add(record)

                # 记录更新的时间
                today = datetime.datetime.today().date()
                up_obj = UpdateTime.query.filter(UpdateTime.type == 3).filter(
                    UpdateTime.create_time.like(str(today) + "%")).first()
                if not up_obj:
                    time_obj = UpdateTime()
                    time_obj.type = 3
                    db.session.add(time_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc下架课程
@api_lesson.route('/down_lessons', methods=['POST'])
@login_required
def down_lessons():
    try:
        params = request.get_json()
        lesson_id_list = params.get('lesson_id_list')
        type_id = params.get('type_id')
        admin_id = g.user_id

        print('请求参数：', request.data)
        if not lesson_id_list:
            return jsonify(errno=-1, errmsg="参数错误,请传入下线的文章ID")

        if type_id:
            # 传type_id
            # 下线当前课程所在的当前类型
            type_obj = Lesson_type.query.get(type_id)
            if not type_obj:
                return jsonify(errno=-1, errmsg="参数错误,该分类不存在")

            for lesson_id in lesson_id_list:
                print('lesson_id:', lesson_id)
                lesson_obj = NewLesson.query.get(lesson_id)
                if not lesson_obj:
                    return jsonify(errno=-1, errmsg="参数错误,该课程不存在", lesson_id=lesson_id)

                if lesson_obj.is_show == 0:
                    return jsonify(errno=-1, errmsg="参数错误,该课程未上线", lesson_id=lesson_id)

                obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id,
                                                  LessonTypeShip.lesson_id == lesson_id).first()
                if not obj:
                    return jsonify(errno=-1, errmsg="该课程已上线，但不在该分类", lesson_id=lesson_id)

                results = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).all()
                for res in results:
                    if res.sort_num > obj.sort_num:
                        res.sort_num -= 1
                        db.session.add(res)

                db.session.delete(obj)
                types = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id).all()
                num = len(types)
                print('num:', num)
                if num == 0:
                    lesson_obj.is_show = 0
                    lesson_obj.admin_id = admin_id
                    db.session.add(lesson_obj)

        else:
            # 不传type_id 下线当前课程所在的全部类型
            for lesson_id in lesson_id_list:
                lesson_obj = NewLesson.query.get(lesson_id)
                if not lesson_obj:
                    return jsonify(errno=-1, errmsg="参数错误,该课程不存在", lesson_id=lesson_id)

                if lesson_obj.is_show == 0:
                    return jsonify(errno=-1, errmsg="参数错误,该课程未上线", lesson_id=lesson_id)

                objs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id).all()
                for obj in objs:
                    # 修改当前类型下所属课程的sort_num
                    lessons = LessonTypeShip.query.filter(LessonTypeShip.type_id == obj.type_id).all()
                    for lesson in lessons:
                        if lesson.sort_num > obj.sort_num:
                            lesson.sort_num -= 1
                            db.session.add(lesson)

                    db.session.delete(obj)
                lesson_obj.is_show = 0
                lesson_obj.admin_id = admin_id
                db.session.add(lesson_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc删除课程
@api_lesson.route('/delete_lesson', methods=['POST'])
@login_required
def delete_lesson():
    try:
        params = request.get_json()
        lesson_id_list = params.get('lesson_id_list')
        user_id = g.user_id

        print('请求参数：', request.data)
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        user_obj = Admin.query.get(user_id)
        if not lesson_id_list:
            return jsonify(errno=-1, errmsg='前传入要删除的课程的ID')

        for lesson_id in lesson_id_list:
            try:
                lesson_id = int(lesson_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='lesson_id错误')

            lesson_obj = NewLesson.query.filter(NewLesson.id == lesson_id).first()
            if lesson_obj:
                lesson_order = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id).first()
                if lesson_order:
                    return jsonify(errno=-1, errmsg='课程ID为%s的课程已有人参与，禁止删除' % lesson_id)
                else:
                    # 修改sort_num
                    results = NewLesson.query.all()
                    for result in results:
                        if result.sort_num > lesson_obj.sort_num:
                            result.sort_num -= 1
                            db.session.add(result)
                    db.session.delete(lesson_obj)
                    print('管理员%s在%s删除了ID为%s的课程,课程标题是:%s' % (user_obj.username, now, lesson_obj.id, lesson_obj.title))

                    results = Audio.query.filter(Audio.lesson_id == lesson_id).all()
                    if results:
                        for result in results:
                            db.session.delete(result)

                    db.session.commit()
                    print('删除成功')
                    return jsonify(errno=0, errmsg='删除课程成功')
            else:
                return jsonify(errno=-1, errmsg='课程不存在')

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC上线分类课程移动位置
@api_lesson.route('/lesson_move', methods=['POST'])
@login_required
@admin_required
def lesson_move():
    try:
        res = request.get_json()
        sort_num = res.get('sort_num')
        lesson_id = res.get('lesson_id')
        type_id = res.get('type_id')
        move = res.get('move')  # 1,上移 2,下移 3,移至顶部 4,移至底部
        admin_id = g.user_id

        print('请求参数：', request.data)
        if not all([sort_num, lesson_id, move, type_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            lesson_id = int(lesson_id)
            sort_num = int(sort_num)
            move = int(move)
            type_id = int(type_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        if move not in [1, 2, 3, 4]:
            return jsonify(errno=-1, errmsg='move值错误')

        type_obj = Lesson_type.query.get(type_id)
        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj or sort_num <= 0 or not type_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if lesson_obj.is_show != 1:
            return jsonify(errno=-1, errmsg='该课程未上线')

        if type_obj.is_show != 1 and type_obj.is_show != 2:
            return jsonify(errno=-1, errmsg='该分类未启用')

        lesson_type_obj = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id,
                                                      LessonTypeShip.type_id == type_id).first()
        if not lesson_type_obj:
            return jsonify(errno=-1, errmsg='该课程不在该分类')

        if lesson_type_obj.sort_num != sort_num:
            return jsonify(errno=-1, errmsg='传入的该课程的sort_num错误')

        results = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id).all()
        if move == 1:
            # 上移
            sort_num = sort_num - 1
            to_lesson_obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id,
                                                        LessonTypeShip.sort_num == sort_num).first()
            to_lesson_obj.sort_num += 1
            db.session.add(to_lesson_obj)

            lesson_type_obj.sort_num = sort_num
            # db.session.add(lesson_type_obj)

        elif move == 2:
            # 下移
            sort_num = sort_num + 1
            to_lesson_obj = LessonTypeShip.query.filter(LessonTypeShip.type_id == type_id,
                                                        LessonTypeShip.sort_num == sort_num).first()
            to_lesson_obj.sort_num -= 1
            db.session.add(to_lesson_obj)

            lesson_type_obj.sort_num = sort_num
            # db.session.add(lesson_type_obj)

        elif move == 3:
            # 移至顶部
            sort_num = 1
            for result in results:
                result.sort_num += 1
                db.session.add(result)

            lesson_type_obj.sort_num = sort_num
            # db.session.add(lesson_type_obj)

        elif move == 4:
            # 移至底部
            for result in results:
                if result.sort_num >= sort_num:
                    result.sort_num -= 1
                    db.session.add(result)

            sort_num = len(results)
            lesson_type_obj.sort_num = sort_num

        lesson_type_obj.admin_id = admin_id
        db.session.add(lesson_type_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc新增免费听课程
@api_lesson.route('/add_free_lesson', methods=['POST'])
@login_required
def add_free_lesson():
    try:
        params = request.get_json()
        free_sort_num = params.get('free_sort_num', 1)
        title = params.get('title')
        lesson_id_list = params.get('lesson_id_list')
        admin_id = g.user_id

        print('请求参数：', request.data)
        if not all([lesson_id_list, free_sort_num, title]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            free_sort_num = int(free_sort_num)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        for lesson_id in lesson_id_list:
            try:
                lesson_id = int(lesson_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='lesson_id错误')

            lesson_obj = NewLesson.query.get(lesson_id)

            docs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id).all()
            if docs:
                return jsonify(errno=-1, errmsg='该课程:%s 已经上架为积赞课程' % lesson_obj.title)

            results = NewLesson.query.filter(NewLesson.cost_type == 3).all()
            total_num = len(results) + 1
            if free_sort_num > total_num:
                return jsonify(errno=-1, errmsg='参数错误,传入的free_sort_num值超出范围')

            for result in results:
                if result.free_sort_num >= free_sort_num:
                    result.free_sort_num += 1
                    db.session.add(result)
                    db.session.commit()

            if lesson_obj:
                lesson_obj.cost_type = 3
                lesson_obj.is_show = 1
                lesson_obj.free_sort_num = free_sort_num
                lesson_obj.title = title
                lesson_obj.admin_id = admin_id
                db.session.add(lesson_obj)

                db.session.commit()
                return jsonify(errno=0, errmsg='OK')
            else:
                return jsonify(errno=-1, errmsg='课程不存在')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc启用或停用免费课程
@api_lesson.route('/open_free_lesson', methods=['POST'])
@login_required
def open_free_lesson():
    try:
        res = request.get_json()
        lesson_id = res.get('lesson_id')
        admin_id = g.user_id

        print('请求参数：', request.data)
        try:
            lesson_id = int(lesson_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='课程不存在')

        if lesson_obj.cost_type != 3:
            return jsonify(errno=-1, errmsg='该课程不是免费课程', lesson_id=lesson_id)

        if lesson_obj.is_open == 0:
            # 启用
            lesson_obj.is_open = 1

            # 记录小程序课程有更新,发送通知
            records = UserBTN.query.filter(UserBTN.btn_num == 2).all()
            for record in records:
                record.is_new = 1
                record.is_send = 0
                db.session.add(record)

            # 记录更新的时间
            today = datetime.datetime.today().date()
            up_obj = UpdateTime.query.filter(UpdateTime.type == 3).filter(
                UpdateTime.create_time.like(str(today) + "%")).first()
            if not up_obj:
                time_obj = UpdateTime()
                time_obj.type = 3
                db.session.add(time_obj)

        else:
            # 停用
            lesson_obj.is_open = 0
        lesson_obj.admin_id = admin_id
        db.session.add(lesson_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='OK')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc免费听课程自定义排序
@api_lesson.route('/update_free_lesson', methods=['POST'])
@login_required
def update_free_lesson():
    try:
        res = request.get_json()
        lesson_id = res.get('lesson_id')
        title = res.get('title')
        free_sort_num = res.get('free_sort_num', 1)
        admin_id = g.user_id
        print('请求参数:', request.data)

        if not all([lesson_id, free_sort_num, title]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            lesson_id = int(lesson_id)
            free_sort_num = int(free_sort_num)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='课程不存在')

        new_lesson_obj = NewLesson.query.filter(NewLesson.title == title).first()

        if lesson_obj.id != new_lesson_obj.id:
            db.session.delete(lesson_obj)

        docs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == new_lesson_obj.id).all()
        if docs:
            return jsonify(errno=-1, errmsg='该课程已经上架为积赞课程')

        # if lesson_obj.cost_type != 3:
        #     return jsonify(errno=-1, errmsg='该课程不是免费课程', lesson_id=lesson_id)

        results = NewLesson.query.filter(NewLesson.cost_type == 3).all()
        total_num = len(results)
        if free_sort_num > total_num:
            return jsonify(errno=-1, errmsg='参数错误,传入的free_sort_num值超出范围')

        for result in results:
            # 课程往前调
            if new_lesson_obj.free_sort_num > free_sort_num:
                # 选取修改范围
                if free_sort_num <= result.free_sort_num < new_lesson_obj.free_sort_num:
                    # 先加再赋值
                    result.free_sort_num += 1
                    db.session.add(result)
            # 课程往后调
            elif new_lesson_obj.free_sort_num < free_sort_num:
                # 选取修改范围
                if new_lesson_obj.free_sort_num <= result.free_sort_num <= free_sort_num:
                    # 先加再赋值
                    result.free_sort_num -= 1
                    db.session.add(result)
            else:
                # 位置不变
                new_lesson_obj.free_sort_num = free_sort_num

        new_lesson_obj.free_sort_num = free_sort_num
        new_lesson_obj.title = title
        new_lesson_obj.cost_type = 3
        new_lesson_obj.is_show = 1
        new_lesson_obj.admin_id = admin_id

        db.session.add(new_lesson_obj)
        db.session.commit()

        return jsonify(errno=0, errmsg='OK')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC今日免费听课程列表
@api_lesson.route('/pc_free_lessons', methods=['POST'])
@login_required
def pc_free_lessons():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 10)
        user_id = g.user_id
        # user_id = 6

        print('请求参数:', request.data)
        user_obj = Admin.query.get(user_id)
        is_admin = user_obj.is_admin

        if is_admin == 1:
            lessons = NewLesson.query.filter(NewLesson.cost_type == 3).order_by(NewLesson.free_sort_num).all()
        else:
            lessons = NewLesson.query.filter(NewLesson.admin_id == user_id, NewLesson.cost_type == 3).order_by(
                NewLesson.free_sort_num).all()

        count = len(lessons)
        lessons = lessons[(page - 1) * pagesize:page * pagesize]
        lesson_list = list()
        i = (page - 1) * pagesize + 1
        for lesson_obj in lessons:
            lesson_dict = dict()
            lesson_dict['lesson_id'] = lesson_obj.id
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['cost_type'] = lesson_obj.cost_type
            lesson_dict['free_sort_num'] = lesson_obj.free_sort_num
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['is_open'] = lesson_obj.is_open
            lesson_dict['location'] = i
            i += 1

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc今日免费听删除
@api_lesson.route('/del_free_lesson', methods=['POST'])
@login_required
def del_free_lesson():
    try:
        params = request.get_json()
        lesson_id_list = params.get('lesson_id_list')
        admin_id = g.user_id

        print('请求参数：', request.data)
        for lesson_id in lesson_id_list:
            try:
                lesson_id = int(lesson_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='lesson_id错误')

            lesson_obj = NewLesson.query.get(lesson_id)
            if not lesson_obj:
                return jsonify(errno=-1, errmsg='课程不存在')

            objs = LessonTypeShip.query.filter(LessonTypeShip.lesson_id == lesson_id).all()
            if objs:
                # 如果该课程已上架到其他分类,下架课程所在所有分类
                for obj in objs:
                    # 修改当前类型下所属课程的sort_num
                    lessons = LessonTypeShip.query.filter(LessonTypeShip.type_id == obj.type_id).all()
                    for lesson in lessons:
                        if lesson.sort_num > obj.sort_num:
                            lesson.sort_num -= 1
                            db.session.add(lesson)
                    db.session.delete(obj)
            lesson_obj.is_show = 0
            lesson_obj.cost_type = 1
            lesson_obj.free_sort_num = 0
            lesson_obj.is_open = 0
            lesson_obj.admin_id = admin_id
            db.session.add(lesson_obj)

            results = NewLesson.query.filter(NewLesson.cost_type == 3).all()
            for result in results:
                if result.free_sort_num > lesson_obj.free_sort_num:
                    result.free_sort_num -= 1
                    db.session.add(result)

        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 新版(返回课程库,从中选取3个设置为免费)
# PC今日免费听课程列表(全部)
@api_lesson.route('/pc_new_free_lessons', methods=['POST'])
@login_required
def pc_new_free_lessons():
    try:
        params = request.get_json()
        page = params.get('page', 1)
        pagesize = params.get('pagesize', 10)
        user_id = g.user_id
        # user_id = 6

        user_obj = Admin.query.get(user_id)
        is_admin = user_obj.is_admin

        if is_admin == 1:
            lessons = NewLesson.query.all()
        else:
            lessons = NewLesson.query.filter(NewLesson.admin_id == user_id).all()

        count = len(lessons)
        lessons = lessons[(page - 1) * pagesize:page * pagesize]
        lesson_list = list()
        i = (page - 1) * pagesize + 1
        for lesson_obj in lessons:
            lesson_dict = dict()
            lesson_dict['lesson_id'] = lesson_obj.id
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['cost_type'] = lesson_obj.cost_type
            lesson_dict['free_sort_num'] = lesson_obj.free_sort_num
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['is_open'] = lesson_obj.is_open
            lesson_dict['location'] = i
            i += 1

            results = Audio.query.filter(Audio.lesson_id == lesson_obj.id).all()
            audio_num = len(results)
            lesson_dict['audio_num'] = audio_num

            if lesson_obj.cost_type == 3:
                lesson_list.insert(0, lesson_dict)
            else:
                lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='查询成功', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 新版
# pc设置免费课程
@api_lesson.route('/set_free_lessons', methods=['POST'])
@login_required
def set_free_lessons():
    try:
        res = request.get_json()
        lesson_id_list = res.get('lesson_id_list')

        if not lesson_id_list:
            return jsonify(errno=-1, errmsg='请传入要设置的课程ID')

        num = len(lesson_id_list)
        if num > 3:
            return jsonify(errno=-1, errmsg='免费课程最多只能设置3个')

        for lesson_id in lesson_id_list:
            try:
                lesson_id = int(lesson_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='参数错误', lesson_id=lesson_id)

            lesson_obj = NewLesson.query.get(lesson_id)
            if not lesson_obj:
                return jsonify(errno=-1, errmsg='当前课程不存在', lesson_id=lesson_id)

            lesson_obj.cost_type = 3
            db.session.add(lesson_obj)
        db.session.commit()

        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--今日免费听
@api_lesson.route('/today_free_lessons')
def today_free_lessons():
    try:
        results = NewLesson.query.filter(NewLesson.cost_type == 3, NewLesson.is_open == 1).order_by(
            NewLesson.free_sort_num).all()
        count = len(results)
        lesson_list = list()
        for result in results:
            lesson_dict = dict()
            lesson_dict['lesson_id'] = result.id
            lesson_dict['title'] = result.title
            lesson_dict['min_pic'] = result.min_pic
            audios_list = list()
            audios = Audio.query.filter(Audio.lesson_id == result.id).all()
            for audio in audios:
                audio_dict = dict()
                audio_dict['audio_id'] = audio.id
                audio_dict['title'] = audio.title
                audio_dict['mp3_url'] = audio.mp3_url
                audios_list.append(audio_dict)
            lesson_dict['audios_list'] = audios_list
            lesson_list.append(lesson_dict)
        return jsonify(errno=0, errmsg='ok', lesson_list=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')
