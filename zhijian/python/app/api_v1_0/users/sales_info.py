# -*- coding:utf-8 -*-
# author: will
import datetime

from flask import request, jsonify

from app import db
from app.models import NewLesson, Sales, SalesNum, User, DailySalesQrNum, ChangeClickStatistics
from utils.time_service import dif_time, get_today
from utils.log_service import Logging
from . import api_user


# 小程序--记录推广人员推广的数量
@api_user.route('/record_sale_num', methods=['POST'])
def record_sale_num():
    try:
        res = request.get_json()
        sales_id = res.get('sales_id')
        lesson_id = res.get('lesson_id')
        user_id = res.get('user_id')

        print(('请求参数:', request.data))
        if not all([sales_id, lesson_id, user_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            sales_id = int(sales_id)
            lesson_id = int(lesson_id)
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')

        sales_obj = Sales.query.get(sales_id)
        if not sales_obj:
            return jsonify(errno=-1, errmsg='推广员ID错误')

        lesson_obj = NewLesson.query.get(lesson_id)
        if not lesson_obj:
            return jsonify(errno=-1, errmsg='课程不存在')

        # 记录新用户识别数量(授权30s的误差内,为新用户)
        now = datetime.datetime.now()
        user_obj = User.query.get(user_id)
        mistiming = dif_time(str(user_obj.create_time))
        print(("mistiming=", mistiming))
        if mistiming <= 30:

            # 按天记录/当天累加
            result = DailySalesQrNum.query.filter(DailySalesQrNum.lesson_id == lesson_id,
                                                  DailySalesQrNum.sales_id == sales_id,
                                                  DailySalesQrNum.record_time == now.date()).first()
            if result:
                result.daily_num += 1
                db.session.add(result)
            else:
                daily_qr = DailySalesQrNum()
                daily_qr.lesson_id = lesson_id
                daily_qr.sales_id = sales_id
                daily_qr.daily_num = 1
                db.session.add(daily_qr)

            # 记录总数
            sales = SalesNum.query.filter(SalesNum.lesson_id == lesson_id, SalesNum.sales_id == sales_id).first()
            if not sales:
                obj = SalesNum()
                obj.sales_id = sales_id
                obj.lesson_id = lesson_id
                db.session.add(obj)
            else:
                sales.num += 1
                db.session.add(sales)

            db.session.commit()
        return jsonify(errno=0, errmsg='OK')
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 换量点击次数统计
@api_user.route('/amount_click_num', methods=['POST'])
def amount_click_num():
    try:
        # 获取今天零点
        today = get_today()
        res = request.get_json()
        amount_id = res.get('amount_id')
        type = res.get('type')
        if not all([amount_id, type]):
            return jsonify(errno=-1, errmsg='参数不完整')
        try:
            # 判断点击成功还是失败 1点击 2 成功
            type = int(type)
            amount_id = int(amount_id)
        except Exception as e:
            print(e)
            return jsonify(errno=-1, errmsg='参数错误')
        sales = ChangeClickStatistics.query.filter(ChangeClickStatistics.create_time > today,
                                                   ChangeClickStatistics.amount_id == amount_id).first()
        if sales:
            sales.btn_nums += 1 if type == 1 else 0
            sales.btn_successful_nums += 1 if type == 2 else 0
            db.session.add(sales)
        else:
            obj = ChangeClickStatistics()
            obj.amount_id = amount_id
            obj.btn_nums = 1 if type == 1 else 0
            obj.btn_successful_nums = 1 if type == 2 else 0
            db.session.add(obj)
        db.session.commit()
        Logging.logger.info('换量新点击数据'.format(amount_id))
        return jsonify(errno=0, errmsg='追加成功')

    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='参数错误')
