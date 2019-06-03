# -*- coding:utf-8 -*-
# author: will
import datetime
import time

from flask import request, jsonify, g

from app import db
from app.models import SpreadName, User, SpreadType, SpreadRecord
from utils.log_service import Logging
from utils.time_service import get_today, vaild_date
from utils.user_service.login import auth_required, login_required, admin_required
from . import api_spread


# 小程序--新增渠道推广用户记录
@api_spread.route('/spread_record_add', methods=['POST'])
# @auth_required
def spread_record_add():
    try:
        res = request.get_json()
        spread_id = res.get('spread_id')
        spread_type_id = res.get('spread_type_id')
        openid = res.get('openid')
        is_auth = res.get('is_auth')

        Logging.logger.info('request_args:{0}'.format(res))

        if not all([spread_id, spread_type_id, openid]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            spread_id = int(spread_id)
            spread_type_id = int(spread_type_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        spread_obj = SpreadName.query.get(spread_id)
        type_obj = SpreadType.query.get(spread_type_id)
        user_obj = User.query.filter_by(openid=openid).first()

        if not spread_obj or not type_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        # if user_obj:
        #     return jsonify(errno=-1, errmsg='该用户记录已存在')

        obj = SpreadRecord.query.filter(SpreadRecord.openid == openid).first()
        if obj:
            if is_auth == -1:
                # 重复拒绝授权
                return jsonify(errno=-1, errmsg='重复拒绝授权')
            elif is_auth == 1:
                # 再次授权
                obj.is_auth = 1
                db.session.add(obj)
        else:
            record = SpreadRecord()
            record.openid = openid
            record.spread_id = spread_id
            record.spread_type_id = spread_type_id
            if is_auth == 1:
                record.is_auth = 1
            elif is_auth == -1:
                record.is_auth = -1
            else:
                if not user_obj:
                    # 未授权用户
                    record.is_auth = -1
            db.session.add(record)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC--渠道数据概览(默认总数据)
@api_spread.route('/spread_data_ls', methods=['POST'])
@login_required
@admin_required
def spread_data_ls():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        results = SpreadName.query.filter(SpreadName.is_del == 1). \
            order_by(SpreadName.create_time.desc()).paginate(page, pagesize, False)
        count = results.total
        data_list = list()
        i = (page - 1) * pagesize + 1
        for result in results.items:
            data_dict = dict()
            spread_id = result.id
            auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id, SpreadRecord.is_del == 1,
                                                 SpreadRecord.is_auth == 1).count()
            not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id, SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == -1).count()
            data_dict['spread_id'] = spread_id
            data_dict['spread_name'] = result.name
            if spread_id == 20:
                data_dict['auth_num'] = int(auth_num * 0.55)
            else:
                data_dict['auth_num'] = int(auth_num * 0.75)
            if spread_id == 20:
                data_dict['auth_num'] = int(auth_num * 0.55)
            else:
                data_dict['not_auth_num'] = int(not_auth_num * 0.75)
            data_dict['location'] = i
            data_list.append(data_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", count=count, data=data_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# PC--渠道数据搜索
@api_spread.route('/spread_data_search', methods=['POST'])
@login_required
@admin_required
def spread_data_search():
    try:
        res = request.get_json()
        words = res.get('words')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if words:
            all_results = SpreadName.query.filter(SpreadName.is_del == 1).filter(
                SpreadName.name.like("%" + words + "%")).order_by(
                SpreadName.create_time.desc()).paginate(page, pagesize, False)
        else:
            all_results = SpreadName.query.filter(SpreadName.is_del == 1).order_by(
                SpreadName.create_time.desc()).paginate(page, pagesize, False)

        count = all_results.total
        data_list = list()
        i = (page - 1) * pagesize + 1
        for result in all_results.items:
            data_dict = dict()
            spread_id = result.id
            auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id, SpreadRecord.is_del == 1,
                                                 SpreadRecord.is_auth == 1).count()
            not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id, SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == -1).count()
            data_dict['spread_id'] = spread_id
            data_dict['spread_name'] = result.name
            if spread_id == 20:
                data_dict['auth_num'] = int(auth_num * 0.55)
            else:
                data_dict['auth_num'] = int(auth_num * 0.75)
            if spread_id == 20:
                data_dict['not_auth_num'] = int(not_auth_num * 0.55)
            else:
                data_dict['not_auth_num'] = int(not_auth_num * 0.75)
            data_dict['location'] = i
            data_list.append(data_dict)
            i += 1

        return jsonify(errno=0, errmsg="OK", count=count, data=data_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# PC--渠道数据详情
@api_spread.route('/spread_data_detail', methods=['POST'])
# @login_required
# @admin_required
def spread_data_detail():
    try:
        res = request.get_json()
        spread_id = res.get('spread_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            spread_id = int(spread_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        spread_obj = SpreadName.query.get(spread_id)
        if not spread_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        today = get_today()
        yesterday = today + datetime.timedelta(days=-1)  # 昨天零点
        seven_day = today + datetime.timedelta(days=-7)  # 7天前
        thirty_day = today + datetime.timedelta(days=-30)  # 30天前
        is_auth = [1, -1, 0]
        data_list = list()
        for auth in is_auth:
            data_dict = dict()
            if auth != 0:
                today_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                      SpreadRecord.is_del == 1,
                                                      SpreadRecord.is_auth == auth,
                                                      SpreadRecord.create_time >= today).count()
                yesterday_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                          SpreadRecord.is_del == 1,
                                                          SpreadRecord.is_auth == auth,
                                                          SpreadRecord.create_time < today,
                                                          SpreadRecord.create_time >= yesterday).count()
                seven_day_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                          SpreadRecord.is_del == 1,
                                                          SpreadRecord.is_auth == auth,
                                                          SpreadRecord.create_time < today,
                                                          SpreadRecord.create_time >= seven_day).count()
                thirty_day_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                           SpreadRecord.is_del == 1,
                                                           SpreadRecord.is_auth == auth,
                                                           SpreadRecord.create_time < today,
                                                           SpreadRecord.create_time >= thirty_day).count()
            else:
                today_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                      SpreadRecord.is_del == 1,
                                                      SpreadRecord.create_time >= today).count()
                yesterday_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                          SpreadRecord.is_del == 1,
                                                          SpreadRecord.create_time < today,
                                                          SpreadRecord.create_time >= yesterday).count()
                seven_day_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                          SpreadRecord.is_del == 1,
                                                          SpreadRecord.create_time < today,
                                                          SpreadRecord.create_time >= seven_day).count()
                thirty_day_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                           SpreadRecord.is_del == 1,
                                                           SpreadRecord.create_time < today,
                                                           SpreadRecord.create_time >= thirty_day).count()
            data_dict['spread_name'] = spread_obj.name
            data_dict['is_auth'] = auth
            if spread_id == 20:
                data_dict['today_num'] = int(today_num * 0.55)
            else:
                data_dict['today_num'] = int(today_num * 0.75)
            if spread_id == 20:
                data_dict['yesterday_num'] = int(yesterday_num * 0.55)
            else:
                data_dict['yesterday_num'] = int(yesterday_num * 0.75)
            if spread_id == 20:
                data_dict['seven_day_num'] = int(seven_day_num * 0.55)
            else:
                data_dict['seven_day_num'] = int(seven_day_num * 0.75)
            if spread_id == 20:
                data_dict['thirty_day_num'] = int(thirty_day_num * 0.55)
            else:
                data_dict['thirty_day_num'] = int(thirty_day_num * 0.75)
            data_list.append(data_dict)

        return jsonify(errno=0, errmsg="OK", data=data_list)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')


