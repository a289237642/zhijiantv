# Author:zcc
# -*- coding:utf-8 -*-
from flask import request

from app import db
# from app.models import LessonOrder
from app.models import LessonOrder

"""
Created on 2014-11-24
@author: http://blog.csdn.net/yueguanghaidao
 * 微信支付帮助库
 * ====================================================
 * 接口分三种类型：
 * 【请求型接口】--Wxpay_client_
 *      统一支付接口类--UnifiedOrder
 *      订单查询接口--OrderQuery
 *      退款申请接口--Refund
 *      退款查询接口--RefundQuery
 *      对账单接口--DownloadBill
 *      短链接转换接口--ShortUrl
 * 【响应型接口】--Wxpay_server_
 *      通用通知接口--Notify
 *      Native支付——请求商家获取商品信息接口--NativeCall
 * 【其他】
 *      静态链接二维码--NativeLink
 *      JSAPI支付--JsApi
 * ====================================g=================
 * 【CommonUtil】常用工具：
 *      trimString()，设置参数时需要用到的字符处理函数
 *      createNoncestr()，产生随机字符串，不长于32位
 *      formatBizQueryParaMap(),格式化参数，签名过程需要用到
 *      getSign(),生成签名
 *      arrayToXml(),array转xml
 *      xmlToArray(),xml转 array
 *      postXmlCurl(),以post方式提交xml到对应的接口url
 *      postXmlSSLCurl(),使用证书，以post方式提交xml到对应的接口url
"""

import json
import time
import random
import urllib.request, urllib.error, urllib.parse
import hashlib
import threading
from urllib.parse import quote
import xml.etree.ElementTree as ET

try:
    import pycurl
    from io import StringIO
except ImportError:
    pycurl = None


class WxPayConf_pub(object):
    """配置账号信息"""
    # =======【基本信息设置】=====================================
    # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID = "wx8068c95c08b3b464"
    # JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
    APPSECRET = "e25cd4b6ab4e8f59bee6af15a2fd4ced"
    # 受理商ID，身份标识
    MCHID = "1500273982"
    # 商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY = "8c319f28d81d1527a9428e9a5c2195f5"

    # =======【异步通知url设置】===================================
    # 异步通知url，商户根据实际开发过程设定
    NOTIFY_URL = "https://zj-live.max-digital.cn/api/v1_0/payback"

    # =======【JSAPI路径设置】===================================
    # 获取access_token过程中的跳转url，通过跳转将code传入jsapi支付页面
    JS_API_CALL_URL = "http://******.com/pay/?showwxpaytitle=1"
    # =======【证书路径设置】=====================================
    # 证书路径,注意应该填写绝对路径
    SSLCERT_PATH = "/www/cert/apiclient_cert.pem"
    SSLKEY_PATH = "/www/cert/apiclient_key.pem"
    # =======【curl超时设置】===================================
    CURL_TIMEOUT = 20
    # =======【HTTP客户端设置】===================================
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL")


class Singleton(object):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance


# 使用urlib2发送请求
class UrllibClient(object):
    """使用urlib2发送请求"""

    def get(self, url, second=30):
        return self.postXml(None, url, second)

    def postXml(self, xml, url, second=30):
        """不使用证书"""
        data = urllib.request.urlopen(url, xml, timeout=second).read()
        return data

    def postXmlSSL(self, xml, url, second=30):
        """使用证书"""
        raise TypeError("please use CurlClient")


