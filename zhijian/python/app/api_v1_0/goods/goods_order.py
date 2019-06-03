# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import hashlib
import random
import string
import time

import requests
from flask import request, jsonify

from app import db, redis_store
from config.wxpay_config import WxPayConfPub
from utils.log_service import Logging
from utils.redis_service.redis_limit import limit_handler
from utils.time_service import dif_time, unix_time
from utils.user_service.login import auth_required
from utils.user_service.wechat_pay import WechatPayTool, OrderQuery, RefundPub, AESCipher
from . import api_goods

from app.models import User, GoodsOrder, Goods, UserAddress, GoodsImage


# 小程序--创建商品订单
@api_goods.route('/create_goods_order', methods=['POST'])
# @auth_required
def create_goods_order():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')
        user_id = res.get('user_id')
        address_id = res.get('address_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([goods_id, user_id, address_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        goods_obj = Goods.query.get(goods_id)
        address_obj = UserAddress.query.get(address_id)
        if not user_obj or not goods_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if not address_obj:
            return jsonify(errno=-1, errmsg='请补充收货地址信息')

        if goods_obj.is_show == -1:
            return jsonify(errno=-1, errmsg='对不起,该商品已下架')

        user_coins = user_obj.coins
        if user_coins < goods_obj.price:
            return jsonify(errno=-1, errmsg='您的钢镚不足')

        num = GoodsOrder.query.filter(GoodsOrder.user_id == user_id, GoodsOrder.goods_id == goods_id,
                                      GoodsOrder.order_status == 1).count()
        if num > 0:
            return jsonify(errno=-3, errmsg='该商品已有未支付订单，请先支付')

        # 检查剩余库存
        # response = limit_handler(goods_obj.name, goods_obj.ku_num)
        # if response is False or int(goods_obj.available_num) <= 0:
        #     return jsonify(errno=-2, errmsg='对不起,该商品已领完')
        if int(goods_obj.available_num) <= 0:
            return jsonify(errno=-2, errmsg='对不起,该商品已领完')
        # 加入随机字符生成订单号
        chars = "abcdefghijklmnopqrstuvwxyz"
        strs = []
        for x in range(5):
            strs.append(chars[random.randrange(0, len(chars))])
        random_chars = "".join(strs)
        # random_chars = string.join(random.sample([x for x in chars], 5)).replace(" ", "")
        order_num = random_chars + str(int(time.time()))
        # print order_num

        obj = GoodsOrder()
        obj.user_id = user_id
        obj.goods_id = goods_id
        obj.order_num = order_num
        obj.address_id = address_id
        obj.price = goods_obj.price
        obj.postage = goods_obj.postage
        db.session.add(obj)

        goods_obj.available_num -= 1
        db.session.add(goods_obj)

        # 创建订单扣除用户钢镚,支付时,改变订单状态
        user_obj.coins -= goods_obj.price
        db.session.add(user_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK", order_id=obj.id)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常', num=6)


# 小程序--订单地址修改
@api_goods.route('/goods_order_address_update', methods=['POST'])
@auth_required
def goods_order_address_update():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        address_id = res.get('address_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([order_id, address_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        order_obj = GoodsOrder.query.get(order_id)
        address_obj = UserAddress.query.get(address_id)
        if not address_obj or not order_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if order_obj.order_status != 1:
            return jsonify(errno=-1, errmsg='当前订单状态不支持修改地址')

        order_obj.address_id = address_id
        db.session.add(order_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--订单页提示数量
@api_goods.route('/my_goods_order_num', methods=['POST'])
@auth_required
def my_goods_order_num():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        num1 = GoodsOrder.query.filter(GoodsOrder.user_id == user_id, GoodsOrder.order_status == 1).count()  # 待付款
        num2 = GoodsOrder.query.filter(GoodsOrder.user_id == user_id, GoodsOrder.order_status == 2).count()  # 待发货
        num3 = GoodsOrder.query.filter(GoodsOrder.user_id == user_id, GoodsOrder.order_status == 3).count()  # 待收货

        data = [
            {"order_status": 1, "num": num1},
            {"order_status": 2, "num": num2},
            {"order_status": 3, "num": num3},
        ]

        return jsonify(errno=0, errmsg="OK", data=data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--我的商品订单
@api_goods.route('/my_goods_order', methods=['POST'])
@auth_required
def my_goods_order():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        order_status = res.get('order_status', 6)  # 6全部
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if not all([user_id, order_status]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        if not user_obj or not isinstance(order_status, int):
            return jsonify(errno=-1, errmsg='参数错误')

        if order_status not in [1, 2, 3, 4, 5, 6]:
            return jsonify(errno=-1, errmsg='订单状态参数不合法')

        if order_status == 6:
            orders = GoodsOrder.query.filter(GoodsOrder.user_id == user_id).order_by(
                GoodsOrder.create_time.desc()).paginate(page, pagesize, False)
        else:
            orders = GoodsOrder.query.filter(GoodsOrder.user_id == user_id,
                                             GoodsOrder.order_status == order_status).order_by(
                GoodsOrder.create_time.desc()).paginate(page, pagesize, False)

        count = orders.total
        order_list = list()
        for order in orders.items:
            order_dict = dict()
            order_dict['order_id'] = order.id
            order_dict['order_num'] = order.order_num
            order_dict['price'] = order.price
            order_dict['postage'] = order.postage
            order_dict['order_status'] = order.order_status
            order_dict['create_time'] = str(order.create_time)

            goods_id = order.goods_id
            goods_obj = Goods.query.get(goods_id)
            order_dict['goods_name'] = goods_obj.name

            img_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_id, GoodsImage.is_min == 1).first()
            order_dict['min_pic'] = img_obj.img_url

            address_id = order.address_id
            address = UserAddress.query.get(address_id)
            # address_data = list()
            address_dict = dict()
            address_dict['name'] = address.name
            address_dict['phone'] = address.phone
            address_dict['provence'] = address.provence
            address_dict['city'] = address.city
            address_dict['area'] = address.area
            address_dict['detail'] = address.detail
            address_dict['post_num'] = address.post_num
            # address_data.append(address_dict)

            order_dict['address_data'] = address_dict
            order_list.append(order_dict)

        return jsonify(errno=0, errmsg="OK", data=order_list, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--订单详情
@api_goods.route('/goods_order_detail', methods=['POST'])
@auth_required
def goods_order_detail():
    try:
        res = request.get_json()
        order_id = res.get('order_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not isinstance(order_id, int):
            return jsonify(errno=-1, errmsg='参数格式不合法')

        order = GoodsOrder.query.get(order_id)
        if not order:
            return jsonify(errno=-1, errmsg='参数错误')

        order_dict = dict()
        order_dict['order_id'] = order.id
        order_dict['order_num'] = order.order_num
        order_dict['price'] = order.price
        order_dict['postage'] = order.postage
        order_dict['order_status'] = order.order_status
        order_dict['create_time'] = str(order.create_time)
        order_dict['timestamp'] = unix_time(order.create_time)
        goods_id = order.goods_id
        goods_obj = Goods.query.get(goods_id)
        order_dict['goods_name'] = goods_obj.name
        order_dict['goods_id'] = goods_id
        img_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_id, GoodsImage.is_min == 1).first()
        order_dict['min_pic'] = img_obj.img_url

        address_id = order.address_id
        address = UserAddress.query.get(address_id)
        address_dict = dict()
        address_dict['name'] = address.name
        address_dict['phone'] = address.phone
        address_dict['provence'] = address.provence
        address_dict['city'] = address.city
        address_dict['area'] = address.area
        address_dict['detail'] = address.detail
        address_dict['post_num'] = address.post_num
        address_dict['address_id'] = address_id

        order_dict['address_data'] = address_dict

        return jsonify(errno=0, errmsg="OK", data=order_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--商品支付
@api_goods.route('/goods_pay', methods=['POST'])
@auth_required
def goods_pay():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, order_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if order_obj.user_id != user_id:
            return jsonify(errno=-1, errmsg='订单与用户不符')

        if order_obj.order_status == 2 and order_obj.wx_code == "SUCCESS":
            return jsonify(errno=-1, errmsg='订单已支付成功')

        goods_id = order_obj.goods_id
        goods_obj = Goods.query.get(goods_id)
        goods_name = goods_obj.name

        postage = order_obj.postage

        if postage == 0:
            # 钢镚已在创建订单时扣除
            # user_obj.coins -= price
            order_obj.order_status = 2
            order_obj.pay_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(user_obj)
            db.session.add(order_obj)
            db.session.commit()
        elif postage > 0:
            # 钢镚+微信支付
            Logging.logger.info('---开始微信支付---')
            # 统一下单支付接口
            client_ip = request.remote_addr  # 获取客户端ip
            openid = User.query.get(user_id).openid

            pay = WechatPayTool()
            # 请求微信的url
            url = pay.UFDODER_URL

            # 拿到封装好的xml数据
            body_data = pay.get_body_data(openid, client_ip, postage, order_obj.order_num, goods_name)

            # 获取时间戳
            timeStamp = str(int(time.time()))

            # 请求微信接口下单
            result = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})

            # 回复数据为xml,将其转为字典
            content = pay.xmlToArray(result.content)
            # return jsonify(errno=0, errmsg="OK", data=content)

            if content["return_code"] == 'SUCCESS' and content["result_code"] == 'SUCCESS':
                # 获取预支付交易会话标识
                prepay_id = content.get("prepay_id")
                # 获取随机字符串
                nonceStr = content.get("nonce_str")

                # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
                paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr)

                # 封装返回给前端的数据
                data = {"prepay_id": prepay_id, "nonceStr": nonceStr, "paySign": paySign,
                        "timeStamp": timeStamp}
                db.session.add(order_obj)
                db.session.commit()
                return jsonify(errno=0, errmsg="OK", data=data)
            else:
                Logging.logger.error('errmsg:{0}'.format(content))
                return jsonify(errno=-1, errmsg='支付失败')
        else:
            pass

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 微信支付回调接口,微信会以post方式通知服务器，数据类型为xml
@api_goods.route('/goods_wechat_payback', methods=['POST'])
def goods_wechat_payback():
    try:
        pay = WechatPayTool()
        res = pay.xmlToArray(request.data)
        Logging.logger.info('微信回调参数:{0}'.format(res))

        out_trade_no = res.get('out_trade_no')  # 订单号
        transaction_id = res.get('transaction_id')  # 微信支付成功返回的微信订单号
        total_fee = res.get('total_fee')  # 订单金额(邮费)
        sign = res.get('sign')  # 签名
        pay_time = res.get('time_end')  # 支付完成时间
        return_code = res.get('return_code')
        result_code = res.get('result_code')
        return_msg = res.get('return_msg')

        """
        1、商户系统对于支付结果通知的内容一定要做签名验证,
        并校验返回的订单金额是否与商户侧的订单金额一致，防止数据泄漏导致出现“假通知”，造成资金损失。

        2、当收到通知进行处理时，首先检查对应业务数据的状态，
        判断该通知是否已经处理过，如果没有处理过再进行处理，如果处理过直接返回结果成功。
        在对业务数据进行状态检查和处理之前，要采用数据锁进行并发控制，以避免函数重入造成的数据混乱。
        """

        result = GoodsOrder.query.filter_by(order_num=out_trade_no).first()
        if return_code == 'SUCCESS' and result_code == 'SUCCESS':

            # 签名验证方法:
            # 去除微信返回的sign,对参数按照key=value的格式，并按照参数名ASCII字典序排序,再次加密生成sign,对比sign
            res.pop('sign')
            stringA = '&'.join(["{0}={1}".format(k, res.get(k)) for k in sorted(res)])
            stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
            new_sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
            new_sign = new_sign.upper()

            Logging.logger.info('new_sign={0}'.format(new_sign))
            if not result:
                doc = {'return_code': 'FAIL', 'return_msg': '订单不存在'}
                doc = pay.arrayToXml(doc)
                Logging.logger.error('回调支付失败, errmsg:订单不存在')
                result.wx_code = 'FAIL'
                db.session.add(result)
                db.session.commit()
                return doc

            elif result.order_status == 2:
                doc = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
                doc = pay.arrayToXml(doc)
                Logging.logger.info('已支付成功')
                result.wx_code = 'SUCCESS'
                db.session.add(result)
                db.session.commit()
                return doc

            elif result.postage == int(total_fee) and new_sign == sign:

                # 修改数据库订单相关信息
                result.order_status = 2
                result.pay_time = pay_time
                result.transaction_id = transaction_id
                result.wx_code = 'SUCCESS'

                doc = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
                doc = pay.arrayToXml(doc)  # 要以xml方式返回数据
                Logging.logger.info('微信支付成功')
                db.session.add(result)
                db.session.commit()
                return doc
            else:
                doc = {'return_code': 'FAIL', 'return_msg': '订单金额不符或签名错误'}
                doc = pay.arrayToXml(doc)
                Logging.logger.error('回调支付失败, errmsg:订单金额不符或签名错误')
                result.wx_code = 'FAIL'
                db.session.add(result)
                db.session.commit()
                return doc
        else:
            doc = {'return_code': 'FAIL', 'return_msg': return_msg}
            doc = pay.arrayToXml(doc)
            Logging.logger.error('回调支付失败, errmsg:{0}'.format(res))
            result.wx_code = 'FAIL'
            db.session.add(result)
            db.session.commit()
            return doc
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--查询用户订单状态
@api_goods.route('/goods_order_status_query', methods=['POST'])
@auth_required
def goods_order_status_query():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        order_id = res.get('order_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, order_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if order_obj.user_id != user_id:
            return jsonify(errno=-1, errmsg='订单与用户不符')

        order_status = order_obj.order_status
        wx_code = order_obj.wx_code

        return jsonify(errno=0, errmsg="OK", order_status=order_status, wx_code=wx_code)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 超过两小时未支付订单自动关闭
@api_goods.route('/clear_old_goods_order')
def clear_old_goods_order():
    try:
        results = GoodsOrder.query.filter(GoodsOrder.order_status == 1).all()
        if results:
            for result in results:
                mistiming = dif_time(str(result.create_time))
                Logging.logger.info('订单号:{0} 将在{1}秒后自动关闭'.format(result.order_num, 3600 * 2 - mistiming))
                if mistiming > 3600 * 2:
                    result.order_status = 5
                    result.close_time = datetime.datetime.now()

                    # 用户钢镚回退
                    user_id = result.user_id
                    user_obj = User.query.get(user_id)
                    user_obj.coins += result.price

                    # 商品库存回退
                    goods_id = result.goods_id
                    goods_obj = Goods.query.get(goods_id)
                    goods_obj.available_num += 1
                    redis_store.decr(goods_obj.name)

                    db.session.add(user_obj)
                    db.session.add(result)
                    db.session.add(goods_obj)
                    Logging.logger.info('订单号:{0} 超时未支付,自动关闭'.format(result.order_num))
            db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--取消订单
@api_goods.route('/goods_order_cancel', methods=['POST'])
@auth_required
def goods_order_cancel():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, order_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if order_obj.user_id != user_id:
            return jsonify(errno=-1, errmsg='订单与用户不符')

        if order_obj.order_status != -1:
            return jsonify(errno=-1, errmsg='当前订单状态不支持该操作')

        price = order_obj.price
        postage = order_obj.postage

        if postage == 0:
            # 邮费为0,申请过后直接退钢镚
            user_obj.coins += price
            order_obj.order_status = -2
            db.session.add(user_obj)
            db.session.add(order_obj)
            db.session.commit()
        elif postage > 0:
            user_obj.coins += price
            # 调微信退款接口
            refund = RefundPub()
            # 加入随机字符生成退款订单号
            chars = "abcdefghijklmnopqrstuvwxyz"
            random_chars = string.join(random.sample([x for x in chars], 5)).replace(" ", "")
            refund_order_num = random_chars + str(int(time.time()))
            xml_data = refund.get_xml_data(order_obj.transaction_id, refund_order_num, order_obj.postage,
                                           order_obj.postage)
            response = refund.apply_refund(xml_data)
            Logging.logger.info('微信返回的退款结果:{0}'.format(response.content))
            order_obj.refund_order_num = refund_order_num
            order_obj.refund_time = datetime.datetime.now()
            order_obj.order_status = -2
            db.session.add(user_obj)
            db.session.add(order_obj)
            db.session.commit()
        else:
            pass

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 微信退款回调接口,微信会以post方式通知服务器，数据类型为xml
@api_goods.route('/goods_wechat_refund_back', methods=['POST'])
def goods_wechat_refund_back():
    try:
        pay = WechatPayTool()
        res = pay.xmlToArray(request.data)
        Logging.logger.info('微信退款回调参数:{0}'.format(res))
        nonce_str = res.get('nonce_str')
        req_info_a = res.get('req_info')
        return_code = res.get('return_code')
        return_msg = res.get('return_msg')
        if return_code == 'SUCCESS':
            Logging.logger.info("----微信退款回调参数开始解密----")
            # 解密req_info
            """解密步骤如下：
            （1）对加密串A做base64解码，得到加密串B
            （2）对商户密钥key做md5，得到32位小写key*
            （3）用key*对加密串B做AES-256-ECB解密（PKCS7Padding）
            """
            try:
                # req_info_b = base64.b64decode(req_info_a)
                key = WxPayConfPub.KEY
                new_req_info = AESCipher(key).decrypt(req_info_a)
                Logging.logger.info('微信退款解密后的回调参数req_info:{0}'.format(new_req_info))

                if new_req_info.get('refund_status') == 'SUCCESS':
                    refund_id = new_req_info.get('refund_id')
                    refund_order_num = new_req_info.get('out_refund_no')
                    out_trade_no = new_req_info.get('out_trade_no')
                    success_time = new_req_info.get('success_time')
                    result = GoodsOrder.query.filter_by(order_num=out_trade_no).first()

                    # 库存回退
                    goods_id = result.goods_id
                    goods_obj = Goods.query.get(goods_id)
                    goods_obj.available_num += 1
                    redis_store.decr(goods_obj.name)

                    # 订单增加退款信息
                    result.refund_order_num = refund_order_num
                    result.refund_id = refund_id
                    result.refund_time = success_time
                    result.order_status = -2

                    # 用户金币回退
                    user_id = result.user_id
                    user_obj = User.query.get(user_id)
                    user_obj.coins += result.price

                    db.session.add(user_obj)
                    db.session.add(result)
                    db.session.add(goods_obj)
                    db.session.commit()

                    doc = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
                    doc = pay.arrayToXml(doc)
                    Logging.logger.info('微信退款回调成功')
                else:
                    doc = {'return_code': 'FAIL', 'return_msg': 'fail'}
                    doc = pay.arrayToXml(doc)
                    Logging.logger.error('微信退款回调失败')
                return doc
            except Exception as e:
                doc = {'return_code': 'FAIL', 'return_msg': 'fail'}
                doc = pay.arrayToXml(doc)
                Logging.logger.error('微信退款回调失败, errmsg:{0}'.format(e))
                return doc
        else:
            doc = {'return_code': 'FAIL', 'return_msg': return_msg}
            doc = pay.arrayToXml(doc)
            Logging.logger.error('回调退款失败, errmsg:{0}'.format(res))
            # result.wx_code = 'FAIL'
            # db.session.add(result)
            # db.session.commit()
            return doc

        # out_trade_no = res.get('out_trade_no')  # 订单号
        # transaction_id = res.get('transaction_id')  # 微信支付成功返回的微信订单号
        # total_fee = res.get('total_fee')  # 订单金额(邮费)
        # sign = res.get('sign')  # 签名
        # pay_time = res.get('time_end')  # 支付完成时间
        # return_code = res.get('return_code')
        # result_code = res.get('result_code')
        # return_msg = res.get('return_msg')
        #
        # result = GoodsOrder.query.filter_by(order_num=out_trade_no).first()
        # if return_code == 'SUCCESS' and result_code == 'SUCCESS':
        #
        #     # 签名验证方法:
        #     # 去除微信返回的sign,对参数按照key=value的格式，并按照参数名ASCII字典序排序,再次加密生成sign,对比sign
        #     res.pop('sign')
        #     stringA = '&'.join(["{0}={1}".format(k, res.get(k)) for k in sorted(res)])
        #     stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
        #     new_sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        #     new_sign = new_sign.upper()
        #
        #     Logging.logger.info('new_sign={0}'.format(new_sign))
        #     if not result:
        #         doc = {'return_code': 'FAIL', 'return_msg': '订单不存在'}
        #         doc = pay.arrayToXml(doc)
        #         Logging.logger.error('回调支付失败, errmsg:订单不存在')
        #         result.wx_code = 'FAIL'
        #         db.session.add(result)
        #         db.session.commit()
        #         return doc
        #
        #     elif result.order_status == 2:
        #         doc = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
        #         doc = pay.arrayToXml(doc)
        #         Logging.logger.info('已支付成功')
        #         result.wx_code = 'SUCCESS'
        #         db.session.add(result)
        #         db.session.commit()
        #         return doc
        #
        #     elif result.postage == int(total_fee) and new_sign == sign:
        #
        #         # 修改数据库订单相关信息
        #         result.order_status = 2
        #         result.pay_time = pay_time
        #         result.transaction_id = transaction_id
        #         result.wx_code = 'SUCCESS'
        #
        #         doc = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
        #         doc = pay.arrayToXml(doc)  # 要以xml方式返回数据
        #         Logging.logger.info('微信支付成功')
        #         db.session.add(result)
        #         db.session.commit()
        #         return doc
        #     else:
        #         doc = {'return_code': 'FAIL', 'return_msg': '订单金额不符或签名错误'}
        #         doc = pay.arrayToXml(doc)
        #         Logging.logger.error('回调支付失败, errmsg:订单金额不符或签名错误')
        #         result.wx_code = 'FAIL'
        #         db.session.add(result)
        #         db.session.commit()
        #         return doc
        # else:
        #     doc = {'return_code': 'FAIL', 'return_msg': return_msg}
        #     doc = pay.arrayToXml(doc)
        #     Logging.logger.error('回调支付失败, errmsg:{0}'.format(res))
        #     result.wx_code = 'FAIL'
        #     db.session.add(result)
        #     db.session.commit()
        #     return doc
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--确认收货
@api_goods.route('/affirm_goods', methods=['POST'])
@auth_required
def affirm_goods():
    try:
        res = request.get_json()
        order_id = res.get('order_id')
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, order_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            order_id = int(order_id)
            user_id = int(user_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        order_obj = GoodsOrder.query.get(order_id)
        if not order_obj:
            return jsonify(errno=-1, errmsg='订单不存在')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if order_obj.user_id != user_id:
            return jsonify(errno=-1, errmsg='订单与用户不符')

        if order_obj.order_status != 3:
            return jsonify(errno=-1, errmsg='当前订单状态不支持该操作')

        now = datetime.datetime.now()
        order_obj.order_status = 4
        order_obj.receive_time = now
        db.session.add(order_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