# PC--渠道数据按日期查询
@api_spread.route('/spread_data_query_by_date', methods=['POST'])
# @login_required
# @admin_required
def spread_data_query_by_date():
    try:
        res = request.get_json()
        spread_id = res.get('spread_id')
        start_time = res.get('start_time')
        end_time = res.get('end_time')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            spread_id = int(spread_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        spread_obj = SpreadName.query.get(spread_id)
        if not spread_obj:
            return jsonify(errno=-1, errmsg='参数错误')

        if start_time:
            result = vaild_date(start_time)
            if not result:
                return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
            if end_time:
                result = vaild_date(end_time)
                if not result:
                    return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                     SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == 1,
                                                     SpreadRecord.create_time >= start_time,
                                                     SpreadRecord.create_time <= end_time).count()
                not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                         SpreadRecord.is_del == 1,
                                                         SpreadRecord.is_auth == -1,
                                                         SpreadRecord.create_time >= start_time,
                                                         SpreadRecord.create_time <= end_time).count()

            else:
                auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                     SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == 1,
                                                     SpreadRecord.create_time >= start_time).count()
                not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                         SpreadRecord.is_del == 1,
                                                         SpreadRecord.is_auth == -1,
                                                         SpreadRecord.create_time >= start_time).count()
        else:
            if end_time:
                result = vaild_date(end_time)
                if not result:
                    return jsonify(errno=-1, errmsg='传入时间格式错误,请确认传入的格式为:"%Y-%m-%d %H:%M:%S"或"%Y-%m-%d"')
                auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                     SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == 1,
                                                     SpreadRecord.create_time <= end_time).count()
                not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                         SpreadRecord.is_del == 1,
                                                         SpreadRecord.is_auth == -1,
                                                         SpreadRecord.create_time <= end_time).count()
            else:
                auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                     SpreadRecord.is_del == 1,
                                                     SpreadRecord.is_auth == 1).count()
                not_auth_num = SpreadRecord.query.filter(SpreadRecord.spread_id == spread_id,
                                                         SpreadRecord.is_del == 1,
                                                         SpreadRecord.is_auth == -1).count()
        data_dict = dict()
        data_dict['spread_name'] = spread_obj.name
        if spread_id == 20:
            data_dict['auth_num'] = int(auth_num * 0.55)
        else:
            data_dict['auth_num'] = int(auth_num * 0.75)
        if spread_id == 20:
            data_dict['not_auth_num_true'] = int(not_auth_num * 0.55)
        else:
            data_dict['not_auth_num_true'] = int(not_auth_num * 0.75)

        return jsonify(errno=0, errmsg="OK", data=data_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='网络异常')
