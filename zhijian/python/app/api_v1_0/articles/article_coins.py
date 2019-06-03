# -*- coding:utf-8 -*-
# author: will
import datetime
import random
import time

from flask import request, jsonify

from app import db
from app.models import User, UserSteps, UserFriends, Article, UserReadArticle, UserShareArticle, UserSign
from utils.log_service import Logging
from utils.time_service import dif_time
from utils.user_service.login import auth_required
from . import api_article


# 步数兑换
# 步数与钢镚兑换规则:1步=0.001枚钢镚-->春节双倍
# 每日0点用户步数清零
@api_article.route('/change_steps', methods=['POST'])
@auth_required
def change_steps():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            user_id = int(user_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        available_step = user_obj.available_step
        coins = float('%.2f' % (available_step * 0.001))
        # coins = float('%.2f' % (available_step * 0.002))
        if available_step != 0:
            user_step = UserSteps()
            user_step.user_id = user_id
            user_step.change_step = available_step
            user_step.get_coins = coins
            user_step.change_step_date = datetime.datetime.now()
            user_obj.coins += coins
            user_obj.available_step = 0
            user_obj.change_steal_step = user_obj.steal_step

            db.session.add(user_step)
            db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=coins, total_coins=user_obj.coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='兑换失败')


# 计算步数兑换结果
@api_article.route('/step_to_coin', methods=['POST'])
@auth_required
def step_to_coin():
    try:
        res = request.get_json()
        steps = res.get('steps')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            steps = int(steps)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        coins = float('%.2f' % (steps * 0.001))
        # coins = float('%.2f' % (steps * 0.002))
        return jsonify(errno=0, errmsg="OK", coins=coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='兑换失败')


# 随机奖励--春节翻倍
@api_article.route('/get_random_coins', methods=['POST'])
@auth_required
def get_random_coins():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        get_type = res.get('get_type')  # 1:签到后转发, 2:兑换步数后转发
        openGId = res.get('openGId')  # 用户分享的微信群的唯一标识

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, get_type, openGId]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            user_id = int(user_id)
            get_type = int(get_type)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        coins = random.uniform(0.5, 2)
        # coins = random.uniform(1, 4)
        coins = float('%.2f' % coins)
        user_obj.coins += coins

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)

        if get_type == 1:
            share = UserSign.query.filter(UserSign.user_id == user_id,
                                          UserSign.openGId == openGId,
                                          UserSign.create_time >= today).first()
            if share:
                return jsonify(errno=-1, errmsg='今日已获得当前群奖励')
            else:
                sign_obj = UserSign.query.filter(UserSign.user_id == user_id, UserSign.create_time >= today).first()
                sign_obj.random_coin = coins
                sign_obj.openGId = openGId
                db.session.add(sign_obj)
        elif get_type == 2:
            share = UserSteps.query.filter(UserSteps.user_id == user_id,
                                           UserSteps.openGId == openGId,
                                           UserSteps.create_time >= today).first()
            if share:
                return jsonify(errno=-1, errmsg='今日已获得当前群奖励')
            else:
                change_obj = UserSteps.query.filter(UserSteps.user_id == user_id,
                                                    UserSteps.create_time >= today).first()
                change_obj.random_coin = coins
                change_obj.openGId = openGId
                db.session.add(change_obj)
        else:
            pass

        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=coins, total_coins=user_obj.coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='兑换失败')


# 每日签到奖励钢镚5个-->春节翻倍
@api_article.route('/sign_today', methods=['POST'])
@auth_required
def sign_today():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        last_day = user_obj.sign_time
        sign_coin = user_obj.sign_coin
        if not last_day:
            user_obj.coins += sign_coin
            user_obj.is_sign = 1
            user_obj.sign_time = datetime.datetime.now()
            # 用户每日签到记录
            sign_obj = UserSign()
            sign_obj.user_id = user_id
            sign_obj.sign_coin = sign_coin
        else:
            today = datetime.date.today()
            today_time = int(time.mktime(today.timetuple()))
            last_time = int(time.mktime(last_day.timetuple()))
            if user_obj.is_sign == 0 or (last_time - today_time) <= 0:
                user_obj.coins += sign_coin
                user_obj.is_sign = 1
                user_obj.sign_time = datetime.datetime.now()
                sign_obj = UserSign()
                sign_obj.user_id = user_id
                sign_obj.sign_coin = sign_coin
            else:
                coins = 0
                return jsonify(errno=0, errmsg="今天已经完成签到了,明天再来吧", coins=coins, total_coins=user_obj.coins)

        db.session.add(user_obj)
        db.session.add(sign_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=sign_coin, total_coins=user_obj.coins)

    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 好友点击分享卡片
