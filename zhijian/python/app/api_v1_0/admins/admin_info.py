# -*- coding:utf-8 -*-
import hashlib
import logging

from flask import request, jsonify, logging, session, g

from app import db, redis_store
from app.models import Admin
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required
from . import api_admin


# 登录
@api_admin.route('/login', methods=['GET', 'POST'])
def login():
    try:
        res = request.get_json()
        username = res.get('username')
        password = res.get('password')
        Logging.logger.info('request_args:{0}'.format(res))

        if not all([username, password]):
            return jsonify(errno=-1, errmsg='请输入用户名和密码')

        try:
            access_counts = redis_store.get('access_' + username)
            Logging.logger.info('登录错误次数: %s' % access_counts)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='查询redis失败')

            # 错误次数不为空 and 错误次数超过了最大值
        if access_counts is not None and int(access_counts) >= 5:
            waiting_time = redis_store.ttl('access_' + username)
            return jsonify(errno=-1, errmsg='请求错误已超过最大次数,还有%s秒可重新登录' % waiting_time)

        user = Admin.query.filter_by(username=username).first()
        if user:
            if user.status == 0:
                return jsonify(errno=-1, errmsg='该账号已被停用，请联系管理员')

            res = hashlib.md5()
            res.update(password.encode('utf-8'))
            password = res.hexdigest()
            if password == user.password:
                token = user.generate_active_token()
                user.token = token
                user.is_login = 1
                # 权限状态更新
                if user.auth_status == 1:
                    user.auth_status = 0
                db.session.add(user)
                db.session.commit()
                try:
                    redis_store.delete('access_' + username)
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))

                session['user_id'] = user.id
                session['user_name'] = user.username
                session['token'] = token

                data = {
                    "user_id": user.id,
                    "username": username,
                    "token": token,
                    "is_admin": user.is_admin,
                    "status": user.status,
                    "auth_status": user.auth_status
                }
                Logging.logger.info('管理员:{0} 登陆成功'.format(username))
                return jsonify(errno=0, errmsg="登录成功", data=data)
            else:
                # 累加错误次数, 并设置时间
                try:
                    # incr:累加错误次数
                    redis_store.incr('access_' + username)
                    # expire: 第一个参数 key, 第二个参数 过期时间10分钟
                    redis_store.expire('access_' + username, 600)
                except Exception as e:
                    Logging.logger.error('errmsg:{0}'.format(e))
                    return jsonify(errno=-1, errmsg='用户名或密码错误')
        else:
            return jsonify(errno=-1, errmsg='用户名不存在')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 更改密码
@api_admin.route('/changwpwd', methods=['POST'])
@login_required
# @admin_required
def change_pwd():
    # res = json.loads(request.data)
    res = request.get_json()
    try:
        username = res['username']
        passwordo = res['passwordo']
        password1 = res['password1']
        password2 = res['password2']
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    results = Admin.query.filter_by(username=username).first()
    if results:
        token = hashlib.md5()
        token.update(passwordo.encode('utf-8'))
        olpwd = token.hexdigest()
        if results.password != olpwd:
            data = {
                'errno': '-2',
                'errmsg': '原始密码错误'
            }
        elif password1 != password2:
            data = {
                'errno': '-2',
                'errmsg': '密码不一致'
            }
        else:
            token = hashlib.md5()
            token.update(password1.encode('utf-8'))
            newpwd = token.hexdigest()
            if newpwd == results.password:
                data = {
                    'errno': '-2',
                    'errmsg': '新密码与原密码相同，请重新输入'
                }
            else:
                results.password = newpwd
                try:
                    db.session.commit()
                    data = {
                        'errno': '0',
                        'msg': 'success'
                    }
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    data = {
                        'errno': '-2',
                        'msg': 'Fail'
                    }
    else:
        data = {
            'errno': '-2',
            'errmsg': '账号不存在'
        }
    return jsonify(data)


# 添加用户
@api_admin.route('/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    try:
        res = request.get_json()
        username = res.get('username')

        user_obj = Admin.query.filter_by(username=username).first()
        if user_obj:
            return jsonify(errno=-1, errmsg='用户名已存在')

        new_user = Admin()
        new_user.username = username

        db.session.add(new_user)
        db.session.commit()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        logging.error(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 登出
@api_admin.route('/logout')
@login_required
@admin_required
def logout():
    try:
        user_id = g.user_id
        user_obj = Admin.query.get(user_id)

        user_obj.is_login = 0
        db.session.add(user_obj)
        db.session.commit()
        session.clear()
        return jsonify(errno=0, errmsg='ok')
    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')


# 改变账号状态
@api_admin.route('/change_status')
@login_required
@admin_required
def change_status():
    try:
        user_id = g.user_id
        user_obj = Admin.query.get(user_id)

        if user_obj.status == 0:
            user_obj.status = 1
        else:
            user_obj.status = 0
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg='ok')

    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')

# 测试
@api_admin.route('/test', methods=['POST', 'GET'])
def test():
    try:
        if request.method == 'POST':
            res = request.get_json()
            return jsonify(res)
        else:
            return jsonify(errno=1, errmsg='ok')

    except Exception as e:
        print(e)
        return jsonify(errno=-1, errmsg='网络异常')
