# -*- coding:utf-8 -*-
# author: will
import base64
import hashlib
import random
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests
from Crypto.Cipher import AES

from config.wxpay_config import WxPayConfPub


class WechatPayTool(object):
    """ 微信支付工具 """

    def __init__(self):
        self.UFDODER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"  # 微信统一下单接口链接

    # 生成随机字符串:
    @staticmethod
    def get_random_str():
        data = "123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
        random_str = ''.join(random.sample(data, 30))
        return random_str

    # 生成签名的函数
    @staticmethod
    def generate_sign(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee):
        ret = {
            "appid": WxPayConfPub.APPID,
            "body": body,
            "mch_id": WxPayConfPub.MCHID,
            "nonce_str": nonce_str,
            "notify_url": WxPayConfPub.NOTIFY_URL,  # 填写支付成功的回调地址，微信确认支付成功会访问这个接口
            "openid": openid,
            "out_trade_no": out_trade_no,
            "spbill_create_ip": spbill_create_ip,
            "total_fee": total_fee,
            "trade_type": 'JSAPI'  # 小程序支付
        }

        # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
        stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
        stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    # 获取返回给小程序的paySign
    @staticmethod
    def get_paysign(prepay_id, timeStamp, random_str):
        pay_data = {
            'appId': WxPayConfPub.APPID,
            'nonceStr': random_str,
            'package': "prepay_id=" + prepay_id,
            'signType': 'MD5',
            'timeStamp': timeStamp
        }
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    # 获取全部参数信息，封装成xml,传递过来的openid和客户端ip，和价格需要我们自己获取传递进来
    def get_body_data(self, openid, client_ip, price, order_num, body):
        body = body  # 商品描述
        nonce_str = self.get_random_str()  # 随机字符串
        out_trade_no = order_num  # 商户订单号
        total_fee = str(price)  # 订单价格，单位是 分
        # 获取签名
        sign = self.generate_sign(body, nonce_str, openid, out_trade_no, client_ip, total_fee)

        bodyData = '<xml>'
        bodyData += '<appid>' + WxPayConfPub.APPID + '</appid>'  # 小程序ID
        bodyData += '<body>' + body + '</body>'  # 商品描述
        bodyData += '<mch_id>' + WxPayConfPub.MCHID + '</mch_id>'  # 商户号
        bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
        bodyData += '<notify_url>' + WxPayConfPub.NOTIFY_URL + '</notify_url>'  # 支付成功的回调地址
        bodyData += '<openid>' + openid + '</openid>'  # 用户标识
        bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
        bodyData += '<spbill_create_ip>' + client_ip + '</spbill_create_ip>'  # 客户端终端IP
        bodyData += '<total_fee>' + total_fee + '</total_fee>'  # 总金额 单位为分
        bodyData += '<trade_type>JSAPI</trade_type>'  # 交易类型 小程序取值如下：JSAPI
        bodyData += '<sign>' + sign + '</sign>'
        bodyData += '</xml>'

        return bodyData

    @staticmethod
    def arrayToXml(arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.items():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @staticmethod
    def xmlToArray(xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data


# 微信订单查询
class OrderQuery(WechatPayTool):

    def __init__(self, timeout=WxPayConfPub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 设置curl超时时间
        self.curl_timeout = timeout
        self.parameters = {}
        super(WechatPayTool, self).__init__()

    def get_xml_data(self, transaction_id):
        nonce_str = self.get_random_str()  # 随机字符串
        # 获取签名
        sign = self.create_sign(nonce_str, transaction_id)
        # sign = '2BFB737A05D8FA431FF6F206848AD19F'
        bodyData = '<xml>'
        bodyData += '<appid>' + WxPayConfPub.APPID + '</appid>'  # 小程序ID
        bodyData += '<mch_id>' + WxPayConfPub.MCHID + '</mch_id>'  # 商户号
        bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
        bodyData += '<transaction_id>' + transaction_id + '</transaction_id>'  # 支付成功的微信订单号
        bodyData += '<sign>' + sign + '</sign>'
        bodyData += '</xml>'
        return bodyData

    @staticmethod
    def create_sign(nonce_str, transaction_id):
        ret = {
            "appid": WxPayConfPub.APPID,
            "mch_id": WxPayConfPub.MCHID,
            "nonce_str": nonce_str,
            "transaction_id": transaction_id
        }

        # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
        stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
        stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()


# 退款申请
class RefundPub(WechatPayTool):

    def __init__(self, timeout=WxPayConfPub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        # 设置curl超时时间
        self.curl_timeout = timeout
        self.parameters = {}
        super(RefundPub, self).__init__()

    def get_xml_data(self, transaction_id, refund_order_num, refund_fee, total_fee):
        nonce_str = self.get_random_str()  # 随机字符串
        # 获取签名
        sign = self.create_sign(nonce_str, transaction_id, refund_order_num, refund_fee, total_fee)
        # sign = '2BFB737A05D8FA431FF6F206848AD19F'
        bodyData = '<xml>'
        bodyData += '<appid>' + WxPayConfPub.APPID + '</appid>'  # 小程序ID
        bodyData += '<mch_id>' + WxPayConfPub.MCHID + '</mch_id>'  # 商户号
        bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
        bodyData += '<notify_url>' + WxPayConfPub.REFUND_NOTIFY_URL + '</notify_url>'  # 退款成功的回调地址
        bodyData += '<out_refund_no>' + refund_order_num + '</out_refund_no>'  # 商户退款单号
        bodyData += '<refund_fee>' + str(refund_fee) + '</refund_fee>'  # 退款金额
        bodyData += '<total_fee>' + str(total_fee) + '</total_fee>'  # 订单金额
        bodyData += '<transaction_id>' + transaction_id + '</transaction_id>'  # 支付成功的微信订单号
        bodyData += '<sign>' + sign + '</sign>'
        bodyData += '</xml>'
        return bodyData

    @staticmethod
    def create_sign(nonce_str, transaction_id, refund_order_num, refund_fee, total_fee):
        ret = {
            "appid": WxPayConfPub.APPID,
            "mch_id": WxPayConfPub.MCHID,
            "nonce_str": nonce_str,
            "notify_url": WxPayConfPub.REFUND_NOTIFY_URL,
            "out_refund_no": refund_order_num,
            "refund_fee": refund_fee,
            "total_fee": total_fee,
            "transaction_id": transaction_id
        }

        # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
        stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
        stringSignTemp = '{0}&key={1}'.format(stringA, WxPayConfPub.KEY)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    def apply_refund(self, xml_data):
        """ 发送退款申请，使用证书通信(需要双向证书)"""
        cert_path = WxPayConfPub.SSLCERT_PATH
        key_path = WxPayConfPub.SSLKEY_PATH
        res = requests.post(self.url, cert=(cert_path, key_path), data=xml_data.encode('utf-8'),
                            headers={'Content-Type': 'application/xml'})

        return res


class AESCipher(object):
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = hashlib.md5(key.encode('utf8')).hexdigest()

        # Padding for the input string --not
        # related to encryption itself.
        self.BLOCK_SIZE = 32  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                             chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # 加密
    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

    # 解密，针对微信用此方法即可
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc)).decode('utf8')
