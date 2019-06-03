# -*- coding:utf-8 -*-
import datetime
import time


def strftime_to_str(my_time):
    # time.localtime将当前系统时间戳转化为struct_time格式
    local_date = time.localtime(int(my_time))

    # time.strftime将struct_time格式转成指定的字符串格式
    time_str = time.strftime("%Y-%m-%d", local_date)
    return time_str


def strftime_to_int(my_time):
    tm = time.strptime(my_time, '%Y-%m-%d')
    time_int = int(time.mktime(tm))
    return time_int


def get_time(my_time):
    # time.strptime将自定义时间格式的字符串转换为struct_time格式
    tm = time.strptime(my_time, '%Y-%m-%d %H:%M:%S')

    # time.mktime将struct_time格式转回成时间戳
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


def today_time():
    local_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d", local_time)
    tm = time.strptime(time_str, '%Y-%m-%d')
    time_int = int(time.mktime(tm))
    return time_str, time_int


def dif_time(data):
    # 计算两个时间之间差值
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    # 间隔天数
    day = (d2 - d1).days
    # 间隔秒数
    second = (d2 - d1).seconds
    # print day   #17
    # print second  #13475  注意这样计算出的秒数只有小时之后的计算额 也就是不包含天之间差数
    return second


def unix_time(dtime):
    # 将python的datetime转换为unix时间戳
    un_time = time.mktime(dtime.timetuple())
    return un_time


def date_time(unix_ts):
    # 将unix时间戳转换为python  的datetime
    times = datetime.datetime.fromtimestamp(unix_ts)
    return times  # 2017-11-02 23:29:45


def get_today():
    now = datetime.datetime.now()
    # 获取今天零点
    today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    return today


# 校验字符串日期是否有效
def vaild_date(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False
