# -*- coding:utf-8 -*-
import base64
import datetime
import hashlib
import json
import time
from urllib import parse
# 用parse.urljoin代替urlparse.urljoin
import requests
from flask import request, jsonify
from sqlalchemy import func

from app import redis_store, db
from app.models import User, UserSteps, UserReadArticle, LookVideoRecord, RedOpneDay
from config.keys_config import KeysConfig
from libs.WXBizDataCrypt import WXBizDataCrypt
from utils.qr_service import get_qr_func
from utils.time_service import get_today
from utils.user_service.auth import Openid, AccessToken
from utils.log_service import Logging
from utils.user_service.login import login_required, admin_required, auth_required
from utils.oss_service.storage import storage_by_url, storage_by_file
from utils.to_dict import query_to_dict
from . import api_user


# 授权
@api_user.route('/getopenid', methods=['POST'])
def get_openid():
    try:
        res = request.get_json()
        token = res.get('token')
        code = res.get('code')
        Logging.logger.info('request_args:{0}'.format(res))
        if not code or len(str(code)) < 15:
            return jsonify(status='-2', errmsg='code错误')

        openinfo = Openid.get_openid(code)
        if 'errcode' in openinfo:
            return jsonify(status='-2', errmsg=openinfo['errmsg'])

        if not token:
            openid = openinfo['openid']
            token = hashlib.md5()
            sessionkey = openinfo['session_key']
            token.update((openid + KeysConfig.get_my_secret()).encode('utf-8'))
            md5openid = token.hexdigest()
            results = User.query.filter_by(token=md5openid).first()
            if results:
                return jsonify(status='0', token=md5openid, openid=openid, sessionkey=sessionkey)
            else:
                return jsonify(status='-1', token=md5openid, openid=openid, sessionkey=sessionkey)
        else:
            # 用token查询信息
            results = User.query.filter_by(token=token).first()
            if results:
                sessionkey = openinfo['session_key']
                return jsonify(status='0', token=token, openid=results.openid, sessionkey=sessionkey)
            else:
                openid = openinfo['openid']
                token = hashlib.md5()
                sessionkey = openinfo['session_key']
                token.update(openid + KeysConfig.get_my_secret())
                md5openid = token.hexdigest()
                return jsonify(status='-1', token=md5openid, openid=openid, sessionkey=sessionkey)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(status='-2', errmsg='网络异常')


# 保存用户信息
@api_user.route('/saveuser', methods=['POST'])
# @auth_required
def save_user():
    try:
        res = request.get_json()
        token = res.get('token')
        openid = res.get('openid')
        nickname = res.get('nickname')
        avatar_url = res.get('avatar_url')
        gender = res.get('gender')
        city = res.get('city')
        province = res.get('province')
        country = res.get('country')
        language = res.get('language')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([token, openid]):
            return jsonify(status="-2", errmsg='参数错误')

        results = User.query.filter_by(openid=openid).first()
        url = storage_by_url(avatar_url)
        if results:
            Logging.logger.info('用户:{0} 授权返回,信息更新'.format(nickname))
            results.nick_name = nickname
            results.nick_nameemoj = str(base64.b64encode(nickname.encode('utf-8')), 'utf-8')
            results.avatar_url = url
            results.gender = gender
            results.city = city
            results.province = province
            results.country = country
            results.language = language
            db.session.add(results)
            db.session.commit()
            return jsonify(status='0', is_new=0, msg='success')
        else:
            Logging.logger.info('新增用户:{0}'.format(nickname))
            user_obj = User()
            user_obj.openid = openid
            user_obj.nick_name = nickname
            # user_obj.nick_nameemoj = base64.b64encode(nickname.encode('utf-8'))
            user_obj.nick_nameemoj = str(base64.b64encode(nickname.encode('utf-8')), 'utf-8')
            user_obj.avatar_url = url
            user_obj.gender = gender
            user_obj.city = city
            user_obj.province = province
            user_obj.country = country
            user_obj.language = language
            user_obj.token = token
            db.session.add(user_obj)
            db.session.commit()
            # 新用户 is_new =1
            return jsonify(status='0', is_new=1, msg='success')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(status='-2', msg='Fail')


