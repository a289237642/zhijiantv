# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 5:00 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

pcfileinfo = Blueprint('pcfileinfo', __name__)

import app.Tvzhijian.pcfileinfo.pc_fileinfo