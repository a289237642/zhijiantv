# -*- coding:utf-8 -*-
# author: will
from datetime import datetime
from datetime import date, time
from flask_sqlalchemy import Model
from sqlalchemy.orm.query import Query
from sqlalchemy import DateTime, Numeric, Date, Time


def query_to_dict(models):
    if isinstance(models, list):
        # 对象列表
        if isinstance(models[0], Model):
            # Model对象
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0], g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            # 查询结果对象
            res = result_to_dict(models)
            return res
    else:
        # 单个对象
        if isinstance(models, Model):
            gen = model_to_dict(models)
            dit = dict((g[0], g[1]) for g in gen)
            return dit
        else:
            res = dict(list(zip(list(models.keys()), models)))
            find_datetime(res)
            return res


# 当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(list(zip(list(r.keys()), r))) for r in results]
    # 这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res


# 结果为Model中的模型类时
def model_to_dict(model):
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)


def find_datetime(value):
    for v in value:
        if isinstance(value[v], datetime):
            value[v] = convert_datetime(value[v])  # 这里修改的字典对象，不用返回即可修改


def convert_datetime(value):
    if value:
        if isinstance(value, (datetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
            return value.strftime("%H:%M:%S")
    else:
        return ""