@api_user.route('/savephone', methods=['POST'])
# @auth_required
def save_phone():
    try:
        res = request.get_json()
        Logging.logger.info('request_args:{0}'.format(res))

        if not all([res['token'], res['openid'], res['encryptedData'], res['iv'], res['sessionKey']]):
            return jsonify(status="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    encryptedData = res['encryptedData']
    iv = res['iv']
    sessionKey = res['sessionKey']
    appId = 'wx8068c95c08b3b464'
    try:
        pc = WXBizDataCrypt(appId, sessionKey)
        data = pc.decrypt(encryptedData, iv)
        print((data['phoneNumber']))
        phone = data['phoneNumber']
    except Exception as e:
        data = {
            'status': '-2',
            'msg': '解密失败'
        }
        return jsonify(data)
    results = User.query.filter_by(openid=res['openid']).first()
    if results:
        results.phone = phone
        try:
            db.session.commit()
            data = {
                'status': '0',
                'msg': 'success',
                'phone': phone
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail',
            }
    else:
        data = {
            'status': '-2',
            'msg': '用户不存在'
        }
    return jsonify(data)


@api_user.route('/savegender', methods=['POST'])
# @auth_required
def save_gender():
    # res = json.loads(request.data)
    res = request.get_json()
    Logging.logger.info('request_args:{0}'.format(res))

    try:
        if not all([res['token'], res['openid'], res['gender']]):
            return jsonify(status="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    print((res['openid'], "openid"))
    results = User.query.filter_by(openid=res['openid']).first()
    if results:
        results.gender = res['gender']
        try:
            db.session.commit()
            data = {
                'status': '0',
                'msg': 'success',
                'gender': res['gender']
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail',
                'gender': res['gender']
            }
    else:
        data = {
            'status': '-2',
            'msg': '用户不存在',
            'gender': res['gender']
        }
    return jsonify(data)


@api_user.route('/saveimg', methods=['POST'])
@auth_required
def save_img():
    image_file = request.files.get('image')
    token = request.form.get(key='token', type=str, default=None)
    openid = request.form.get(key='openid', type=str, default=None)
    Logging.logger.info('request_args:{0}'.format(request.data))

    if not all([token, openid]):
        return jsonify(status=-2, errmsg='参数错误')

    url = storage_by_file(image_file)
    results = User.query.filter_by(openid=openid).first()
    if results:
        results.avatar_url = url
        try:
            db.session.commit()
            data = {
                'status': '0',
                'avatar_url': url,
                'msg': 'success'
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail'
            }
    else:
        data = {
            'status': '-2',
            'msg': '用户不存在'
        }
    return jsonify(data)


@api_user.route('/savenickname', methods=['POST'])
@auth_required
def save_nickname():
    # res = json.loads(request.data)
    res = request.get_json()
    Logging.logger.info('request_args:{0}'.format(res))

    try:
        if not all([res['token'], res['openid'], res['nick_name']]):
            return jsonify(status="-2", errmsg='参数错误')
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    results = User.query.filter_by(openid=res['openid']).first()
    if results:
        results.nick_name = res['nick_name']
        results.nick_nameemoj = base64.b64encode(res['nick_name'])
        try:
            db.session.commit()
            data = {
                'status': '0',
                'msg': 'success',
                'nick_name': res['nick_name']
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            data = {
                'status': '-2',
                'msg': 'Fail',
                'nick_name': res['nick_name']
            }
    else:
        data = {
            'status': '-2',
            'msg': '用户不存在',
            'nick_name': res['nick_name']
        }
    return jsonify(data)


@api_user.route('/getuser', methods=['POST'])
# @auth_required
def get_user():
    # res = json.loads(request.data)
    res = request.get_json()
    Logging.logger.info('request_args:{0}'.format(res))

    try:
        token = res['token']
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    print(token)
    results = User.query.filter_by(token=token).first()
    print(results)
    if results:
        data = {
            'status': '0',
            'userinfo': {
                'id': results.id,
                'nickname': str(base64.b64decode(results.nick_nameemoj), encoding='utf-8'),
                'openid': results.openid,
                'token': results.token,
                'avatarurl': results.avatar_url,
                'gender': results.gender,
                'city': results.city,
                'province': results.province,
                'country': results.country,
                'language': results.language,
                'phone': results.phone
            }
        }
    else:
        data = {
            'status': '-2',
            'userinfo': {}
        }
    return jsonify(data)


@api_user.route('/getuserlist', methods=['POST'])
@login_required
@admin_required
def get_userlist():
    try:
        res = request.get_json()
        Logging.logger.info('request_args:{0}'.format(res))
        page = int(res.get('page', 1))
        size = int(res.get('size', 10))
        total = User.query.count()
        result = User.query.order_by(User.create_time.desc()).paginate(page, size, False)
    except Exception as e:
        print(e)
        return jsonify(status="-2", errmsg='参数错误')
    if result:
        try:
            arr = []
            for item in result.items:
                data = {
                    'id': item.id,
                    # 'nick_name': base64.b64decode(item.nick_nameemoj),
                    'nick_name': str(base64.b64decode(item.nick_nameemoj), encoding='utf-8'),
                    'gender': item.gender,
                    'phone': item.phone,
                    'avatar_url': item.avatar_url,
                    'create_time': str(item.create_time)
                }
                arr.append(data)
        except Exception as e:
            print(e)
            return jsonify(errno="-2", errmsg='网络错误')
        data = {
            'errno': '0',
            'list': arr,
            'total': total
        }
    else:
        data = {
            'errno': '0',
            'list': {},
            'total': total
        }
    return jsonify(data)


# 小程序生成二维码
@api_user.route('/getqr', methods=['POST'])
# @auth_required
def get_qr():
    try:
        res = request.get_json()
        page = res.get('page')
        scene = res.get('scene', 'default')

        Logging.logger.info('request_args:{0}'.format(res))
        if not page:
            return jsonify(status="-2", errmsg='参数错误')

        oss_url = get_qr_func(page, scene)
        if not oss_url:
            return jsonify(status="-2", msg='Fail')
        else:
            return jsonify(status="0", url=oss_url)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(status="-2", errmsg='qr获取失败')


@api_user.route('/myuser', methods=['POST'])
def get_myuser():
    # res = json.loads(request.data)
    res = request.get_json()

    try:
        token = res['token']
    except Exception as e:
        return jsonify(status="-2", errmsg='参数错误')
    print(token)
    results = User.query.filter_by(token=token).first()
    print(results)
    if results:
        data = {
            'status': '0',
            'userinfo': {
                'id': results.id,
                'nickname': results.nick_name,
                'openid': results.openid,
                'token': results.token,
                'avatarurl': results.avatar_url,
                'fid': str(results.id).zfill(6)
            }
        }
    else:
        data = {
            'status': '-1',
            'userinfo': {}
        }
    return jsonify(data)


# 获取access_token
@api_user.route('/access_token')
# @auth_required
def get_access_token():
    access_token = redis_store.get('access_token')
    if access_token:
        return jsonify(errno=0, errmsg="OK", token=access_token)
    else:
        obj = AccessToken()
        access_token = obj.get_access_token()
        redis_store.setex('access_token', 7200, access_token)
        return jsonify(errno=0, errmsg="OK", token=access_token)


# 小程序每次进入检查是否是当天第一次
@api_user.route('/first_login', methods=['POST'])
# @auth_required
def first_login():
    try:
        res = request.get_json()
        openid = res.get('openid')

        Logging.logger.info('request_args:{0}'.format(res))

        user_obj = User.query.filter_by(openid=openid).first()
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        last_day = user_obj.login_time
        today = datetime.date.today()
        today_time = int(time.mktime(today.timetuple()))
        last_time = int(time.mktime(last_day.timetuple()))
        if user_obj.first_login == 1 or (last_time - today_time) <= 0:
            user_obj.login_time = datetime.datetime.now()
            user_obj.first_login = 0
            db.session.add(user_obj)
            db.session.commit()
            return jsonify(errno=0, errmsg="OK", is_login=1)  # 是第一次
        else:
            return jsonify(errno=0, errmsg="OK", is_login=0)  # 不是第一次

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC用户搜索
@api_user.route('/user_search', methods=['POST'])
@login_required
@admin_required
def user_search():
    try:
        res = request.get_json()
        words = res.get('words')
        start_time = res.get('start_time')
        end_time = res.get('end_time')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if start_time:
            # 有开始时间
            try:
                if ":" in start_time:
                    time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                else:
                    time.strptime(start_time, "%Y-%m-%d")
            except Exception as e:
                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

            # 有关键字
            if words:
                # 有结束时间
                if end_time:
                    try:
                        if ":" in end_time:
                            time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(end_time, "%Y-%m-%d")
                    except Exception as e:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                    all_results = User.query.filter(User.create_time >= start_time,
                                                    User.create_time <= end_time).filter(
                        User.nick_name.like("%" + words + "%")).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
                # 无结束时间
                else:
                    all_results = User.query.filter(User.is_show == 0, User.create_time >= start_time).filter(
                        User.nick_name.like("%" + words + "%")).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
            # 无关键字
            else:
                # 有结束时间
                if end_time:
                    try:
                        if ":" in end_time:
                            time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(end_time, "%Y-%m-%d")
                    except Exception as e:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                    all_results = User.query.filter(User.create_time >= start_time,
                                                    User.create_time <= end_time).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
                # 无结束时间
                else:
                    all_results = User.query.filter(User.create_time >= start_time).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
        # 无开始时间
        else:
            # 有关键字
            if words:
                # 有结束时间
                if end_time:
                    try:
                        if ":" in end_time:
                            time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(end_time, "%Y-%m-%d")
                    except Exception as e:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                    all_results = User.query.filter(User.create_time <= end_time).filter(
                        User.nick_name.like("%" + words + "%")).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
                # 无结束时间
                else:
                    all_results = User.query.filter(User.nick_name.like("%" + words + "%")).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
            # 无关键字
            else:
                # 有结束时间
                if end_time:
                    try:
                        if ":" in end_time:
                            time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        else:
                            time.strptime(end_time, "%Y-%m-%d")
                    except Exception as e:
                        return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')

                    all_results = User.query.filter(User.create_time <= end_time).order_by(
                        User.create_time.desc()).paginate(page, pagesize, False)
                # 无结束时间
                else:
                    all_results = User.query.order_by(User.create_time.desc()).paginate(page, pagesize, False)

        res_count = all_results.total
        user_list = list()
        for user in all_results.items:
            group_dict = dict()
            group_dict['user_id'] = user.id
            group_dict['nick_name'] = base64.b64decode(user.nick_nameemoj)
            group_dict['nick_name'] = str(base64.b64decode(user.nick_nameemoj), encoding='utf-8')
            group_dict['avatar_url'] = user.avatar_url
            group_dict['gender'] = user.gender
            group_dict['phone'] = user.phone
            group_dict['create_time'] = str(user.create_time)
            user_list.append(group_dict)

        return jsonify(errno=0, errmsg="OK", count=res_count, data=user_list)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='搜索失败')


# 解密微信运动步数
@api_user.route('/save_wechat_steps', methods=['POST'])
@auth_required
def save_wechat_steps():
    try:
        res = request.get_json()
        sessionKey = res.get('sessionKey')
        user_id = res.get('user_id')
        encryptedData = res.get('encryptedData')
        iv = res.get('iv')
        appId = 'wx8068c95c08b3b464'

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([sessionKey, user_id, encryptedData, iv]):
            return jsonify(errno="-1", errmsg='参数不完整')

        user = User.query.get(user_id)
        if not user:
            return jsonify(errno="-1", errmsg='用户不存在')

        pc = WXBizDataCrypt(appId, sessionKey)
        data = pc.decrypt(encryptedData, iv)
        Logging.logger.info('解密后的微信运动数据包:{0}'.format(data))
        stepInfoList = data.get('stepInfoList')
        ret = sorted(stepInfoList, key=lambda x: x['timestamp'], reverse=True)
        wechat_step = ret[0].get('step')

        Logging.logger.info('获取到的微信步数:{0}'.format(wechat_step))
        print(('获取到的微信步数:', wechat_step))
        user_info = dict()
        # 总的可用 = 获取到的微信步数 + 总的偷得步数 - 总的兑换步数
        # 计算用户当天已兑换的步数
        now = datetime.datetime.now()
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
        user_steps = UserSteps.query.filter(UserSteps.user_id == user_id, UserSteps.change_step_date >= today).all()
        change_step = 0
        if user_steps:
            for user_step in user_steps:
                change_step += user_step.change_step  # 兑换的步数中包含(偷取好友的步数和之前微信运动步数)

        available_step = wechat_step + user.steal_step - change_step
        user_info['available_step'] = available_step
        user.available_step = available_step
        user.wechat_step = wechat_step

        # user_info['is_sign'] = user.is_sign
        # user_info['sign_coin'] = user.sign_coin
        # user_info['coins'] = user.coins

        db.session.add(user)
        db.session.commit()
        Logging.logger.info('返回的数据data={0}'.format(user_info))
        return jsonify(errno=0, errmsg="OK", data=user_info)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno="-1", errmsg='获取微信运动失败,请刷新重新获取')


# 解密转发群信息
@api_user.route('/analysis_share_info', methods=['POST'])
@auth_required
def analysis_share_info():
    try:
        res = request.get_json()
        sessionKey = res.get('sessionKey')
        encryptedData = res.get('encryptedData')
        iv = res.get('iv')
        appId = 'wx8068c95c08b3b464'

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([sessionKey, encryptedData, iv]):
            return jsonify(errno="-1", errmsg='参数不完整')

        pc = WXBizDataCrypt(appId, sessionKey)
        data = pc.decrypt(encryptedData, iv)
        # print "data=", data
        return jsonify(errno=0, errmsg="OK", data=data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno="-1", errmsg='网络异常')


# 小程序--获取用户钢镚数
@api_user.route('/get_user_coins', methods=['POST'])
@auth_required
def get_user_coins():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user = User.query.get(user_id)
        if not user:
            return jsonify(errno="-1", errmsg='用户不存在')

        user_info = dict()
        user_info['is_sign'] = user.is_sign
        user_info['sign_coin'] = user.sign_coin
        user_info['coins'] = user.coins
        today = get_today()
        user_steps = UserSteps.query.filter(UserSteps.user_id == user_id, UserSteps.change_step_date >= today).all()
        change_step = 0
        if user_steps:
            for user_step in user_steps:
                change_step += user_step.change_step
        available_step = user.wechat_step + user.steal_step - change_step
        user_info['available_step'] = available_step
        # 判断用户观看小视频成功上限  暂定10次
        movie_nums = LookVideoRecord.query.filter(LookVideoRecord.user_id == user_id,
                                                  LookVideoRecord.create_time >= today).count()
        if movie_nums >= 10:
            user_info['is_movie'] = -1
        else:
            user_info['is_movie'] = 0
        # 判断当日首次登陆
        login_day = RedOpneDay.query.filter(RedOpneDay.user_id == user_id, RedOpneDay.create_time >= today).count()
        if login_day:
            user_info['login_day'] = -1
        else:
            user_info['login_day'] = 0
        return jsonify(errno=0, errmsg="OK", user_info=user_info)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno="-1", errmsg='网络异常')


