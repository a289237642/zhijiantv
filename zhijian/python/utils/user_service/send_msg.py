# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import json

import requests

from app import redis_store, db
from app.models import UserFormID, LessonOrder, LessonTypeShip, NewLesson, User, Article, ArticleGroup
from utils.log_service import Logging
from utils.user_service.auth import AccessToken


# 发送模板消息
def send_msg(template_id, openid, page, form_id, data):
    # access_token = redis_store.get('access_token')
    # if not access_token:
    obj = AccessToken()
    access_token = obj.get_access_token()
    redis_store.setex('access_token', 7200, access_token)

    params = {
        "touser": openid,
        "template_id": template_id,
        "page": page,
        "form_id": form_id,
        "data": data
    }
    params = json.dumps(params)
    result = requests.post(
        'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s' % access_token, params)
    return result


def first_send(result):
    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
        UserFormID.create_time.desc()).first()
    if not form_obj:
        Logging.logger.info('user_id=%s的用户FormID不足' % result.user_id)
    else:
        Logging.logger.info('准备向user_id=%s的用户推送(发生点击后第1天）12点整的通知:' % result.user_id)
        form_id = form_obj.form_id
        openid = form_obj.openid

        user_obj = User.query.get(result.user_id)
        now = datetime.datetime.now()
        template_id = 'LFMuIoAgGvegGPru0AAh_Go1sgSbk7D4A0BvD3-1C4o'
        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                'keyword2': {'value': '您订阅的热门文章已更新'},
                'keyword3': {'value': '现在已为您挑选了5篇您喜欢的文章，请点击阅读！'},
                'keyword4': {'value': now.strftime('%Y-%m-%d %H:%M:%S')}}
        # page = 'pages/tipoff/tipofflist/main'
        page = 'pages/changehome/main'

        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
        response = send_msg(template_id, openid, page, form_id, data)
        response = response.json()
        Logging.logger.info('返回结果:{0}'.format(response))
        if response.get('errcode') == 0:
            print(("推送成功:", response))
        else:
            print(("推送失败:", response))

        db.session.delete(form_obj)
        db.session.commit()
        return response


def second_send(result):
    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
        UserFormID.create_time.desc()).first()
    if not form_obj:
        print(('user_id=%s的用户FormID不足' % result.user_id))
    else:
        print(('准备向user_id=%s的用户推送(发生点击后第2天）9点整的通知:' % result.user_id))
        form_id = form_obj.form_id
        openid = form_obj.openid

        lesson = NewLesson.query.filter(NewLesson.cost_type == 3, NewLesson.is_open == 1).order_by(
            NewLesson.free_sort_num).first()
        user_obj = User.query.get(result.user_id)
        now = datetime.datetime.now()
        template_id = 'LFMuIoAgGvegGPru0AAh_Go1sgSbk7D4A0BvD3-1C4o'
        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                'keyword2': {'value': '已赠送您一门专属课程'},
                'keyword3': {'value': '《' + lesson.title + '》' + '点击马上听课。'},
                'keyword4': {'value': now.strftime('%Y-%m-%d %H:%M:%S')}}
        page = 'pages/curse/lessonList/main?lesson_id=%s' % lesson.id

        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
        response = send_msg(template_id, openid, page, form_id, data)
        response = response.json()
        print(('返回结果:', response))
        if response.get('errcode') == 0:
            print(("推送成功:", response))
        else:
            print(("推送失败:", response))

        db.session.delete(form_obj)
        db.session.commit()
        return response


