# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 1:12 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

pcadmin = Blueprint('pcadmin', __name__)

import app.Tvzhijian.pcadmin.pc_admin
