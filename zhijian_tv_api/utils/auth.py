# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 3:15 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : auth.py
# @Software: PyCharm
from functools import wraps
from flask import session, jsonify


def is_login(view_func):
    """检验用户的登录状态"""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_name = session.get("user_name")
        if not user_name:
            return jsonify(errno=403, errmsg='用户未登录')
        else:
            return view_func(*args, **kwargs)

    return wrapper
