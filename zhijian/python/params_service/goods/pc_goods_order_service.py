# -*- coding:utf-8 -*-
# author: will
from app.models import GoodsOrder
from common.error_code import ErrorCode
from utils.log_service import Logging


class BaseParamsCheck(object):

    @staticmethod
    def params_check(res):
        page = res.get('page')
        pagesize = res.get('pagesize')

        if not isinstance(page, int) or not isinstance(pagesize, int):
            Logging.logger.warning('there is params type error')
            return False, ErrorCode.params_type_error


class LsParamsCheck(BaseParamsCheck):

    @staticmethod
    def ls_params_check(res):
        order_status = res.get('order_status')
        if not order_status:
            Logging.logger.warning('there is missing a params named "order_status"')
            return False, ErrorCode.params_missing
        else:
            return True, ErrorCode.OK


class DetailParamsCheck(object):

    @staticmethod
    def detail_params_check(res):
        order_id = res.get('order_id')
        if not isinstance(order_id, int):
            return False, ErrorCode.params_type_error

        order = GoodsOrder.query.get(order_id)
        if not order:
            return False, ErrorCode.order_not_exist


class ExpressParamsCheck(DetailParamsCheck):

    @staticmethod
    def express_params_check(res):
        order_id = res.get('order_id')
        order = GoodsOrder.query.get(order_id)
        order_status = order.order_status
        print(order_status)
        if order_status in [1, 2]:
            return False, ErrorCode.order_status_error

