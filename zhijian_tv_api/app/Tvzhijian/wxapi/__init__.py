# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 1:00 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

wxapi = Blueprint('wx_api', __name__)

import app.Tvzhijian.wxapi.wx_info