@api_article.route('/invite_friend', methods=['POST'])
@auth_required
def invite_friend():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        friend_id = res.get('friend_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, friend_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        friend_obj = User.query.get(friend_id)
        if not user_obj or not friend_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        if user_id == friend_id:
            return jsonify(errno=-1, errmsg='参数错误')

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
        user_friend = UserFriends.query.filter(UserFriends.user_id == user_id, UserFriends.friend_id == friend_id,
                                               UserFriends.create_time >= today).first()
        if user_friend:
            return jsonify(errno=-1, errmsg='您今天已经被偷取过了')
        else:
            friends_num = UserFriends.query.filter(UserFriends.user_id == user_id, UserFriends.steal_num > 0,
                                                   UserFriends.create_time >= today).count()
            if friends_num < 5:
                obj = UserFriends()
                obj.friend_id = friend_id
                obj.user_id = user_id
                db.session.add(obj)
            else:
                return jsonify(errno=-1, errmsg='您好友的可偷取位置已满')
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 今日可偷取好友列表
@api_article.route('/steal_friend_list', methods=['POST'])
@auth_required
def steal_friend_list():
    try:
        res = request.get_json()
        user_id = res.get('user_id')

        Logging.logger.info('request_args:{0}'.format(res))
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)

        friends = UserFriends.query.filter(UserFriends.user_id == user_id, UserFriends.steal_num > 0,
                                           UserFriends.create_time >= today).all()
        friends_num = len(friends)
        friends_info = list()
        for friend in friends:
            friends_dict = dict()
            friend_id = friend.friend_id
            friend_obj = User.query.get(friend_id)
            friends_dict['avatar_url'] = friend_obj.avatar_url
            friends_dict['steal_num'] = friend.steal_num
            friends_dict['friend_id'] = friend_id
            steal_date = friend.steal_date
            if steal_date:
                un_time = time.mktime(steal_date.timetuple())
                friends_dict['steal_date'] = un_time
            else:
                friends_dict['steal_date'] = None

            # steal_date = friend.steal_date
            # steal_num = friend.steal_num
            # if steal_date and steal_num > 0:
            #     mistiming = dif_time(str(steal_date))
            #     if mistiming <= 60 * 5:
            #         mistiming = 60 * 5 - mistiming
            #         friends_dict['mistiming'] = mistiming
            #     else:
            #         friends_dict['mistiming'] = 0
            # elif not steal_date:
            #     friends_dict['mistiming'] = 0
            # else:
            #     pass
            friends_info.append(friends_dict)

        return jsonify(errno=0, errmsg="OK", friends_info=friends_info, friends_num=friends_num)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# 偷取好友步数/5分钟后才可以偷取第二次
