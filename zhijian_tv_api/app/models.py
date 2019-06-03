# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 1:58 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : model.py
# @Software: PyCharm

from datetime import datetime
from app import db


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    admin_id = db.Column(db.Integer, index=True)  # 数据的最后更新人


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "tv_user_info"

    id = db.Column(db.Integer, unique=True, primary_key=True)  # 用户id
    user_name = db.Column(db.String(255), index=True)  # 账号
    pass_word = db.Column(db.String(255), index=True)  # 账号
    status = db.Column(db.String(255), index=True)  # 状态值
    siuper = db.Column(db.Integer, default=0)  # 超级账号


class VideoInfo(BaseModel, db.Model):
    """视频"""
    __tablename__ = "tv_video_info"

    id = db.Column(db.Integer, unique=True, primary_key=True)  # 视频id
    vtype = db.Column(db.Integer, db.ForeignKey("tv_video_type.id"))  # 视频分类  创建对应关系
    title = db.Column(db.String(255), index=True)  # 视频标题
    summary = db.Column(db.String(255), default='')  # 视频简介
    url = db.Column(db.String(255), default='')  # 视频url
    pic_url = db.Column(db.String(255), default='')  # 视频图url
    play_nums = db.Column(db.Integer, default=0)  # 播放次数
    play_times = db.Column(db.String(11))  # 视频时长
    is_show = db.Column(db.Integer, default=0, index=True)  # 精选状态 0不显示　1显示
    status = db.Column(db.Integer, default=0, index=True)  # 上架状态 0不显示　1显示


class VideoType(BaseModel, db.Model):
    """视频分类"""
    __tablename__ = "tv_video_type"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(255), index=True)  # 分类标题
    summary = db.Column(db.String(255), default='')  # 分类简介
    url = db.Column(db.String(255), default='')  # 分类图片
    cross_url = db.Column(db.String(255), default='')  # 分类图片
    status = db.Column(db.Integer, default=0, index=True)  # 分类状态 0不显示　1显示