# 使用Curl发送请求
class CurlClient(object):
    """使用Curl发送请求"""

    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYHOST, False)
        self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
        # 设置不输出header
        self.curl.setopt(pycurl.HEADER, False)

    def get(self, url, second=30):
        return self.postXmlSSL(None, url, second=second, cert=False, post=False)

    def postXml(self, xml, url, second=30):
        """不使用证书"""
        return self.postXmlSSL(xml, url, second=second, cert=False, post=True)

    def postXmlSSL(self, xml, url, second=30, cert=True, post=True):
        """使用证书"""
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.TIMEOUT, second)
        # 设置证书
        # 使用证书：cert 与 key 分别属于两个.pem文件
        # 默认格式为PEM，可以注释
        if cert:
            self.curl.setopt(pycurl.SSLKEYTYPE, "PEM")
            self.curl.setopt(pycurl.SSLKEY, WxPayConf_pub.SSLKEY_PATH)
            self.curl.setopt(pycurl.SSLCERTTYPE, "PEM")
            self.curl.setopt(pycurl.SSLCERT, WxPayConf_pub.SSLKEY_PATH)
        # post提交方式
        if post:
            self.curl.setopt(pycurl.POST, True)
            self.curl.setopt(pycurl.POSTFIELDS, xml)
        buff = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buff.write)

        self.curl.perform()
        return buff.getvalue()


class HttpClient(Singleton):
    @classmethod
    def configure(cls):
        if pycurl is not None and WxPayConf_pub.HTTP_CLIENT != "URLLIB":
            return CurlClient
        else:
            return UrllibClient


