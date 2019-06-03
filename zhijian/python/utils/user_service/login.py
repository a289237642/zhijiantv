# -*- coding:utf-8 -*-
# author: will
from functools import wraps

import itsdangerous
from flask import session, jsonify, g, request

from app import db
from app.models import Admin, User, BlackAccount
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config.keys_config import KeysConfig
from utils.log_service import Logging
from utils.redis_service.Redis_Client import RedisClient
# from utils.user_service.user_api_limit import get_user_ip


def login_required(view_func):
    """PC检验用户的登录状态"""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # user_id = session.get("user_id")
        token = session.get("token")
        if not token:
            return jsonify(errno=403, errmsg='用户未登录')
        try:
            serializer = Serializer(KeysConfig.get_secret_key(), 24 * 3600)
            result = serializer.loads(token)  # {"confirm": self.id}
            Logging.logger.info("当前登录的管理员ID={0}".format(result.get('confirm')))
        except itsdangerous.SignatureExpired:
            return jsonify(errno=401, errmsg='登陆已过期，请重新登陆')
        except itsdangerous.BadSignature:
            return jsonify(errno=402, errmsg='token值错误，请重新登陆')

        user_id = result.get('confirm')

        g.user_id = user_id

        try:
            user = Admin.query.get(user_id)
        except Exception as e:
            print (e)
            return jsonify(errno=402, errmsg='账号不存在，请联系管理员')

        if user.status == 0:
            return jsonify(errno=402, errmsg='账号已停用，请联系管理员')

        if user.is_login == 0:
            return jsonify(errno=402, errmsg='账号已退出，请重新登陆')

        if user.auth_status == 1:
            return jsonify(errno=402, errmsg='权限已变更，请重新登陆')

        if token != user.token:

            return jsonify(errno=402, errmsg='账号异地登陆，请重新登陆')

        # 如果用户登陆，进入到view_func中
        else:
            return view_func(*args, **kwargs)

    return wrapper


# 检查是否是管理员账号
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # user_id = session.get("user_id")
        user_id = g.user_id
        user = Admin.query.get(user_id)

        if user.is_admin == 0:
            return jsonify(errno=402, errmsg='当前账号没有权限查看,请联系管理员')
        else:
            return view_func(*args, **kwargs)

    return wrapper


# 检查小程序端用户是否是正常访问及接口访问频次限制
def auth_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("TOKEN")
        openid = request.headers.get("OPENID")
        ip = request.headers.get("Remoteip")

        Logging.logger.info('headers:{0}'.format(request.headers))
        if not all([token, openid]):
            return jsonify(errno=403, errmsg='用户未授权或非正常访问')

        user = User.query.filter(User.token == token, User.openid == openid).first()
        if not user:
            return jsonify(errno=403, errmsg='用户未授权或非正常访问')
        else:
            Logging.logger.info("当前用户昵称:{0}, IP:{1}".format(user.nick_name, ip))
            # 用户限制一分钟内总的接口访问量
            redis_cli = RedisClient.create_redis_cli()
            num = redis_cli.get(openid)
            if not num:
                redis_cli.setex(openid, 60, 1)
            else:
                Logging.logger.info("num:{0}".format(num))
                if int(num) >= 300:  # 5次/秒/人的接口访问量
                    # 重置过期时间, 30秒后可访问
                    Logging.logger.info("num:{0}".format(type(num)))
                    redis_cli.setex(openid, 30, num)
                    # 记录访问黑名单
                    # try:
                    #     obj = BlackAccount()
                    #     obj.ip = ip
                    #     obj.openid = openid
                    #     obj.num = num
                    #     db.session.add(obj)
                    #     db.session.commit()
                    # except Exception as e:
                    #     Logging.logger.error('record to black_account fail, errmsg:{0}'.format(e))
                    #     db.session.rollback()
                    return jsonify(errno=403, errmsg='操作过于频繁,请稍后再试')
                else:
                    redis_cli.incrby(openid, 1)
            return view_func(*args, **kwargs)

    return wrapper
