# -*- coding:utf-8 -*-
# author: will
from flask import Blueprint

api_lesson = Blueprint('api_lesson', __name__)

from . import lesson_info, icon_info, lesson_audio,business_info


@api_lesson.after_request
def after_request(response):
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response
