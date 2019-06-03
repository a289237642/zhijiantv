# -*- coding:utf-8 -*-
# author: will
import datetime
import random, pymysql, time

from flask import request, jsonify, g

from app import db
from app.models import ChangeAmount, User, ChangeAmountUser, AfterPlayShare, LookVideoRecord, HeavenForUserOpen, \
    HeavenRedRecord, RedOpneDay
from utils.log_service import Logging
from utils.time_service import get_today, date_time
from utils.user_service.login import login_required, admin_required, auth_required
from . import api_user


# PC新增或修改换量小程序信息
@api_user.route('/update_mini_program', methods=['POST'])
@login_required
@admin_required
def update_mini_program():
    try:
        res = request.get_json()
        coin = res.get('coin')
        name = res.get('name')
        img_url = res.get('img_url')
        sort_num = res.get('sort_num', 1)
        app_id = res.get('app_id')
        mini_program_id = res.get('mini_program_id')
        words = res.get('words')
        path = res.get('path')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([name, coin, img_url, sort_num, app_id, words]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            sort_num = int(sort_num)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            sort_num = 1

        if not mini_program_id:
            # 新增
            obj = ChangeAmount()
            obj.coin = coin
            obj.name = name
            obj.img_url = img_url
            obj.sort_num = sort_num
            obj.app_id = app_id
            obj.admin_id = admin_id
            obj.words = words
            obj.path = path
            db.session.add(obj)
        else:
            # 修改
            try:
                mini_program_id = int(mini_program_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg='参数类型错误')

            mini_obj = ChangeAmount.query.get(mini_program_id)
            if not mini_obj:
                return jsonify(errno=-1, errmsg='换量小程序不存在')

            if sort_num != mini_obj.sort_num:
                if sort_num < mini_obj.sort_num:
                    # 往前移
                    results = ChangeAmount.query.filter(ChangeAmount.sort_num >= sort_num).all()
                    for result in results:
                        result.sort_num += 1
                else:
                    # 往后移
                    results = ChangeAmount.query.filter(ChangeAmount.sort_num <= sort_num).all()
                    for result in results:
                        result.sort_num -= 1

            mini_obj.coin = coin
            mini_obj.name = name
            mini_obj.img_url = img_url
            mini_obj.sort_num = sort_num
            # mini_obj.app_id = app_id
            mini_obj.admin_id = admin_id
            mini_obj.words = words
            mini_obj.path = path
            db.session.add(mini_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC换量小程序列表
@api_user.route('/mini_program_ls', methods=['POST'])
@login_required
@admin_required
def mini_program_ls():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        # admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        results = ChangeAmount.query.order_by(ChangeAmount.sort_num.asc()).all()
        count = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]
        data_list = list()
        for result in results:
            data_dict = dict()
            data_dict['mini_program_id'] = result.id
            data_dict['name'] = result.name
            data_dict['img_url'] = result.img_url
            data_dict['is_show'] = result.is_show
            data_dict['sort_num'] = result.sort_num
            data_dict['coin'] = result.coin
            data_dict['app_id'] = result.app_id
            data_dict['words'] = result.words
            data_dict['path'] = result.path
            data_list.append(data_dict)

        return jsonify(errno=0, errmsg="OK", data=data_list, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC改变换量小程序的状态
@api_user.route('/mini_program_change_status', methods=['POST'])
@login_required
@admin_required
def mini_program_change_status():
    try:
        res = request.get_json()
        mini_program_id = res.get('mini_program_id')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            mini_program_id = int(mini_program_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数类型错误')

        obj = ChangeAmount.query.get(mini_program_id)
        if not obj:
            return jsonify(errno=-1, errmsg='该换量小程序不存在')

        if obj.is_show == 0:
            obj.is_show = 1
            obj.admin_id = admin_id
        else:
            obj.is_show = 0
            obj.admin_id = admin_id

        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC换量小程序删除
@api_user.route('/del_mini_program', methods=['POST'])
@login_required
@admin_required
def del_news_groups():
    try:
        res = request.get_json()
        mini_program_id_list = res.get('mini_program_id_list')

        Logging.logger.info('request_args:{0}'.format(res))
        if not isinstance(mini_program_id_list, list):
            return jsonify(errno=-1, errmsg="参数类型错误")

        for mini_program_id in mini_program_id_list:
            obj = ChangeAmount.query.get(mini_program_id)
            if not obj:
                return jsonify(errno=-1, errmsg="该换量小程序不存在")

            db.session.delete(obj)
            db.session.commit()
            Logging.logger.info("换量小程序:{0},删除成功".format(obj.name))
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--换量小程序
@api_user.route('/mini_program', methods=['POST'])
@auth_required
def mini_program():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user = User.query.get(user_id)
        if not user:
            return jsonify(errno=-1, errmsg='用户不存在')

        # 获取今天零点
        today = get_today()
        results = ChangeAmountUser.query.filter(ChangeAmountUser.user_id == user_id,
                                                ChangeAmountUser.create_time >= today).all()
        data_dict = dict()
        if results:
            # 用户今日已获得奖励的换量小程序ID
            mini_program_id_ls = [x.mini_program_id for x in results]
            result = ChangeAmount.query.filter(ChangeAmount.id.notin_(mini_program_id_ls),
                                               ChangeAmount.is_show == 1).order_by(ChangeAmount.sort_num.asc()).first()
        else:
            result = ChangeAmount.query.filter(ChangeAmount.is_show == 1).order_by(ChangeAmount.sort_num.asc()).first()

        if result:
            data_dict['mini_program_id'] = result.id
            data_dict['name'] = result.name
            data_dict['img_url'] = result.img_url
            data_dict['sort_num'] = result.sort_num
            data_dict['coin'] = result.coin
            data_dict['app_id'] = result.app_id
            data_dict['words'] = result.words
            data_dict['path'] = result.path
        else:
            data_dict['coin'] = -1

        return jsonify(errno=0, errmsg="OK", data=data_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--用户点击试玩换量小程序,20s内有返回,给对应奖励
@api_user.route('/play_mini_program', methods=['POST'])
@auth_required
def play_mini_program():
    try:
        res = request.get_json()
        mini_program_id = res.get('mini_program_id')
        user_id = res.get('user_id')
        start_time = res.get('start_time')
        end_time = res.get('end_time')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([mini_program_id, user_id]):
            return jsonify(errno=-1, errmsg="参数不完整")

        try:
            mini_program_id = int(mini_program_id)
            user_id = int(user_id)
            start_time = int(start_time)
            end_time = int(end_time)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数类型错误')

        mini_obj = ChangeAmount.query.get(mini_program_id)
        user_obj = User.query.get(user_id)
        if not mini_obj or not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")

        dif_time = end_time - start_time
        if dif_time < 20:
            return jsonify(errno=-1, errmsg="试玩时间不足奖励标准")

        # 获取今天零点
        today = get_today()
        obj = ChangeAmountUser.query.filter(ChangeAmountUser.user_id == user_id,
                                            ChangeAmountUser.mini_program_id == mini_program_id,
                                            ChangeAmountUser.create_time >= today).first()
        if obj:
            return jsonify(errno=-1, errmsg="今天已经试玩过了")
        else:
            play = ChangeAmountUser()
            play.mini_program_id = mini_program_id
            play.user_id = user_id
            play.coin = mini_obj.coin
            play.start_time = date_time(start_time)
            play.end_time = date_time(end_time)

            user_obj.coins += mini_obj.coin
            db.session.add(user_obj)
            db.session.add(play)
            db.session.commit()
        return jsonify(errno=0, errmsg="OK", coin=mini_obj.coin)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 小程序--用户点击试玩换量小程序后转发获得随机奖励(规则同文章转发)
@api_user.route('/play_for_coins', methods=['POST'])
@auth_required
def play_for_coins():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        mini_program_id = res.get('mini_program_id')
        openGId = res.get('openGId')  # 用户分享的微信群的唯一标识

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, mini_program_id, openGId]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            user_id = int(user_id)
            mini_program_id = int(mini_program_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数类型错误')

        mini_obj = ChangeAmount.query.get(mini_program_id)
        user_obj = User.query.get(user_id)
        if not mini_obj or not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")

        # 获取今天零点
        today = get_today()
        obj = AfterPlayShare.query.filter(AfterPlayShare.user_id == user_id,
                                          AfterPlayShare.mini_program_id == mini_program_id,
                                          AfterPlayShare.openGId == openGId,
                                          AfterPlayShare.create_time >= today).first()
        if obj:
            return jsonify(errno=-1, errmsg="请换个群来换取奖励")

        random_coins = float('%.2f' % random.uniform(1, 3))
        # random_coins = float('%.2f' % random.uniform(2, 6))
        user_obj.coins += random_coins

        play = AfterPlayShare()
        play.openGId = openGId
        play.mini_program_id = mini_program_id
        play.user_id = user_id
        play.random_coins = random_coins

        db.session.add(play)
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=random_coins, total_coins=user_obj.coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='兑换失败')


# 用户看视频获取 金币奖励
@api_user.route('/look_video_coins', methods=['POST'])
@auth_required
def play_look_video():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        start_time = res.get('start_time')
        end_time = res.get('end_time')
        coin = res.get('coin')
        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, start_time, end_time, coin]):
            return jsonify(errno=-1, errmsg="参数不完整")
        try:
            user_id = int(user_id)
            start_time = int(start_time)
            end_time = int(end_time)
            coin = int(coin)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数类型错误')
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")
        play = LookVideoRecord()
        play.user_id = user_id
        play.coin = coin
        play.start_time = date_time(start_time)
        play.end_time = date_time(end_time)
        user_obj.coins += coin
        db.session.add(user_obj)
        db.session.add(play)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", total_coins=user_obj.coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 天降红包 list
@api_user.route('/heaven_for_list', methods=['POST'])
# @auth_required
def heaven_for_list():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")

        user_s_obj = HeavenForUserOpen.query.filter(HeavenForUserOpen.user_id == user_id,
                                                    HeavenForUserOpen.status == 0).all()
        arr = dict()
        arr['f_id'] = user_obj.id
        arr['f_openid'] = user_obj.openid
        arr['f_token'] = user_obj.token
        arr['f_nick_name'] = user_obj.nick_name
        arr['f_avatar_url'] = user_obj.avatar_url
        user_s_info = list()
        if user_s_obj:
            # 用成功邀请用户信息  查询新用户信息
            nuw_user_ids = [x.new_user_id for x in user_s_obj]
            new_user_list = User.query.filter(User.id.in_(nuw_user_ids)).limit(3).all()
            new_user_list_num = len(new_user_list)
            arr['user_count'] = new_user_list_num
            if new_user_list:
                for i in new_user_list:
                    new_user_info = dict()
                    nick_name = i.nick_name
                    openid = i.openid
                    token = i.token
                    s_id = i.id
                    avatar_url = i.avatar_url
                    new_user_info['s_id'] = s_id
                    new_user_info['s_openid'] = openid
                    new_user_info['s_nick_name'] = nick_name
                    new_user_info['s_token'] = token
                    new_user_info['s_avatar_url'] = avatar_url
                    # 邀请成功有新用户
                    user_s_info.append(new_user_info)
                if new_user_list_num == 2:
                    brr = dict()
                    brr['s_avatar_url'] = ''
                    user_s_info.append(brr)
                if new_user_list_num == 1:
                    brr = dict()
                    brr['s_avatar_url'] = ''
                    user_s_info.append(brr)
                    user_s_info.append(brr)
        else:
            for i in range(3):
                brr = dict()
                brr['s_avatar_url'] = ''
                user_s_info.append(brr)
            arr['user_count'] = ''
        arr['user_s_info'] = user_s_info
        return jsonify(errno=0, errmsg="OK", total_coins=arr)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 天降红包 open
@api_user.route('/heaven_for_open', methods=['POST'])
# @auth_required
def heaven_for_open():
    try:
        cion_nums = 200
        res = request.get_json()
        s_id = res.get('s_id')
        f_id = res.get('f_id')
        # 查询是否兑换过金币
        heavenred = HeavenRedRecord()
        is_true = HeavenRedRecord.query.filter(HeavenRedRecord.user_s_id == str(s_id)).first()
        if is_true:
            return jsonify(errno=-1, errmsg="请勿重复点击")
        if not all([s_id, f_id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        s_id_list = s_id.strip(',').split(',')
        coins_nums = len(s_id_list)
        if coins_nums < 3:
            return jsonify(errno=-1, errmsg="子用户少于三条")
        for x in s_id_list:
            results = HeavenForUserOpen.query.filter(HeavenForUserOpen.new_user_id == int(x)).first()
            if results:
                Logging.logger.info('用户:{0} 天降红包修改关联表'.format(f_id))
                results.status = 1
                # 1:天降红包关联用户表 用户信息
                db.session.add(results)
                db.session.commit()
        # 3:记录用户天降红包日志
        heavenred.user_s_id = s_id
        heavenred.coins = cion_nums
        heavenred.user_id = int(f_id)
        db.session.add(heavenred)
        db.session.commit()
        # 2:计算用户天降红包所得钢镚（总和记录）
        user_obj = User.query.get(f_id)
        user_obj.coins += cion_nums
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", cion_nums=cion_nums)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 天降红包分享增加用户
@api_user.route('/heaven_for_users', methods=['POST'])
@auth_required
def heaven_for_users():
    try:
        db = pymysql.connect(host="rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com", port=3306, user="maxpr_mysql",
                             password="COFdjwD*$*m8bd!HtMLP4+Az0eE9m",
                             charset="utf8")
        res = request.get_json()
        user_id = res.get('user_id')
        open_id = res.get('open_id')
        new_user_id = res.get('new_user_id')
        new_open_id = res.get('new_open_id')
        if not all([user_id, open_id, new_user_id, new_open_id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        cursor = db.cursor()
        timeStamp = int(time.time())
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        sql = f"INSERT INTO zjlivenew.zj_heaven_for_user(create_time,update_time,user_id,openid,new_user_id,new_openid,status)" \
              f"VALUES('{otherStyleTime}','{otherStyleTime}',{int(user_id)},'{open_id}',{int(new_user_id)},'{new_open_id}',{int(0)})"
        print(sql)
        cursor.execute(sql)
        db.commit()
        db.close()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 每日签到开红包 100 钢镚 随机
@api_user.route('/open_red_day', methods=['POST'])
@auth_required
def open_red_day():
    try:
        res = request.get_json()
        coins = int(random.randint(1, 100))
        user_id = res.get('user_id')
        if not all([user_id]):
            return jsonify(errno=-1, errmsg="参数不完整")
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg="参数错误")
        # 每日开钢镚奖励记录
        r = RedOpneDay()
        r.user_id = user_id
        r.coins = coins
        db.session.add(r)
        user_obj.coins += int(coins)
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