@api_article.route('/steal_friend_step', methods=['POST'])
@auth_required
def steal_friend_step():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        friend_id = res.get('friend_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, friend_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        friend_obj = User.query.get(friend_id)
        if not user_obj or not friend_obj:
            return jsonify(errno=-1, errmsg='用户不存在')

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
        user_friend = UserFriends.query.filter(UserFriends.user_id == user_id, UserFriends.friend_id == friend_id,
                                               UserFriends.create_time >= today).first()
        if not user_friend:
            return jsonify(errno=-1, errmsg='该好友未被邀请')

        steal_date = user_friend.steal_date
        if not steal_date:
            user_friend.steal_num -= 1
            # user_obj.available_step += 1000
            user_obj.steal_step += 1000
            # print '偷取的步数累计:', user_obj.steal_step
            user_friend.steal_date = datetime.datetime.now()
        else:
            if user_friend.steal_num <= 0:
                return jsonify(errno=0, errmsg="请换个好友偷取吧")
            else:
                mistiming = dif_time(str(steal_date))
                if mistiming < 60 * 5:
                    return jsonify(errno=-1, errmsg="请在%s秒后再来偷取吧" % (60 * 5 - mistiming))
                else:
                    user_friend.steal_num -= 1
                    # user_obj.available_step += 1000
                    user_obj.steal_step += 1000
                    # print '偷取的步数累计=', user_obj.steal_step
                    user_friend.steal_date = datetime.datetime.now()

        db.session.add(user_obj)
        db.session.add(user_friend)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('[api/steal_friend_step] errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 每人每天阅读前10次奖励1钢镚-->改为前5次,奖励随机值(0,1)-->春节翻倍
@api_article.route('/read_article_for_coin', methods=['POST'])
@auth_required
def read_article_for_coin():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        article_id = res.get('article_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, article_id]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        article_obj = Article.query.get(article_id)
        if not user_obj or not article_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)

        num = UserReadArticle.query.filter(UserReadArticle.user_id == user_id,
                                           UserReadArticle.create_time >= today).count()
        Logging.logger.info('已阅读文章次数={0}'.format(num))
        if num >= 5:
            return jsonify(errno=-1, errmsg='每人每天只有前5次阅读文章才可以拿奖励哦')

        obj = UserReadArticle.query.filter(UserReadArticle.user_id == user_id,
                                           UserReadArticle.article_id == article_id,
                                           UserReadArticle.create_time >= today).first()
        if obj:
            return jsonify(errno=-1, errmsg='今日已获得当前文章奖励')
        else:
            random_coins = float('%.2f' % random.uniform(0, 1))
            # random_coins = float('%.2f' % random.uniform(1, 2))
            user_obj.coins += random_coins

            user_article = UserReadArticle()
            user_article.article_id = article_id
            user_article.user_id = user_id
            user_article.random_coins = random_coins

            db.session.add(user_article)
            db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=random_coins, total_coins=user_obj.coins, num=num)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 每人每天分享前10次奖励2钢镚-->修改为1-3随机值,无限制分享次数
@api_article.route('/share_article_for_coin', methods=['POST'])
@auth_required
def share_article_for_coin():
    try:
        res = request.get_json()
        user_id = res.get('user_id')
        article_id = res.get('article_id')
        # friend_id = res.get('friend_id')
        openGId = res.get('openGId')  # 用户分享的微信群的唯一标识

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([user_id, article_id, openGId]):
            return jsonify(errno=-1, errmsg='参数不完整')

        user_obj = User.query.get(user_id)
        article_obj = Article.query.get(article_id)
        # friend_obj = User.query.get(friend_id)
        if not user_obj or not article_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        # if user_id != friend_id:
        #     return jsonify(errno=-1, errmsg='分享人本人未点击')

        now = datetime.datetime.now()
        # 获取今天零点
        today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)

        # obj = UserShareArticle.query.filter(UserShareArticle.user_id == user_id,
        #                                     UserShareArticle.article_id == article_id,
        #                                     UserShareArticle.create_time >= today).first()
        # if obj:
        #     return jsonify(errno=-1, errmsg='今日已获得当前文章奖励')
        # else: 同一篇文章每日分享次数限制的话,无法进行分享后的继续挖币
        # share = UserShareArticle.query.filter(UserShareArticle.user_id == user_id,
        #                                       UserShareArticle.openGId == openGId,
        #                                       UserShareArticle.article_id == article_id,
        #                                       UserShareArticle.create_time >= today).first()
        # 最新逻辑
        share = UserShareArticle.query.filter(UserShareArticle.user_id == user_id,
                                              UserShareArticle.openGId == openGId,
                                              UserShareArticle.create_time >= today).first()
        if share:
            return jsonify(errno=-1, errmsg='今天已经分享过了明天再来吧')
        share_nums = UserShareArticle.query.filter(UserShareArticle.user_id == user_id,
                                                   UserShareArticle.create_time >= today).count()
        if share_nums:
            return jsonify(errno=-1, errmsg='你分享的次数已达到上限明天再来吧')

        random_coins = float('%.2f' % random.uniform(20, 30))
        # random_coins = float('%.2f' % random.uniform(2, 6))
        user_obj.coins += random_coins

        user_article = UserShareArticle()
        user_article.article_id = article_id
        user_article.user_id = user_id
        user_article.openGId = openGId
        user_article.random_coins = random_coins
        # user_article.friend_id = friend_id

        db.session.add(user_article)
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK", coins=random_coins, total_coins=user_obj.coins)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')