def third_send(result):
    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
        UserFormID.create_time.desc()).first()
    if not form_obj:
        print(('user_id=%s的用户FormID不足' % result.user_id))
    else:
        print(('准备向user_id=%s的用户推送(发生点击后第3天）12点整的通知:' % result.user_id))
        form_id = form_obj.form_id
        openid = form_obj.openid

        # 当前用户已参与的课程的ID
        order_lessons_id_list = list()
        order_lessons = LessonOrder.query.filter(LessonOrder.user_id == result.user_id).all()
        if order_lessons:
            for order_lesson in order_lessons:
                order_lessons_id_list.append(order_lesson.lesson_id)

        # 当前类别下用户未参与的课程ID
        lessons_id_list = list()
        results = LessonTypeShip.query.filter(LessonTypeShip.type_id == 5).order_by(
            LessonTypeShip.sort_num).all()
        for res in results:
            if res.lesson_id not in order_lessons_id_list:
                lessons_id_list.append(res.lesson_id)
        lesson_id = lessons_id_list[0]
        lesson_obj = NewLesson.query.get(lesson_id)

        user_obj = User.query.get(result.user_id)
        now = datetime.datetime.now()
        template_id = 'LFMuIoAgGvegGPru0AAh_Go1sgSbk7D4A0BvD3-1C4o'
        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                'keyword2': {'value': '免费领课又上新了，快来领取'},
                'keyword3': {'value': lesson_obj.title},
                'keyword4': {'value': now.strftime('%Y-%m-%d %H:%M:%S')}}
        page = 'pages/curse/freeCourse/main'

        # response = threading.Timer(3600, send_msg, (template_id, openid, page, form_id, data))
        response = send_msg(template_id, openid, page, form_id, data)
        response = response.json()
        print(('返回结果:', response))
        if response.get('errcode') == 0:

            db.session.delete(form_obj)
            db.session.delete(result)
            db.session.commit()
            print(("推送成功:", response))
        else:
            db.session.delete(form_obj)
            db.session.commit()
            print(("推送失败:", response))
        return response


def new_article_update_inform(result):
    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
        UserFormID.create_time.desc()).first()
    if not form_obj:
        Logging.logger.info('user_id=%s的用户FormID不足' % result.user_id)
    else:
        # user_obj = User.query.get(result.user_id)
        # Logging.logger.info('准备向用户:%s推送(发生点击后第1天）12点整的文章更新提醒:' % user_obj.nick_name)
        Logging.logger.info('准备向用户:推送(发生点击后第1天）12点整的文章更新提醒:')
        form_id = form_obj.form_id
        openid = form_obj.openid

        obj = db.session.query(Article).join(ArticleGroup, ArticleGroup.article_id == Article.id).filter(
            ArticleGroup.group_id == 1).order_by(Article.zj_art_date.desc()).first()

        template_id = 'LFMuIoAgGvegGPru0AAh_P822rfsddrbBRJ9OTxfnkU'
        data = {
            'keyword1': {'value': '热文已更新，快去涨姿势吧！'},
            'keyword2': {'value': obj.title},  # 热文榜单第一篇文章
            'keyword3': {'value': '【智见live】发布文章啦，快去阅读得钢镚，换大奖吧！'}}
        page = 'pages/tipoff/tipoffcontent/main?arc_id=%s' % obj.id

        response = send_msg(template_id, openid, page, form_id, data)
        response = response.json()
        Logging.logger.info('发送结果:{0}'.format(response))

        db.session.delete(form_obj)
        db.session.commit()
        return response


def wechat_steps_inform(result):
    form_obj = UserFormID.query.filter(UserFormID.user_id == result.user_id).order_by(
        UserFormID.create_time.asc()).first()
    if not form_obj:
        Logging.logger.info('user_id=%s的用户FormID不足' % result.user_id)
    else:
        user_obj = User.query.get(result.user_id)
        Logging.logger.info('准备向用户:%s推送(发生点击后第1天）20点整的步数兑换更新提醒:' % user_obj.nick_name)
        form_id = form_obj.form_id
        openid = form_obj.openid

        change_coin = float('%.2f' % (user_obj.available_step * 0.001))
        now = datetime.datetime.now()
        template_id = 'IaVzZSp6QJhCi0-s-o9hPmCubthtQtrRXIR2Ic66yiY'
        data = {'keyword1': {'value': base64.b64decode(user_obj.nick_nameemoj)},
                'keyword2': {'value': now.strftime('%Y-%m-%d %H:%M:%S')},
                'keyword3': {'value': user_obj.available_step},  # 用户当日未兑换步数
                'keyword4': {'value': int(change_coin)},  # 当日未兑换步数兑换后应得积分
                'keyword5': {'value': int(user_obj.coins)},  # 用户账户总余额
                'keyword6': {'value': '天哪！获得了这么多钢镚，又可以换好多东西了。快去看看能换哪些好宝贝！'}}
        page = 'pages/changehome/main'

        response = send_msg(template_id, openid, page, form_id, data)
        response = response.json()
        Logging.logger.info('返回结果:{0}'.format(response))

        db.session.delete(form_obj)
        db.session.commit()
        return response


def new_sign_in_user_push(result):
    pass