# 所有接口的基类
class Common_util_pub(object):
    """所有接口的基类"""

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self, length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        # 签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String, WxPayConf_pub.KEY)
        # 签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.items():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def postXmlCurl(self, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return HttpClient().postXml(xml, url, second=second)

    def postXmlSSLCurl(self, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return HttpClient().postXmlSSL(xml, url, second=second)


# H5网页端调起支付接口
class JsApi_pub(Common_util_pub):
    """JSAPI支付——H5网页端调起支付接口"""
    code = None  # code码，用以获取openid
    openid = None  # 用户的openid
    parameters = None  # jsapi参数，格式为json
    prepay_id = None  # 使用统一支付接口得到的预支付id
    curl_timeout = None  # curl超时时间

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        self.curl_timeout = timeout

    def createOauthUrlForCode(self, redirectUrl):
        """生成可以获得code的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["redirect_uri"] = redirectUrl
        urlObj["response_type"] = "code"
        urlObj["scope"] = "snsapi_base"
        urlObj["state"] = "STATE#wechat_redirect"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://open.weixin.qq.com/connect/oauth2/authorize?" + bizString

    def createOauthUrlForOpenid(self):
        """生成可以获得openid的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["secret"] = WxPayConf_pub.APPSECRET
        urlObj["code"] = self.code
        urlObj["grant_type"] = "authorization_code"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://api.weixin.qq.com/sns/oauth2/access_token?" + bizString

    def getOpenid(self):
        """通过curl向微信提交code，以获取openid"""
        url = self.createOauthUrlForOpenid()
        data = HttpClient().get(url)
        self.openid = json.loads(data)["openid"]
        return self.openid

    def setPrepayId(self, prepayId):
        """设置prepay_id"""
        self.prepay_id = prepayId

    def setCode(self, code):
        """设置code"""
        self.code = code

    def getParameters(self):
        """设置jsapi的参数"""
        jsApiObj = {}
        jsApiObj["appId"] = WxPayConf_pub.APPID
        timeStamp = int(time.time())
        jsApiObj["timeStamp"] = "{0}".format(timeStamp)
        jsApiObj["nonceStr"] = self.createNoncestr()
        jsApiObj["package"] = "prepay_id={0}".format(self.prepay_id)
        jsApiObj["signType"] = "MD5"
        jsApiObj["paySign"] = self.getSign(jsApiObj)
        self.parameters = json.dumps(jsApiObj)

        return self.parameters


# 请求型接口的基类
class Wxpay_client_pub(Common_util_pub):
    """请求型接口的基类"""
    response = None  # 微信返回的响应
    url = None  # 接口链接
    curl_timeout = None  # curl超时时间

    def __init__(self):
        self.parameters = {}  # 请求参数，类型为关联数组
        self.result = {}  # 返回参数，类型为关联数组

    def setParameter(self, parameter, parameterValue):
        """设置请求参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """设置标配的请求参数，生成签名，生成接口参数xml"""
        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def postXml(self):
        """post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlCurl(xml, self.url, self.curl_timeout)
        return self.response

    def postXmlSSL(self):
        """使用证书post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlSSLCurl(xml, self.url, self.curl_timeout)
        return self.response

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        return self.result


# 统一支付接口类
class UnifiedOrder_pub(Wxpay_client_pub):
    """统一支付接口类"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(UnifiedOrder_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        # 检测必填参数
        if any(self.parameters[key] is None for key in
               ("out_trade_no", "body", "total_fee", "notify_url", "trade_type")):
            raise ValueError("missing parameter")
        if self.parameters["trade_type"] == "JSAPI" and self.parameters["openid"] is None:
            raise ValueError("JSAPI need openid parameters")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["spbill_create_ip"] = "127.0.0.1"  # 终端ip
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        prepay_id = self.result["prepay_id"]
        return prepay_id


# 订单查询接口
class OrderQuery_pub(Wxpay_client_pub):
    """订单查询接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(OrderQuery_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""

        # 检测必填参数
        if any(self.parameters[key] is None for key in ("out_trade_no", "transaction_id")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)


# 退款申请接口
class Refund_pub(Wxpay_client_pub):
    """退款申请接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(Refund_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in
               ("out_trade_no", "out_refund_no", "total_fee", "refund_fee", "op_user_id")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


# 退款申请接口
class RefundQuery_pub(Wxpay_client_pub):
    """退款查询接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/refundquery"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(RefundQuery_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in
               ("out_refund_no", "out_trade_no", "transaction_id", "refund_id")):
            raise ValueError("missing parameter")
        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


# 对账单接口
class DownloadBill_pub(Wxpay_client_pub):
    """对账单接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/downloadbill"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(DownloadBill_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("bill_date",)):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        return self.result


# 短链接转换接口
class ShortUrl_pub(Wxpay_client_pub):
    """短链接转换接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/tools/shorturl"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(ShortUrl_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("long_url",)):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        return self.arrayToXml(self.parameters)

    def getShortUrl(self):
        """获取prepay_id"""
        self.postXml()
        prepay_id = self.result["short_url"]
        return prepay_id


# 响应型接口基类
class Wxpay_server_pub(Common_util_pub):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self):
        self.data = {}  # 接收到的数据，类型为关联数组
        self.returnParameters = {}  # 返回参数，类型为关联数组

    def saveData(self, xml):
        """将微信的请求xml转换成关联数组，以方便数据处理"""
        self.data = self.xmlToArray(xml)

    def checkSign(self):
        """校验签名"""
        tmpData = dict(self.data)  # make a copy to save sign
        del tmpData['sign']
        sign = self.getSign(tmpData)  # 本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def getData(self):
        """获取微信的请求数据"""
        return self.data

    def setReturnParameter(self, parameter, parameterValue):
        """设置返回微信的xml数据"""
        self.returnParameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """生成接口参数xml"""
        return self.arrayToXml(self.returnParameters)

    def returnXml(self):
        """将xml数据返回微信"""
        returnXml = self.createXml()
        return returnXml


# 通用通知接口
class Notify_pub(Wxpay_server_pub):
    """通用通知接口"""


# 请求商家获取商品信息接口
class NativeCall_pub(Wxpay_server_pub):
    """请求商家获取商品信息接口"""

    def createXml(self):
        """生成接口参数xml"""
        if self.returnParameters["return_code"] == self.SUCCESS:
            self.returnParameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
            self.returnParameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
            self.returnParameters["nonce_str"] = self.createNoncestr()  # 随机字符串
            self.returnParameters["sign"] = self.getSign(self.returnParameters)  # 签名

        return self.arrayToXml(self.returnParameters)

    def getProductId(self):
        """获取product_id"""
        product_id = self.data["product_id"]
        return product_id


# 静态链接二维码
class NativeLink_pub(Common_util_pub):
    """静态链接二维码"""

    url = None  # 静态链接

    def __init__(self):
        self.parameters = {}  # 静态链接参数

    def setParameter(self, parameter, parameterValue):
        """设置参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createLink(self):
        if any(self.parameters[key] is None for key in ("product_id",)):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  # 商户号
        time_stamp = int(time.time())
        self.parameters["time_stamp"] = "{0}".format(time_stamp)  # 时间戳
        self.parameters["nonce_str"] = self.createNoncestr()  # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名
        bizString = self.formatBizQueryParaMap(self.parameters, False)
        self.url = "weixin://wxpay/bizpayurl?" + bizString

    def getUrl(self):
        """返回链接"""
        self.createLink()
        return self.url


def pay(orderid, openid, money):
    # res = json.loads(request.data)
    print(money)
    orderid = orderid
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    util = Common_util_pub()
    data = {
        'appid': WxPayConf_pub.APPID,
        'mch_id': WxPayConf_pub.MCHID,
        'nonce_str': util.createNoncestr(),
        'body': 'lesson',
        'out_trade_no': orderid,  # 商户订单号
        'total_fee': str(int(money) * 100),  # 标价金额
        # 'total_fee': '1',#标价金额
        'spbill_create_ip': '101.132.186.25',  # 终端ip
        'notify_url': WxPayConf_pub.NOTIFY_URL,  # 通知地址异步接受微信支付结果的地址
        'trade_type': 'JSAPI',  # 原生扫码支付
        'openid': openid
    }
    data['sign'] = util.getSign(data)
    data = util.arrayToXml(data)
    resp = util.postXmlCurl(xml=data, url=url)
    # resp = util.postXmlSSLCurl(xml=data,url=url)
    resp = util.xmlToArray(resp)
    print(resp)
    if resp['return_code'] == 'SUCCESS' and resp['result_code'] == 'SUCCESS':
        timestamp = str(int(time.time()))
        # payid
        result = LessonOrder.query.filter_by(order_id=orderid).first()
        if result:
            result.wechatpay_id = resp['prepay_id']
            db.session.commit()
        data = {
            "appId": resp['appid'],
            "nonceStr": resp['nonce_str'],
            "package": "prepay_id=" + resp['prepay_id'],
            "signType": "MD5",
            "timeStamp": timestamp,
        }
        data['paySign'] = util.getSign(data)
        data['orderid'] = orderid  # 付款后操作的订单
        result = {
            'status': '0',
            'data': data
        }
    else:
        result = {
            'status': '-1',
            'errmsg': resp['return_msg']
        }
    return result


def order(orderid):
    # res = json.loads(request.data)
    url = "https://api.mch.weixin.qq.com/pay/orderquery"
    util = Common_util_pub()
    order_dict = dict()
    order_dict['appid'] = WxPayConf_pub.APPID
    order_dict['mch_id'] = WxPayConf_pub.MCHID
    order_dict['transaction_id'] = orderid
    order_dict['nonce_str'] = util.createNoncestr()
    order_dict['sign_type'] = 'MD5'
    order_dict['sign'] = util.getSign(order_dict)

    print((555))
    print(order_dict)
    data = util.arrayToXml(order_dict)
    print(data)
    resp = util.postXmlCurl(xml=data, url=url)
    # resp = util.postXmlSSLCurl(xml=data,url=url)
    resp = util.xmlToArray(resp)
    print((111, resp))
    if resp['return_code'] == 'SUCCESS' and resp['result_code'] == 'SUCCESS':
        result = {
            'status': '0',
            'data': resp
        }
    else:
        result = {
            'status': '-1',
            'errmsg': resp['return_msg']
        }
    return result
