# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 13:30 PM
# @Author  : Ligang
# @Email   : a289237642@163.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

api_video = Blueprint('api_video', __name__)

import app.Tvzhijian.pcvideos.video_info