# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import time

from flask import jsonify, request

from app import db
from app.models import NewLesson, LessonOrder, User, LikeNum, Audio, \
    ScanQrNum, DailyScanQrNum
from utils.user_service.pay import Common_util_pub, pay, order
from utils.time_service import dif_time
from . import api_order


# 小程序--新增订单(点击免费领)
@api_order.route('/create_order', methods=['POST'])
def create_order():
    params = request.get_json()
    lesson_id = params.get('lesson_id')
    user_id = params.get('user_id')

    print('请求参数:', request.data)
    if not all([lesson_id, user_id]):
        return jsonify(errno=-1, errmsg='参数不完整')

    try:
        user_id = int(user_id)
        lesson_id = int(lesson_id)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='参数错误')

    user_obj = User.query.get(user_id)
    if not user_obj:
        return jsonify(errno=-1, errmsg='用户不存在')

    lesson_obj = NewLesson.query.get(lesson_id)
    if not lesson_obj:
        return jsonify(errno=-1, errmsg='lesson不存在')

    if int(lesson_obj.count) <= 0:
        return jsonify(errno=-1, errmsg='对不起,该课程已领完')

    order_obj = LessonOrder.query.filter(LessonOrder.user_id == user_id, LessonOrder.lesson_id == lesson_id).first()
    if order_obj:
        return jsonify(errno=-1, errmsg='订单已存在')
    try:
        if lesson_obj.cost_type == 1:
            pay_way = 1
        elif lesson_obj.cost_type == 2:
            pay_way = 2
        else:
            pay_way = 1

        order_num = str(int(time.time()))
        openid = user_obj.openid
        lesson_order_obj = LessonOrder()
        lesson_order_obj.user_id = user_id
        lesson_order_obj.order_num = order_num
        lesson_order_obj.lesson_id = lesson_id
        lesson_order_obj.pay_way = pay_way
        lesson_order_obj.price = lesson_obj.price

        like_obj = LikeNum.query.filter(LikeNum.lesson_id == lesson_id, LikeNum.friend_user_id == user_id).first()
        if like_obj:
            lesson_order_obj.help_num = lesson_obj.present_num
            lesson_order_obj.is_get_present_num = 1

        db.session.add(lesson_order_obj)
        db.session.commit()

        money = lesson_obj.price
        if pay_way == 2:
            data = pay(order_num, openid, money)
            if int(data['status']) == 0:
                return jsonify(errno=0, data=data['data'])
            else:
                return jsonify(errno=-1, errmsg=data['errmsg'])
        else:
            return jsonify(errno=0, errmsg='ok', order_id=lesson_order_obj.id)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--检查改变我的助力团订单状态,超过24h,助力失败
@api_order.route('/check_my_lessons', methods=['POST'])
def check_my_lessons():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        print('请求参数:', request.data)
        if not user_id:
            return jsonify(errno=-1, errmsg='请传入user_id')

        try:
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        results = LessonOrder.query.filter(LessonOrder.user_id == user_id).all()

        for result in results:
            help_num = result.help_num
            price = result.price
            need = int(price) - int(help_num)
            create_time = result.create_time
            create_time = time.mktime(create_time.timetuple())
            now = time.time()
            if int(now) - int(create_time) > 3600 * 24 and need > 0:
                result.order_status = 3
                db.session.add(result)
                db.session.commit()

        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--助力失败重新发起助力,数据清除
