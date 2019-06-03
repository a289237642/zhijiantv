# -*- coding:utf-8 -*-
# author: will

# coding: utf-8
from flask import jsonify

from common.error_code import ErrorCode


def build_response(data=None, errno=None, errmsg=None, **kwargs):

    if None is errno:
        errno = ErrorCode.OK[0]
    if None is errmsg:
        errmsg = ErrorCode.OK[1]
    response = jsonify(errno=errno, data=data, errmsg=errmsg)
    return response
