# -*- coding:utf-8 -*-
# author: will


class WxPayConfPub(object):
    """配置账号信息"""
    # =======【基本信息设置】=====================================
    # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID = "wx8068c95c08b3b464"
    # JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
    APPSECRET = "e25cd4b6ab4e8f59bee6af15a2fd4ced"
    # 商户号ID，身份标识
    MCHID = "1500273982"
    # 商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY = "8c319f28d81d1527a9428e9a5c2195f5"

    # =======【异步通知url设置】===================================
    # 异步通知url，商户根据实际开发过程设定
    # 支付通知
    # NOTIFY_URL = "https://zj-live.max-digital.cn/api/v1_0/goods_wechat_payback"  # 测试
    NOTIFY_URL = "https://zj-live-dev.max-digital.cn/api/v1_0/goods_wechat_payback"  # 正式
    # 退款通知
    # REFUND_NOTIFY_URL = "https://zj-live.max-digital.cn/api/v1_0/goods_wechat_refund_back"  # 测试
    REFUND_NOTIFY_URL = "https://zj-live-dev.max-digital.cn/api/v1_0/goods_wechat_refund_back"  # 正式

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