@api_order.route('/restart_lesson_help', methods=['POST'])
def restart_lesson_help():
    try:
        res = request.get_json()
        order_id = res.get('order_id')

        print('请求参数:', request.data)
        if not order_id:
            return jsonify(errno=-1, errmsg='请传入order_id')

        try:
            order_id = int(order_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = LessonOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        now = int(time.time())
        now = datetime.datetime.fromtimestamp(now)
        print(now)
        order_obj.create_time = now
        order_obj.order_status = 1
        order_obj.help_num = 0
        order_obj.is_help = 0
        order_obj.is_get_present_num = 0
        order_obj.is_send = 0
        results = LikeNum.query.filter(LikeNum.order_id == order_id).all()
        for result in results:
            db.session.delete(result)
        db.session.add(order_obj)
        db.session.commit()

        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--我的助力团列表(订单列表)
@api_order.route('/my_lessons', methods=['POST'])
def my_lessons():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        print('请求参数:', request.data)
        try:
            user_id = int(user_id)
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        print('当前用户的user_id:', user_id)
        results = LessonOrder.query.filter(LessonOrder.user_id == user_id).order_by(
            LessonOrder.create_time.desc()).all()
        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]

        lesson_list = list()
        for result in results:
            lesson_dict = dict()
            help_num = result.help_num
            price = result.price
            need = int(price) - int(help_num)

            lesson_dict['status'] = result.order_status
            lesson_dict['price'] = result.price
            lesson_dict['order_id'] = result.id
            if need >= 0:
                lesson_dict['need'] = need
            else:
                lesson_dict['need'] = 0

            lesson_id = result.lesson_id
            lesson_obj = NewLesson.query.get(lesson_id)
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['is_show'] = lesson_obj.is_show
            lesson_dict['lesson_id'] = lesson_id
            lesson_list.append(lesson_dict)

        return jsonify(errno=0, errmsg='ok', data=lesson_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--我的已购课程列表
@api_order.route('/my_payed_lessons', methods=['POST'])
def my_payed_lessons():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        print('请求参数:', request.data)
        try:
            user_id = int(user_id)
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        print('当前用户的user_id:', user_id)
        results = LessonOrder.query.filter(LessonOrder.user_id == user_id, LessonOrder.is_pay == 1).order_by(
            LessonOrder.pay_time.desc()).all()
        lesson_count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]

        lesson_list = list()
        for result in results:
            lesson_dict = dict()

            lesson_dict['status'] = result.order_status
            lesson_dict['price'] = result.price
            lesson_dict['order_id'] = result.id
            lesson_dict['pay_time'] = str(result.pay_time)

            lesson_id = result.lesson_id
            lesson_obj = NewLesson.query.get(lesson_id)
            lesson_dict['title'] = lesson_obj.title
            lesson_dict['subtitle'] = lesson_obj.subtitle
            lesson_dict['min_pic'] = lesson_obj.min_pic
            lesson_dict['is_show'] = lesson_obj.is_show
            lesson_dict['total_audio_num'] = lesson_obj.total_audio_num
            lesson_dict['lesson_id'] = lesson_id

            audios = Audio.query.filter(Audio.lesson_id == lesson_id).order_by(Audio.sort_num).all()
            audio_count = len(audios)
            audio_list = list()
            for audio in audios:
                audio_dict = dict()
                audio_dict['id'] = audio.id
                audio_dict['name'] = audio.name
                audio_dict['title'] = audio.title
                audio_dict['mp3_url'] = audio.mp3_url
                # audio_dict['sort_num'] = result.sort_num
                audio_list.append(audio_dict)
            lesson_dict['audio_count'] = audio_count
            lesson_dict['audio_list'] = audio_list
            lesson_list.append(lesson_dict)

        return jsonify(errno=0, errmsg='ok', data=lesson_list, count=lesson_count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--分享好友助力页信息
@api_order.route('/share_lesson_info', methods=['POST'])
def share_lesson():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')
        print('分享参数user_id:', user_id)
        print('分享参数order_id:', order_id)

        if not all([order_id, user_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        order_obj = LessonOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        order_dict = dict()
        is_help = order_obj.is_help
        is_pay = order_obj.is_pay
        # order_dict['is_help'] = is_help
        order_dict['is_pay'] = is_pay
        order_dict['status'] = order_obj.order_status
        help_num = order_obj.help_num
        order_user_id = order_obj.user_id
        lesson_id = order_obj.lesson_id
        create_time = order_obj.create_time
        end_time = create_time + datetime.timedelta(days=+1)
        # 课程信息
        lesson_obj = NewLesson.query.get(lesson_id)
        price = lesson_obj.price

        user_list = list()
        if order_user_id == user_id:
            # 本人
            print('本人')
            order_dict['is_owner'] = 1
            order_dict['help_num'] = int(price) - int(help_num)
            print(order_dict)
        else:
            # 好友
            print('好友')
            order_dict['is_owner'] = 0
            # 好友是否已经助力
            obj = LikeNum.query.filter(LikeNum.order_id == order_id, LikeNum.friend_user_id == user_id).first()
            if obj:
                # 已助力
                print('已助力')
                order_dict['is_zhuli'] = 1
                # 好友是否参与当前课程
                friend_order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                            LessonOrder.user_id == user_id).first()
                if friend_order_obj:
                    # 好友已参与
                    print('已参与')
                    order_dict['help_num'] = int(price) - int(friend_order_obj.help_num)
                else:
                    # 好友未参与
                    print('未参与')
                    order_dict['help_num'] = int(price) - int(lesson_obj.present_num)
            else:
                # 未助力
                print('未助力')
                order_dict['is_zhuli'] = 0
                order_dict['help_num'] = int(price) - int(help_num)
            print(order_dict)

        if order_obj.is_get_present_num == 1:
            # 加入默认头像
            pic = 'https://maxpr.oss-cn-shanghai.aliyuncs.com/miniprogram/zjlive/download/image/15398461763541.jpg'
            for i in range(lesson_obj.present_num):
                user_list.append(pic)

        if is_help == 1:
            # 参与助力的好友信息
            results = LikeNum.query.filter(LikeNum.order_id == order_id).all()
            for result in results:
                friend_user_id = result.friend_user_id
                user_obj = User.query.get(friend_user_id)
                user_list.append(user_obj.avatar_url)

        order_dict['user_list'] = user_list
        order_dict['end_time'] = str(end_time)
        order_dict['title'] = lesson_obj.title
        order_dict['min_pic'] = lesson_obj.min_pic
        order_dict['lesson_id'] = lesson_obj.id
        order_dict['present_num'] = lesson_obj.present_num
        order_dict['price'] = lesson_obj.price
        order_user_obj = User.query.get(order_user_id)
        order_dict['user_img'] = order_user_obj.avatar_url
        base_num = lesson_obj.base_num

        # 参与人数
        # join_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id).all()
        # join_num = len(join_lesson_orders)
        # order_dict['join_num'] = join_num + base_num

        # 已购买人数
        buy_lesson_orders = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id, LessonOrder.is_pay == 1).all()
        buy_num = len(buy_lesson_orders)
        order_dict['buy_num'] = buy_num + base_num

        print("分享页返回数据:", order_dict)
        return jsonify(errno=0, errmsg='OK', data=order_dict)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--记录课程二维码识别数量
@api_order.route('/record_share_qr', methods=['POST'])
def record_share_qr():
    try:
        res = request.get_json()
        order_id = res.get('order_id')  # 邀友鼓励btn分享识别进入
        lesson_id = res.get('lesson_id')  # 邀友听课btn分享识别进入
        user_id = res.get('qr_user_id')
        # qr_user_id = res.get('qr_user_id')  # 邀友听课btn分享识别进入,传生成二维码的用户ID

        print('请求参数:', request.data)
        try:
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        # 记录当天新用户识别数量(授权30s的误差内,为新用户)
        now = datetime.datetime.now()
        user_obj = User.query.get(user_id)
        mistiming = dif_time(str(user_obj.create_time))
        print("mistiming=", mistiming)
        if mistiming <= 30:
            if order_id:
                print('邀友鼓励btn分享识别进入')
                try:
                    order_id = int(order_id)
                except Exception as e:
                    print(e)
                    return jsonify(errno=-1, errmsg='参数错误')

                order_obj = LessonOrder.query.get(order_id)
                if not order_obj:
                    return jsonify(errno=-1, errmsg='订单不存在')

                # 总数累计
                qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == order_obj.lesson_id, ScanQrNum.btn == 2).first()
                if qr:
                    qr.num += 1
                else:
                    qr = ScanQrNum()
                    qr.lesson_id = order_obj.lesson_id
                    # qr.user_id = order_obj.user_id
                    qr.btn = 2
                    qr.num = 1
                db.session.add(qr)

                # 按天记录/当天累加
                results = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == order_obj.lesson_id,
                                                      # DailyScanQrNum.user_id == order_obj.user_id,
                                                      DailyScanQrNum.btn == 2,
                                                      DailyScanQrNum.record_time == now.date()).first()
                if results:
                    results.daily_num += 1
                    db.session.add(results)
                else:
                    daily_qr = DailyScanQrNum()
                    daily_qr.lesson_id = order_obj.lesson_id
                    # daily_qr.user_id = order_obj.user_id
                    daily_qr.btn = 2
                    daily_qr.daily_num = 1
                    db.session.add(daily_qr)

                db.session.commit()

            elif lesson_id:
                print('邀友听课btn分享识别进入')
                try:
                    lesson_id = int(lesson_id)
                    # qr_user_id = int(qr_user_id)
                except Exception as e:
                    print(e)
                    return jsonify(errno=-1, errmsg='参数错误')

                lesson_obj = NewLesson.query.get(lesson_id)
                if not lesson_obj:
                    return jsonify(errno=-1, errmsg='课程不存在')

                # qr_user_obj = User.query.get(qr_user_id)
                # if not qr_user_obj:
                #     return jsonify(errno=-1, errmsg='生成二维码的用户ID不存在')

                # 总数累计
                qr = ScanQrNum.query.filter(ScanQrNum.lesson_id == lesson_id, ScanQrNum.btn == 1).first()
                if qr:
                    qr.num += 1
                else:
                    qr = ScanQrNum()
                    qr.lesson_id = lesson_id
                    # qr.user_id = qr_user_id
                    qr.btn = 1
                    qr.num = 1
                db.session.add(qr)

                # 按天记录/当天累加
                results = DailyScanQrNum.query.filter(DailyScanQrNum.lesson_id == lesson_id,
                                                      # DailyScanQrNum.user_id == qr_user_id,
                                                      DailyScanQrNum.btn == 1,
                                                      DailyScanQrNum.record_time == now.date()).first()
                if results:
                    results.daily_num += 1
                    db.session.add(results)
                else:
                    daily_qr = DailyScanQrNum()
                    daily_qr.lesson_id = lesson_id
                    # daily_qr.user_id = qr_user_id
                    daily_qr.btn = 1
                    daily_qr.daily_num = 1
                    db.session.add(daily_qr)

                db.session.commit()

        return jsonify(errno=0, errmsg='OK')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--好友助力
