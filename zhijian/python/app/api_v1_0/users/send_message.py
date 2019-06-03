# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import time

from flask import jsonify, request

from app import db
from app.models import User, LessonOrder, NewLesson, UserFormID, UserBTN, UpdateTime, Banner, Article
from utils.log_service import Logging
from utils.user_service.login import auth_required
from utils.user_service.send_msg import send_msg, first_send, second_send, third_send, new_article_update_inform, \
    wechat_steps_inform, new_sign_in_user_push
from utils.time_service import dif_time, get_today
from . import api_user


# 用户本人点击直接发送模板信息
@api_user.route('/send_template_msg', methods=['POST'])
def send_template_msg():
    try:
        res = request.get_json()
        template_id = res.get('template_id')
        openid = res.get('openid')
        form_id = res.get('form_id')
        data = res.get('data')
        page = res.get('page')

        print(('请求参数:', request.data))

        if not all([template_id, openid, form_id, data, page]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.filter(User.openid == openid).first()
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        result = send_msg(template_id, openid, page, form_id, data)
        print(('返回结果:', result))
        print((result.json()))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg="网络异常")


# 小程序--收集保存用户推送码
@api_user.route('/save_template', methods=['POST'])
# @auth_required
def save_template():
    try:
        res = request.get_json()
        openid = res.get('openid')
        form_id = res.get('form_id')

        if not all([openid, form_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        Logging.logger.info('request_args:{0}'.format(res))
        user_obj = User.query.filter(User.openid == openid).first()
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')
        user_id = user_obj.id

        form_obj = UserFormID()
        form_obj.user_id = user_id
        form_obj.openid = openid
        form_obj.form_id = form_id
        db.session.add(form_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg="网络异常")


# 小程序--收集用户btn
@api_user.route('/save_btn', methods=['POST'])
# @auth_required
def save_btn():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        btn_num = res.get('btn_num')

        if not all([user_id, btn_num]):
            return jsonify(errno=-1, errmsg='参数不完整')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            user_id = int(user_id)
            btn_num = int(btn_num)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.filter(User.id == user_id).first()
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        today = get_today()
        res = UserBTN.query.filter(UserBTN.user_id == user_id, UserBTN.btn_num == btn_num,
                                   UserBTN.create_time >= today).first()
        if not res:
            obj = UserBTN()
            obj.user_id = user_id
            obj.btn_num = btn_num

            db.session.add(obj)
        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg="网络异常")


# 清除过期的formID
@api_user.route('/clear_form_id')
def clear_form_id():
    try:
        results = UserFormID.query.all()
        i = 0
        for result in results:
            create_time = result.create_time
            create_time = time.mktime(create_time.timetuple())
            now = time.time()
            if int(now) - int(create_time) > 3600 * 24 * 7:
                i += 1
                db.session.delete(result)

        Logging.logger.info('清除了{0}条过期的formID'.format(i))
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 1,检查进行中2小时内没有好友助力的订单,发送推送通知
@api_user.route('/check_no_help')
def check_no_help():
    try:
        results = LessonOrder.query.filter(LessonOrder.order_status == 1, LessonOrder.is_help == 0,
                                           LessonOrder.is_send == 0).all()
        if results:
            for result in results:
                # 时间差
                mistiming = dif_time(str(result.create_time))
                print(("mistiming=", mistiming))
                # 误差一分钟,且未发送过消息的order
                if mistiming > 3600 * 2:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                    else:
                        print(('准备向user_id=%s的用户推送2小时内没有好友助力通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        lesson_obj = NewLesson.query.get(result.lesson_id)
                        template_id = '1UMnwF_6E3aLd8Cbjl9luT0-cBIeaml-BW9e_8FTAbQ'
                        data = {'keyword1': {'value': lesson_obj.title}, 'keyword2': {'value': "暂时还没有好友为你鼓励"}}
                        # data = json.dumps(data)
                        page = 'pages/curse/getFriends/main?order_id=%s&lesson_id=%s' % (result.id, result.lesson_id)

                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 2,好友点击助力,通知本人
@api_user.route('/send_template_friend', methods=['POST'])
def send_template_friend():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        data = res.get('data')

        print(('传入的参数:', request.data))
        if not all([order_id, data]):
            return jsonify(errno=-1, errmsg='参数不完整')

        order_obj = LessonOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        form_obj = UserFormID.query.filter(UserFormID.user_id == order_obj.user_id).order_by(
            UserFormID.create_time.desc()).first()
        if not form_obj:
            print(('user_id=%s的用户FormID不足' % order_obj.user_id))
        else:
            print(('准备向user_id=%s的用户推送好友点击助力通知:' % order_obj.user_id))
            form_id = form_obj.form_id
            openid = form_obj.openid

            # template_obj = TemplateMessage.query.filter(TemplateMessage.action == 2).first()

            # user_obj = User.query.get(order_obj.user_id)
            template_id = '1UMnwF_6E3aLd8Cbjl9luT0-cBIeaml-BW9e_8FTAbQ'
            # data = {'keyword1': {'value': userinfo.nickname + "帮你助力成功了"}, 'keyword2': {'value': "暂时还没有好友为你鼓励"}}
            # data = json.dumps(data)
            page = 'pages/curse/getFriends/main?order_id=%s&lesson_id=%s' % (order_obj.id, order_obj.lesson_id)

            # template_id = template_obj.template_id
            # data = json.loads(template_obj.data)
            # page = template_obj.page

            response = send_msg(template_id, openid, page, form_id, data)
            response = response.json()
            print(('返回结果:', response))
            if response.get('errcode') == 0:
                db.session.delete(form_obj)
                db.session.commit()
                print(("推送成功:", response))
            else:
                db.session.delete(form_obj)
                db.session.commit()
                print(("推送失败:", response))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 3,检查订单状态,超过24h,助力失败,推送模板消息
@api_user.route('/check_fail_orders')
def check_fail_orders():
    try:
        results = LessonOrder.query.filter(LessonOrder.order_status == 1).all()
        if results:
            for result in results:
                help_num = result.help_num
                price = result.price
                need = int(price) - int(help_num)
                create_time = result.create_time
                create_time = time.mktime(create_time.timetuple())
                now = time.time()
                if int(now) - int(create_time) > 3600 * 24 and need > 0:
                    result.order_status = 3

                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                        db.session.add(result)
                        db.session.commit()
                    else:
                        print(('准备向user_id=%s的用户推送活动参与失败通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        lesson_obj = NewLesson.query.get(result.lesson_id)
                        template_id = 'TKse_738oD3ZoyrvjYIxU7Nl8SLyrwG1WboPx6oxpN4'
                        data = {'keyword1': {'value': "邀好友鼓励免费领取课程"},
                                'keyword2': {'value': "规定时间未集满鼓励"},
                                'keyword3': {'value': "您也可以重新发起鼓励哦~"},
                                'keyword4': {'value': lesson_obj.title}}
                        # data = json.dumps(data)
                        page = 'pages/curse/getFriends/main?order_id=%s&lesson_id=%s' % (result.id, result.lesson_id)

                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 4,活动参与成功通知
@api_user.route('/send_success_template')
def send_success_template():
    try:
        results = LessonOrder.query.filter(LessonOrder.order_status == 2, LessonOrder.is_pay == 0,
                                           LessonOrder.is_send == 0).all()
        if results:
            for result in results:
                # 推送模板消息

                form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                    UserFormID.create_time.desc()).first()
                if not form_obj:
                    print(('user_id=%s的用户FormID不足' % result.user_id))
                else:
                    print(('准备向user_id=%s的用户推送活动参与成功通知:' % result.user_id))
                    form_id = form_obj.form_id
                    openid = form_obj.openid

                    user_obj = User.query.get(result.user_id)
                    lesson_obj = NewLesson.query.get(result.lesson_id)
                    template_id = '8DtZTnt51b_kPQdlq89dY0BjNx9dJ1VCZf1nOmIBFNY'
                    data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                            'keyword2': {'value': "邀好友鼓励免费领取课程"},
                            'keyword3': {'value': lesson_obj.title},
                            'keyword4': {'value': "您的课程已经发放至您的个人中心，点击下方详情就可以直接收听啦！"}}

                    page = 'pages/curse/courseDetail/main?lesson_id=%s' % result.lesson_id

                    response = send_msg(template_id, openid, page, form_id, data)
                    response = response.json()
                    print(('返回结果:', response))
                    if response.get('errcode') == 0:
                        result.is_send = 1
                        db.session.add(result)
                        db.session.delete(form_obj)
                        db.session.commit()
                        print(("推送成功:", response))
                    else:
                        db.session.delete(form_obj)
                        db.session.commit()
                        print(("推送失败:", response))

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 5,我的已购课程更新通知/1小时后发送-->(改为当天提醒一次)
@api_user.route('/my_lesson_update')
def my_lesson_update():
    try:
        today = datetime.datetime.today().date()
        time_obj = UpdateTime.query.filter(UpdateTime.type == 2).filter(
            UpdateTime.create_time.like(str(today) + "%")).first()
        if time_obj:
            # 与当前时间的时间差
            mistiming = dif_time(str(time_obj.create_time))
            print(("mistiming=", mistiming))
            if mistiming > 3600:
                results = LessonOrder.query.filter(LessonOrder.is_pay == 1, LessonOrder.is_new == 1,
                                                   LessonOrder.is_send == 0).all()
                for result in results:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                        result.is_new = 0
                        db.session.add(result)
                        db.session.commit()
                    else:
                        print(('准备向user_id=%s的用户推送已购课程更新通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        start_time = time.time()
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

                        user_obj = User.query.get(result.user_id)
                        lesson_obj = NewLesson.query.get(result.lesson_id)
                        template_id = 'LFMuIoAgGvegGPru0AAh_P1kS44EotPMIK4L5EB14hE'
                        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                                'keyword2': {'value': now},
                                'keyword3': {'value': lesson_obj.title},
                                'keyword4': {'value': "您喜欢的课程更新啦！点我去收听~"}}
                        # data = json.loads(data)
                        page = 'pages/curse/lessonList/main?lesson_id=%s' % result.lesson_id

                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            result.is_new = 0
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))
                # if not results:
                #     # 全部推送成功
                #     time_obj.is_send = 1
                #     db.session.add(time_obj)
                #     db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 6,文章更新通知/1小时后
@api_user.route('/article_update_inform')
def article_update_inform():
    try:
        time_obj = UpdateTime.query.filter(UpdateTime.type == 1).first()
        if time_obj:
            # 与当前时间的时间差
            mistiming = dif_time(str(time_obj.create_time))
            print(("mistiming=", mistiming))
            if mistiming > 3600:
                results = UserBTN.query.filter(UserBTN.btn_num == 1, UserBTN.is_send == 0, UserBTN.is_new == 1).all()
                for result in results:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                    else:
                        print(('准备向user_id=%s的用户推送文章更新通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        start_time = time.time()
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

                        user_obj = User.query.get(result.user_id)
                        template_id = 'LFMuIoAgGvegGPru0AAh_BXZXHQD-tLahF8Ao20etKA'
                        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                                'keyword2': {'value': "您喜欢的有声节目更新啦！点我去收听！"},
                                'keyword3': {'value': now}}
                        # data = json.loads(data)
                        page = 'pages/tipoff/tipofflist/main'

                        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            result.is_new = 0
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))
                if not results:
                    # 全部推送成功再删除
                    db.session.delete(time_obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 7,免费领课内容更新通知/1小时后
@api_user.route('/lesson_update_inform')
def lesson_update_inform():
    try:
        time_obj = UpdateTime.query.filter(UpdateTime.type == 3).first()
        if time_obj:
            # 与当前时间的时间差
            mistiming = dif_time(str(time_obj.create_time))
            print(("mistiming=", mistiming))
            if mistiming > 3600:
                results = UserBTN.query.filter(UserBTN.btn_num == 2, UserBTN.is_send == 0, UserBTN.is_new == 1).all()
                for result in results:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                    else:
                        print(('准备向user_id=%s的用户推送免费领课内容更新通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        start_time = time.time()
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

                        user_obj = User.query.get(result.user_id)
                        template_id = 'LFMuIoAgGvegGPru0AAh_LR-Z62gzyBgBlQXF3ekYfg'
                        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                                'keyword2': {'value': "免费听课"},
                                'keyword3': {'value': "课程表又更新啦！快点我去给自己充电吧！"},
                                'keyword4': {'value': now}}

                        # data = json.loads(data)
                        page = 'pages/curse/freeCourse/main'

                        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            result.is_new = 0
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))
                if not results:
                    # 全部推送成功再删除
                    db.session.delete(time_obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 8,24h热榜更新通知/1小时后
@api_user.route('/tops_update_inform')
def tops_update_inform():
    try:
        time_obj = UpdateTime.query.filter(UpdateTime.type == 4).first()
        if time_obj:
            # 与当前时间的时间差
            mistiming = dif_time(str(time_obj.create_time))
            print(("mistiming=", mistiming))
            if mistiming > 3600:
                results = UserBTN.query.filter(UserBTN.btn_num == 3, UserBTN.is_send == 0, UserBTN.is_new == 1).all()
                for result in results:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                    else:
                        print(('准备向user_id=%s的用户推送免费领课内容更新通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        start_time = time.time()
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

                        user_obj = User.query.get(result.user_id)
                        template_id = 'LFMuIoAgGvegGPru0AAh_O0sh6x2V_eBDX2pps8QpCY'
                        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                                'keyword2': {'value': now},
                                'keyword3': {'value': "您经常浏览的24h热榜更新啦，快点我去看看过去24小时都发生了什么"}}
                        # data = json.loads(data)
                        page = 'pages/tipoff/companyheadline/main'

                        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
                        response = send_msg(template_id, openid, page, form_id, data)
                        response = response.json()
                        print(('返回结果:', response))
                        if response.get('errcode') == 0:
                            result.is_send = 1
                            result.is_new = 0
                            db.session.add(result)
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送成功:", response))
                        else:
                            db.session.delete(form_obj)
                            db.session.commit()
                            print(("推送失败:", response))
                if not results:
                    # 全部推送成功再删除
                    db.session.delete(time_obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 9,第一个banner图更新通知/30分钟后
@api_user.route('/banner_update_inform')
def banner_update_inform():
    try:
        time_obj = UpdateTime.query.filter(UpdateTime.type == 5).first()
        if time_obj:
            # 与当前时间的时间差
            mistiming = dif_time(str(time_obj.create_time))
            print(("mistiming=", mistiming))
            if mistiming > 1800:
                results = UserBTN.query.filter(UserBTN.btn_num == 4, UserBTN.is_send == 0, UserBTN.is_new == 1).all()
                for result in results:
                    # 推送模板消息
                    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
                        UserFormID.create_time.desc()).first()
                    if not form_obj:
                        print(('user_id=%s的用户FormID不足' % result.user_id))
                        db.session.delete(result)
                        db.session.commit()
                    else:
                        print(('准备向user_id=%s的用户推送第一个banner图更新通知:' % result.user_id))
                        form_id = form_obj.form_id
                        openid = form_obj.openid

                        banner = Banner.query.filter_by(status=1).order_by(Banner.sort.asc()).first()
                        if banner:
                            article = Article.query.get(banner.article_id)

                            user_obj = User.query.get(result.user_id)
                            template_id = 'LFMuIoAgGvegGPru0AAh_BBpX72aaJfRf0-LG3-YJzo'
                            data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                                    'keyword2': {'value': '您订阅的今日热文更新啦！'},
                                    'keyword3': {'value': article.title}}
                            page = 'pages/tipoff/tipoffcontent/main?arc_id=%s' % article.id

                            # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
                            response = send_msg(template_id, openid, page, form_id, data)
                            response = response.json()
                            print(('返回结果:', response))
                            if response.get('errcode') == 0:
                                result.is_send = 1
                                result.is_new = 0
                                db.session.add(result)
                                db.session.delete(form_obj)
                                db.session.commit()
                                print(("推送成功:", response))
                            else:
                                db.session.delete(form_obj)
                                db.session.commit()
                                print(("推送失败:", response))
                if not results:
                    # 全部推送成功再删除
                    db.session.delete(time_obj)
                    db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 10,更新通知/1天后12点/2天后9点/3天后12点
# @api_user.route('/update_inform')
# def update_inform():
#     try:
#         results = UserBTN.query.filter(UserBTN.btn_num == 5).all()
#         # 用户有点击相应btn, 指定时间发通知
#         if results:
#             now = datetime.datetime.now()
#             print '当前时间:', now.strftime('%Y-%m-%d %H:%M:%S')
#             for result in results:
#                 # 推送模板消息
#                 # 1天后/12点发通知
#                 print '用户第一次点击时间:', str(result.create_time)
#                 first_time = result.create_time + datetime.timedelta(days=+1)
#                 second_time = result.create_time + datetime.timedelta(days=+2)
#                 third_time = result.create_time + datetime.timedelta(days=+3)
#                 # first_time = result.create_time + datetime.timedelta(minutes=+3)
#                 # second_time = result.create_time + datetime.timedelta(minutes=+5)
#                 # third_time = result.create_time + datetime.timedelta(minutes=+10)
#
#                 # if first_time.day == now.day and first_time.minute == now.minute:
#                 if first_time.day == now.day and now.hour == 12:
#                     response = first_send(result)
#                     if response:
#                         if response.get('errcode') != 0:
#                             first_send(result)
#
#                 # 2天后/9点发通知
#                 # elif second_time.day == now.day and second_time.minute == now.minute:
#                 elif second_time.day == now.day and now.hour == 9:
#                     response = second_send(result)
#                     if response:
#                         if response.get('errcode') != 0:
#                             first_send(result)
#
#                 # 3天后/12点发通知
#                 # elif third_time.day == now.day and third_time.minute == now.minute:
#                 elif third_time.day == now.day and now.hour == 12:
#                     response = third_send(result)
#                     if response:
#                         if response.get('errcode') != 0:
#                             first_send(result)
#
#         return jsonify(errno=0, errmsg="OK")
#     except Exception as e:
#         print e
#         db.session.rollback()
#         return jsonify(errno=-1, errmsg="网络异常")


# 11,2019-1-29步数兑换等更新通知/1天后12点和20点
@api_user.route('/update_inform')
def update_inform():
    try:
        today = get_today()  # 当天零点
        yesterday = today + datetime.timedelta(days=-1)  # 昨天零点

        # 筛选昨天点过的用户
        results = UserBTN.query.filter(UserBTN.btn_num == 6, UserBTN.create_time >= yesterday,
                                       UserBTN.create_time < today).all()
        # results = UserBTN.query.filter(UserBTN.btn_num == 6).all()
        # 用户有点击相应btn, 指定时间发通知
        if results:
            # now = datetime.datetime.now()
            for result in results:
                # 推送模板消息
                # 1天后/12点发小程序文章更新提醒
                # Logging.logger.info('用户点击时间:{0}'.format(str(result.create_time)))
                # first_time = result.create_time + datetime.timedelta(days=+1)
                # if first_time.day == now.day and now.hour == 12:
                # if first_time.day == now.day:
                # if now.hour == 18:
                # nohup 定时掉了接口
                response = new_article_update_inform(result)
                if response:
                    if response.get('errcode') != 0:
                        new_article_update_inform(result)

                # 1天后/20点发步数兑换提醒
                # elif first_time.day == now.day and now.hour == 20:
                # elif first_time.day == now.day:
                # elif now.hour == 20:
                #     response = wechat_steps_inform(result)
                #     if response:
                #         if response.get('errcode') != 0:
                #             wechat_steps_inform(result)
                # else:
                #     pass

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg="网络异常")


# 像所有用户推送消息模版  147125
@api_user.route('/sign_in_user_push')
def sign_in_user_push():
    # users = User.query.all()
    # if users:
    #     for user in users:
    # 推送模板消息
    # nohup 定时掉了接口
    template_id = 'qbiB5-g1aGiHvO-4n0i1RBtUrYyLFH8I-L__zdmUSl8'
    data = {'keyword1': {'value': '今日奖励还未领取'},
            'keyword2': {'value': '你的今日红包已经发放，赶快进入小程序领取。最高88元现金，可随时提现！'}}
    # page = 'pages/changehome/mains'
    # page = 'pages/tipoff/tipoffcontent/main?arc_id=123620'
    page = 'pages/changehome/main'
    form_obj = UserFormID.query.filter(UserFormID.create_time > "2019-05-27 00:00:00",UserFormID.user_id>122877).group_by(
        UserFormID.user_id).all()
    for i in form_obj:
        if not i:
            Logging.logger.info('user_id=%s的用户FormID不足' % i.user_id)
        else:
            Logging.logger.info(f"准备向用户:推送今日奖励还未领取:{i.user_id}")
            print(i.user_id)
            form_id = i.form_id
            # form_id = 'dfc7fc369c6e41df9ceccef59417f760'
            # openid = 'o0YSl5HA36rf2PKNAd9rpe5dpvAM'
            openid = i.openid
            response = send_msg(template_id, openid, page, form_id, data)
            response = response.json()
            Logging.logger.info(f"准备向用户:推送结果:{response}")
            print(response)
            db.session.delete(i)
            db.session.commit()
    return jsonify(errno=0, errmsg="OK")
