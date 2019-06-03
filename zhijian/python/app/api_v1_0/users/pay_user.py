# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 10:44 AM
# @Author  : Shande
# @Email   : @.com
# @File    : pay_user.py
# @Software: PyCharm

import datetime
import random

from flask import request, jsonify, g

from app import db
from app.models import User, UserAtmRecord
from utils.log_service import Logging
from utils.user_service import MerchantsPay
from utils.user_service.login import auth_required
from . import api_user


# 微信商家支付（用户提现）
@api_user.route('/sz_pay', methods=['POST'])
@auth_required
def sz_pay():
    try:
        # 用户一天只能提现一次
        res = request.get_json()
        openid = res.get('openid')
        if openid in black_users():
            return jsonify(errno=-1, errmsg='今日红包被领完了，明天早点来吧')
        user_id = res.get('user_id')
        amount_r = res.get('amount_r')
        # 规定用户提取范围为 300 -5000 钢镚
        if float(amount_r) > 5000 or float(amount_r) < 300:
            return jsonify(errno=-1, errmsg="超出提现范围")
        ip = request.remote_addr  # 获取客户端ip
        nonce_str = MerchantsPay.random_str()
        trade_no = MerchantsPay.get_out_trade_no()
        if not all([openid, trade_no, amount_r, nonce_str, ip, trade_no]):
            return jsonify(errno=-1, errmsg="参数不完整")
        try:
            # 钢镚转换比例1000:1
            amount = int(float(amount_r / 1000) * 100)
            user_id = int(user_id)
            ip = str(ip)
            nonce_str = str(nonce_str)
            openid = str(openid)
            trade_no = str(trade_no)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数类型错误')
        user_obj = User.query.get(user_id)
        # 用户钢镚限制
        if user_obj.coins < float(amount_r):
            return jsonify(errno=-1, errmsg="用户钢镚不足")
        if not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")
        # 商户支付start
        WxMerchantsPay = MerchantsPay.WxMerchantsPay_util
        pay = MerchantsPay.Pay(WxMerchantsPay.WXPAY_APPID, WxMerchantsPay.WXPAY_MCHID, WxMerchantsPay.WXPAY_APIKEY)
        response = pay.post(openid, trade_no, amount, ip, nonce_str)
        if response and response["return_code"] == "SUCCESS":
            if response["result_code"] == "SUCCESS":
                # 小程序逻辑代码 支付成功  修改用户钢镚  存储提现记录
                atm = UserAtmRecord()
                atm.user_id = user_id
                atm.openid = openid
                atm.coin = float(amount_r)
                atm.atm_num = amount
                atm.ip = ip
                atm.nonce_str = nonce_str
                atm.trade_no = trade_no
                user_obj.coins -= float(amount_r)
                db.session.add(atm)
                db.session.add(user_obj)
                db.session.commit()
                return jsonify(errno=0, errmsg='支付成功')
            else:
                err_code_des = response["err_code_des"] or '违法操作'
                return jsonify(errno=-1, errmsg='今日红包被领完了，明天早点来吧')
        else:
            return jsonify(errno=-1, errmsg='网络错误')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 用户提现黑名单
def black_users():
    return ['o0YSl5LeDy_FeBhqvd3lyZJ5Y0cU', 'o0YSl5PGnaCA67TNEMINzXpeK9Vw', 'o0YSl5JuoVbf0p8Wk586tQ5bvXho']


# 用户今天是否提现
@api_user.route('/today_atm', methods=['POST'])
@auth_required
def today_atm():
    res = request.get_json()
    openid = res.get('openid')
    if not all([openid]):
        return jsonify(errno=-1, errmsg="参数不完整")
    # 获取今天零点
    now = datetime.datetime.now()
    today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    # 查询当天资金池
    atm_nums = UserAtmRecord.query.filter(UserAtmRecord.create_time >= today).all()
    isatm = 0
    for i in atm_nums:
        isatm += int(i.atm_num)
    if (isatm / 100) > 1000:
        return jsonify(errno=-1, errmsg='今日红包被领完了，明天早点来吧')

    user_obj = User.query.filter(User.openid == openid).first()
    # 用户钢镚限制
    if not user_obj:
        return jsonify(errno=-1, errmsg="用户不存在")

    # 用户当天是否提现
    user_atm_ns = UserAtmRecord.query.filter(UserAtmRecord.openid == openid,
                                             UserAtmRecord.create_time >= today).first()
    if user_atm_ns:
        return jsonify(errno=-1, errmsg='今天已经提现过了，明天再来吧！')
    else:
        return jsonify(errno=0, errmsg='可以提现')