@api_order.route('/lesson_help', methods=['POST'])
def lesson_help():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')

        print('请求参数:', request.data)
        if not all([order_id, user_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = LessonOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='好友用户不存在')

        if user_id == order_obj.user_id:
            return jsonify(errno=-1, errmsg='亲,分享给好友来助力哦')

        obj = LikeNum.query.filter(LikeNum.order_id == order_id, LikeNum.friend_user_id == user_id).first()
        if obj:
            return jsonify(errno=-1, errmsg='您已经鼓励过啦')

        if order_obj.order_status == 2 or order_obj.is_pay == 1:
            return jsonify(errno=-1, errmsg='助力值已满')

        order_obj.help_num += 1
        if order_obj.help_num == order_obj.price:
            order_obj.order_status = 2
        order_obj.is_help = 1
        order_obj.is_send = 0
        db.session.add(order_obj)

        lesson_id = order_obj.lesson_id
        lesson_obj = NewLesson.query.get(lesson_id)
        like_obj = LikeNum()
        like_obj.friend_user_id = user_obj.id
        like_obj.order_id = order_id
        like_obj.lesson_id = lesson_id
        like_obj.friend_num = lesson_obj.present_num
        db.session.add(like_obj)

        # 好友是否已经参与该课程
        friend_order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                    LessonOrder.user_id == user_id).first()
        if friend_order_obj:
            # 已参与
            if friend_order_obj.is_get_present_num == 0:
                friend_order_obj.is_get_present_num = 1
                friend_order_obj.help_num += lesson_obj.present_num
                if friend_order_obj.help_num == friend_order_obj.price:
                    friend_order_obj.order_status = 2

                db.session.add(friend_order_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg='OK', order_status=order_obj.order_status)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# pc参与人信息
