# -*- coding:utf-8 -*-
# author: will


class ErrorCode(object):
    ok = (0, "ok")
    OK = (0, "ok")

    Internet_error = (10000, '网络异常')
    params_type_error = (10001, '参数类型错误')
    params_value_error = (10002, '参数错误')
    params_missing = (10003, '参数不完整')
    order_not_exist = (10004, '订单不存在')
    order_status_error = (10005, '当前订单未发货')
