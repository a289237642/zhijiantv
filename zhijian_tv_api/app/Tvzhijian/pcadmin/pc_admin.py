# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 1:14 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : pc_admin.py
# @Software: PyCharm

import hashlib, time
from flask import json, request, jsonify, session
from . import pcadmin
from app.models import User


# 用户登陆
@pcadmin.route('/user_login', methods=['POST'])
def UserLogin():
    try:
        res = request.get_json()
        user_name = res.get('user_name')
        pass_word = res.get('pass_word')
        if not all([user_name, pass_word]):
            return jsonify(errno=-1, errmsg='请输入用户名和密码')
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if int(user.status) != 1:
                return jsonify(errno=-1, errmsg='该账号已被停用，请联系管理员')
            # 生成一个md5对象
            m1 = hashlib.md5()
            m1.update(pass_word.encode("utf-8"))
            pass_word = m1.hexdigest()
            if pass_word != user.pass_word:
                return jsonify(errno=-1, errmsg='密码错误')
            session['user_id'] = user.id
            session['user_name'] = user.user_name
            data = {
                "user_id": user.id,
                "user_name": user_name
            }
            return jsonify(errno=0, errmsg="登录成功", data=data)
        else:
            return jsonify(errno=-1, errmsg='用户不存在')

    except Exception as e:
        return jsonify(errno=-1, errmsg='网络异常')