# 文章-用户-金币,聚合查询,根据用户阅读文章获得奖励由大到小排序
@api_user.route('/article_user_query', methods=['POST'])
def article_user_query():
    """
    session.query(User.name, func.sum(User.id).label("user_id_sum")).filter(func.to_days(User.create_date)==func.to_days(func.now())).group_by(User.name).all()
    """
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('paalgesize', 10)
        results = db.session.query(UserReadArticle.user_id, UserReadArticle.article_id, UserReadArticle.create_time,
                                   func.round(func.sum(UserReadArticle.random_coins), 2).label(
                                       "user_coins_sum")).order_by(
            func.sum(UserReadArticle.random_coins).desc()).group_by(UserReadArticle.user_id).all()

        data = query_to_dict(results)
        # keys = ['user_id', 'total_coin']
        # for result in results:
        #     print result[0].user_id
        #     print result[1]
        # #     data = zip(keys, result)
        # #     print data

        return jsonify(errno=0, errmsg="OK", data=data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno="-1", errmsg='解密失败')


# 临时删除 user信息
@api_user.route('/del_user_test', methods=['GET'])
def del_user_test():
    """
    """
    try:
        open_id = 'o0YSl5D5Gzt6_BuXZUXYE98fp3ps'
        open_id_s = 'o0YSl5Mu47Ykjmgej8fKU_q8k9AE'
        open_id_p = 'o0YSl5E1OO40FhqTDyQ9W-gvr9us'
        bl_obj = User.query.filter(User.openid == open_id).first()
        bl_ob_s = User.query.filter(User.openid == open_id_s).first()
        open_id_p = User.query.filter(User.openid == open_id_p).first()
        if bl_obj:
            db.session.delete(bl_obj)
        if bl_ob_s:
            db.session.delete(bl_ob_s)
        if open_id_p:
            db.session.delete(open_id_p)
        db.session.commit()
        return jsonify(errno=0, errmsg='删除成功')
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno="-1", errmsg='error')
