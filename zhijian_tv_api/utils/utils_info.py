# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 4:16 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : utils.py
# @Software: PyCharm
from moviepy.editor import VideoFileClip
import datetime, time, requests, random
from config.wx_config import WxConfig



def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        WxConfig.get_wx_appid(), WxConfig.get_wx_appsecret())
    resp_data = requests.get(url=url)
    resp_dict = resp_data.json()
    if 'errcode' in resp_dict:
        raise Exception(resp_dict.get('errmsg'))
    access_token = resp_dict.get('access_token')
    return access_token


def get_time(my_time):
    """
    计算 时间
    注意格式str
    """
    tm = time.strptime(my_time, '%Y-%m-%d %H:%M:%S')
    tm = int(time.mktime(tm))
    now_tm = int(time.time())
    new_tm = now_tm - tm
    if new_tm <= 60:
        return '%s秒前' % int(new_tm)
    elif 60 < new_tm <= 60 * 60:
        return '%s分钟前' % (int(new_tm / 60))
    elif 60 * 60 < new_tm <= 60 * 60 * 24:
        return '%s小时前' % (int(new_tm / (60 * 60)))
    else:
        return '%s天前' % (int(new_tm / (60 * 60 * 24)))


def get_today():
    """
    获取今天零点
    """
    now = datetime.datetime.now()
    today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    return today


def random_str(length):
    """
    产生随机字符串，不长于32位
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    strs = []
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])
    return "".join(strs)


def get_file_times(filename):
    """
    获取视频时长（s:秒）
    """
    clip = VideoFileClip(filename)
    data = clip.duration
    file_time = timeConvert(data)
    clip.reader.close()
    clip.audio.reader.close_proc()
    return file_time


def timeConvert(size):
    """
    单位换算（s:秒）
    """
    M, H = 60, 60 ** 2
    if size < M:
        return '%s:%s:%s' % ('00', '00', '%02d' % int(size))
    if size < H:
        return '%s:%s:%s' % ('00', '%02d' % int(size / M), '%02d' % int(size % M))
    else:
        hour = '%02d' % int(size / H)
        mine = '%02d' % int(size % H / M)
        second = '%02d' % int(size % H % M)
        tim_srt = '%s:%s:%s' % (hour, mine, second)
        return tim_srt
