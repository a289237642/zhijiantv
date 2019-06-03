# -*- coding:utf-8 -*-
# author: will
import json
import re
import time

import requests

from app import redis_store
from utils.log_service import Logging

from utils.redis_service.Redis_Client import RedisClient


# 单个接口的用户访问限制
def has_limit(openid, api):
    result = redis_store.hexists(name=openid, key=api)
    now = int(time.time())
    data = {"times": 1, "ttl": now}

    redis_cli = RedisClient.create_redis_cli()

    if not result:
        redis_cli.hset(name=openid, key=api, value=json.dumps(data))
    else:

        res = redis_cli.hget(name=openid, key=api)
        res = json.loads(res)
        Logging.logger.info('用户接口访问状态:{0}'.format(res))

        times = res.get('times')
        ttl = res.get('ttl')
        if times >= 10:
            if now - ttl <= 90:
                return True  # 超出访问限制, 30s后可访问
            else:
                redis_cli.hdel(openid, api)
        if now - ttl <= 60:
            data['times'] = times + 1
            data['ttl'] = ttl
            redis_cli.hset(name=openid, key=api, value=json.dumps(data))
        else:
            redis_cli.hdel(openid, api)
    return False


# def get_user_ip():
#     url = 'https://pv.sohu.com/cityjson?ie=utf-8'
#     data = requests.get(url)
#     text = data.text
#     print(text)
#     res = re.findall(r"= (.+?);", text)[0]
#     fin = json.loads(res)
#     ip = fin.get('cip')
#     print(ip)
#     return ip
