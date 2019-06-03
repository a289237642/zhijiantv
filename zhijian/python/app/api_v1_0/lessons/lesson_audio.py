# -*- coding:utf-8 -*-
# author: will
import datetime
import time

from flask import request, jsonify, g

from app import db
from app.models import NewLesson, Audio, LessonOrder, UpdateTime
from celery_tasks.tasks import upload_file
from utils.user_service.login import login_required
from . import api_lesson


# 上传课程语音
@api_lesson.route('/upload_audio', methods=['POST'])
@login_required
def upload_lesson():
    try:
        start_time = time.time()
        print('开始时间:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
        mp3_file = request.files.get('file')
        now = int(time.time())
        print(now)
        # mp3_file.save('../storage/media/lesson/%s.mp3' % str(now))
        mp3_file.save('/www/zjdev/zhijian_live_miniprogram/storage/media/lesson/%s.mp3' % str(now))

        # mp3_url = 'https://zj-live-dev.max-digital.cn/storage/media/lesson/%s.mp3' % str(now)
        # oss = Ossupload()
        # mp3_url = oss.uploadfile(str(now) + ".mp3", mp3_file)

        mp3_url = 'https://maxpr.oss-cn-shanghai.aliyuncs.com/miniprogram/zjlive/download/mp3/%s.mp3' % str(now)
        upload_file.delay(str(now) + ".mp3")

        end_time = time.time()
        print('结束时间:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
        use_time = end_time - start_time
        print('音频上传时间:', use_time)
        return jsonify(errno=0, errmsg="OK", mp3_url=mp3_url)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='上传mp3失败')


# 新增/修改课程音频
@api_lesson.route('/add_lesson_audio', methods=['POST'])
@login_required
def add_lesson_audio():
    try:
        params = request.get_json()
        lesson_id = params.get('lesson_id')
        name = params.get('name')
        title = params.get('title')
        mp3_url = params.get('mp3_url')
        audio_id = params.get('audio_id')
        admin_id = g.user_id

        print("请求参数:", request.data)
        if not all([lesson_id, name, title, mp3_url]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            lesson_id = int(lesson_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='lesson_id参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='当前课程不存在')

        if not audio_id:
            # 新增
            results = Audio.query.filter(Audio.lesson_id == lesson_id).all()
            if results:
                for result in results:
                    result.sort_num += 1
                    db.session.add(result)

            audio_obj = Audio()
            audio_obj.name = name
            audio_obj.title = title
            audio_obj.mp3_url = mp3_url
            audio_obj.lesson_id = lesson_id
            audio_obj.sort_num = 1
            audio_obj.admin_id = admin_id
            lesson_obj.lesson_update_time = datetime.datetime.now()
            db.session.add(audio_obj)
            db.session.add(lesson_obj)

            # 课程音频新增时,通知已购该课程的用户
            orders = LessonOrder.query.filter(LessonOrder.is_pay == 1, LessonOrder.lesson_id == lesson_id).all()
            if orders:
                # 同一个课程在当日内只记录一次且发一次通知
                today = datetime.datetime.today().date()
                up_obj = UpdateTime.query.filter(UpdateTime.type == 2).filter(
                    UpdateTime.create_time.like(str(today) + "%")).first()

                if up_obj:
                    # 今天已经有更新记录
                    for order in orders:
                        if order.is_send == 0:
                            order.is_new = 1
                            order.lesson_update_time = datetime.datetime.now()
                            db.session.add(order)
                else:
                    # 今天还没更新记录
                    for order in orders:
                        order.is_new = 1
                        order.lesson_update_time = datetime.datetime.now()
                        db.session.add(order)

                    time_obj = UpdateTime()
                    time_obj.type = 2
                    db.session.add(time_obj)

        else:
            # 修改
            try:
                audio_id = int(audio_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='audio_id参数错误')

            audio_obj = Audio.query.get(audio_id)
            if not audio_obj:
                return jsonify(errno=-1, errmsg='当前音频不存在')

            audio_obj.name = name
            audio_obj.title = title
            audio_obj.mp3_url = mp3_url
            audio_obj.lesson_id = lesson_id
            audio_obj.admin_id = admin_id
            db.session.add(audio_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# pc课程的音频列表
@api_lesson.route('/lesson_audio_list', methods=['POST'])
@login_required
def lesson_audio_list():
    try:
        res = request.get_json()
        lesson_id = res.get('lesson_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        print("请求参数:", request.data)
        if not lesson_id:
            return jsonify(errno=-1, errmsg='请传入lesson_id')
        try:
            lesson_id = int(lesson_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='lesson_id参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='当前课程不存在')

        results = Audio.query.filter(Audio.lesson_id == lesson_id).order_by(Audio.sort_num.asc()).all()
        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]
        # location = (page - 1) * pagesize + 1
        location = count
        audio_list = list()
        for result in results:
            audio_dict = dict()
            audio_dict['id'] = result.id
            audio_dict['name'] = result.name
            audio_dict['title'] = result.title
            audio_dict['mp3_url'] = result.mp3_url
            audio_dict['sort_num'] = result.sort_num
            audio_dict['location'] = location
            location = location - 1
            audio_list.append(audio_dict)

        return jsonify(errno=0, errmsg='ok', data=audio_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--课程的音频列表
@api_lesson.route('/lesson_audio_ls', methods=['POST'])
def lesson_audio_ls():
    try:
        res = request.get_json()
        lesson_id = res.get('lesson_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        print("请求参数:", request.data)
        if not lesson_id:
            return jsonify(errno=-1, errmsg='请传入lesson_id')
        try:
            lesson_id = int(lesson_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='lesson_id参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='当前课程不存在')

        results = Audio.query.filter(Audio.lesson_id == lesson_id).order_by(Audio.sort_num.desc()).all()
        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]

        audio_list = list()
        for result in results:
            audio_dict = dict()
            audio_dict['id'] = result.id
            audio_dict['name'] = result.name
            audio_dict['title'] = result.title
            audio_dict['mp3_url'] = result.mp3_url
            # audio_dict['sort_num'] = result.sort_num
            audio_list.append(audio_dict)

        return jsonify(errno=0, errmsg='ok', data=audio_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc删除课程音频
@api_lesson.route('/del_lesson_audio', methods=['POST'])
@login_required
def del_lesson_audio():
    try:
        params = request.get_json()
        lesson_id = params.get('lesson_id')
        audio_id_list = params.get('audio_id_list')

        print("请求参数:", request.data)
        if not all([lesson_id, audio_id_list]):
            return jsonify(errno=-1, errmsg='参数不完整')

        if isinstance(audio_id_list, list):

            try:
                lesson_id = int(lesson_id)
            except Exception as e:
                print(e)
                return jsonify(errno=-1, errmsg='lesson_id错误')

            lesson_obj = NewLesson.query.filter(NewLesson.id == lesson_id).first()
            if not lesson_obj:
                return jsonify(errno=-1, errmsg='课程不存在')
            else:
                lesson_order = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id).first()
                if lesson_order:
                    return jsonify(errno=-1, errmsg='该课程已有人领取，禁止删除')
                else:
                    for audio_id in audio_id_list:
                        audio_obj = Audio.query.get(audio_id)
                        if not audio_obj:
                            return jsonify(errno=-1, errmsg='参数错误,audio_id:%s不存在' % audio_id)

                        lesson_audio = Audio.query.filter(Audio.lesson_id == lesson_id,
                                                          Audio.id == audio_id).first()
                        if not lesson_audio:
                            return jsonify(errno=-1, errmsg='ID为%s的音频不存在当前课程中' % audio_id)

                        # 修改sort_num
                        results = Audio.query.filter(Audio.lesson_id == lesson_id).all()
                        for result in results:
                            if result.sort_num > lesson_audio.sort_num:
                                result.sort_num -= 1
                                db.session.add(result)

                        db.session.delete(audio_obj)

                    db.session.commit()
                    return jsonify(errno=0, errmsg='OK')
        else:
            return jsonify(errno=-1, errmsg='参数错误')

    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 移动音频
@api_lesson.route('/audio_move', methods=['POST'])
@login_required
def audio_move():
    try:
        res = request.get_json()
        sort_num = res.get('sort_num')
        audio_id = res.get('audio_id')
        lesson_id = res.get('lesson_id')
        move = res.get('move')  # 1,上移 2,下移 3,移至顶部 4,移至底部
        admin_id = g.user_id

        print("请求参数:", request.data)
        if not all([sort_num, audio_id, move, lesson_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            audio_id = int(audio_id)
            sort_num = int(sort_num)
            lesson_id = int(lesson_id)
            move = int(move)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='该课程不存在')

        audio_obj = Audio.query.filter(Audio.id == audio_id, Audio.sort_num == sort_num).first()
        if not audio_obj or sort_num <= 0:
            return jsonify(errno=-1, errmsg='参数错误')

        results = Audio.query.filter(Audio.lesson_id == lesson_id).all()
        if move == 1:
            sort_num = sort_num - 1
            to_audio_obj = Audio.query.filter(Audio.lesson_id == lesson_id, Audio.sort_num == sort_num).first()
            to_audio_obj.sort_num += 1
            db.session.add(to_audio_obj)

            audio_obj.sort_num = sort_num

        elif move == 2:
            sort_num = sort_num + 1
            to_audio_obj = Audio.query.filter(Audio.lesson_id == lesson_id, Audio.sort_num == sort_num).first()
            to_audio_obj.sort_num -= 1
            db.session.add(to_audio_obj)

            audio_obj.sort_num = sort_num

        elif move == 3:
            sort_num = 1
            for result in results:
                result.sort_num += 1
                db.session.add(result)

            audio_obj.sort_num = sort_num

        elif move == 4:
            for result in results:
                if result.sort_num >= sort_num:
                    result.sort_num -= 1
                    db.session.add(result)

            sort_num = len(results)
            audio_obj.sort_num = sort_num

        audio_obj.admin_id = admin_id
        db.session.add(audio_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