@api_order.route('/lesson_persons', methods=['POST'])
def lesson_persons():
    try:
        res = request.get_json()
        lesson_id = res.get('lesson_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        print('请求参数:', request.data)
        if not lesson_id:
            return jsonify(errno=-1, errmsg='请传入当前的课程的lesson_id')

        try:
            lesson_id = int(lesson_id)
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='当前课程不存在')

        results = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id).all()
        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]

        user_list = list()
        for result in results:
            user_dict = dict()
            user_obj = User.query.get(result.user_id)
            user_dict['user_img'] = user_obj.avatar_url
            user_dict['nick_name'] = base64.b64decode(user_obj.nick_nameemoj)

            # 是否已支付/已领取课程
            order_obj = LessonOrder.query.filter(LessonOrder.lesson_id == lesson_id,
                                                 LessonOrder.user_id == result.user_id).first()
            user_dict['is_pay'] = order_obj.is_pay
            user_dict['help_num'] = order_obj.help_num
            user_dict['price'] = lesson_obj.price
            user_list.append(user_dict)

        return jsonify(errno=0, errmsg='ok', data=user_list, count=count)
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 兑换/支付
@api_order.route('/lesson_pay', methods=['POST'])
def lesson_pay():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')
        print("支付参数:user_id:", user_id)
        print("支付参数:order_id:", order_id)

        if not all([user_id, order_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = LessonOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if order_obj.user_id != user_id:
            return jsonify(errno=-1, errmsg='用户与订单不符')

        lesson_id = order_obj.lesson_id
        lesson_obj = NewLesson.query.get(lesson_id)
        # 检查库存
        count = lesson_obj.count
        print('库存:', count)

        # 在操作数据库前创建事务保存点
        # save_point = transaction.savepoint()

        if int(count) > 0:
            pay_way = order_obj.pay_way
            if pay_way == 1:
                # 点赞兑换
                # if order_obj.is_pay == 1 and order_obj.order_status == 4:
                if order_obj.is_pay == 1:
                    return jsonify(errno=-1, errmsg='该课程已领取成功')

                help_num = order_obj.help_num
                if int(help_num) >= int(lesson_obj.price):
                    audio_list = list()
                    results = Audio.query.filter(Audio.lesson_id == lesson_id).all()
                    if not results:
                        return jsonify(errno=-1, errmsg='该课程没有音频信息')

                    num = len(results)
                    for result in results:
                        audio_dict = dict()
                        audio_dict['name'] = result.name
                        audio_dict['title'] = result.title
                        audio_dict['mp3_url'] = result.mp3_url
                        audio_list.append(audio_dict)

                    order_obj.is_pay = 1
                    order_obj.is_send = 0
                    # order_obj.order_status = 4
                    order_obj.pay_time = datetime.datetime.now()
                    lesson_obj.count = int(count) - 1

                    db.session.add(lesson_obj)
                    db.session.add(order_obj)
                    db.session.commit()
                    return jsonify(errno=0, errmsg='ok', count=num, audio_list=audio_list)
                else:
                    return jsonify(errno=-1, errmsg='点赞数量不足')
            else:
                # money
                pass
        else:
            return jsonify(errno=-1, errmsg='对不起,课程已领完')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 暂时未用
@api_order.route('/get_order', methods=['POST'])
def get_order():
    params = request.get_json()
    order_id = params.get('order_id')
    user_id = params.get('user_id')
    if user_id:
        try:
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='user_id错误')
    else:
        return jsonify(errno=-1, errmsg='user_id参数缺失')
    user_obj = User.query.get(user_id)
    if not user_obj:
        return jsonify(errno=-1, errmsg='用户不存在')

    if order_id:
        try:
            order_id = int(order_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='order_id错误')
    else:
        return jsonify(errno=-1, errmsg='order_id参数缺失')
    try:
        order_obj = LessonOrder.query.get(order_id)
        print((111))
        if not order_obj:
            print((222))
            return jsonify(errno=-1, errmsg='订单不存在')
        print((333))
        order_result = LessonOrder.query.filter(LessonOrder.user_id == user_id, LessonOrder.id == order_id).first()
        if order_result:
            orderid = str(order_result.pay_order)
            data = order(orderid)
            print(data)
            if int(data['status']) == 0:
                order_dict = {}
                order_dict['']
                return jsonify(errno=0, data=data['data'])
            else:
                return jsonify(errno=0, data=data['errmsg'])
        else:
            return jsonify(errno=-1, errmsg='订单与用户不匹配')


    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 支付回调接口
@api_order.route('/payback', methods=['POST', 'GET'])
def payback():
    util = Common_util_pub()
    # 订单支付成功对该订单操作数据库
    data = util.xmlToArray(request.data)
    try:
        result = LessonOrder.query.filter_by(order_id=data['out_trade_no']).first()
        result.is_pay = 1
        result.pay_order = data['transaction_id']
        print((11111))
    except Exception as e:
        result = LessonOrder.query.filter_by(order_id=data.out_trade_no).first()
        result.is_pay = 1
        result.pay_order = data.transaction_id
        print((2222))
    db.session.commit()
    re = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    res = util.arrayToXml(re)
    return res
