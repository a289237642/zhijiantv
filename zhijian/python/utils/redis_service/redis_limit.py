# -*- coding:utf-8 -*-
# author: will

# 商品库存并发限制
from app import redis_store


def limit_handler(keyname, amount_limit):

    incr_amount = 1  # 每次增加数量

    # 判断key是否存在
    if not redis_store.exists(keyname):
        # setnx可以防止并发时多次设置key,如果字段已经存在，setnx 命令将不执行任何操作
        redis_store.setnx(keyname, 0)

    # 数据插入后再判断是否大于限制数
    if redis_store.incrby(keyname, incr_amount) <= amount_limit:
        return True

    return False
