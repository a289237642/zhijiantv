# coding: utf-8

import time
import uuid
from datetime import datetime
from multiprocessing.pool import ThreadPool

from redlock import RedLock

from app import redis_store

CLOCK_DRIFT_FACTOR = 0.01


class MyRedLock(RedLock):
    """
    重写 RedLock类，用于应对分配时的特殊场景：
       分配时给数据上锁的过程中如果发现锁被占用，说明有其它场景在对未分配的数据进行操作，此时分配应当直接跳过这个数据，不参与分配；
       所以添加 self.wait属性并重写 acquire方法，self.wait为 False时，发现锁已被占用不等待不重试，直接返回 False
    """

    def __init__(self, resource, connection_details, retry_times=None, retry_delay=None, ttl=None,
                 created_by_factory=None, wait=True):
        params_dict = dict(resource=resource, connection_details=connection_details)
        if retry_times:
            params_dict['retry_times'] = retry_times
        if retry_delay:
            params_dict['retry_delay'] = retry_delay
        if ttl:
            params_dict['ttl'] = ttl
        if created_by_factory:
            params_dict['created_by_factory'] = created_by_factory

        super(MyRedLock, self).__init__(**params_dict)
        self.wait = wait

    def acquire(self):

        # lock_key should be random and unique
        self.lock_key = uuid.uuid4().hex

        for retry in range(self.retry_times):
            acquired_node_count = 0
            start_time = datetime.utcnow()

            # acquire the lock in all the redis instances sequentially
            for node in self.redis_nodes:
                result = self.acquire_node(node)
                if not self.wait and not result:
                    return False
                elif result:
                    acquired_node_count += 1

            end_time = datetime.utcnow()
            elapsed_milliseconds = self._total_ms(end_time - start_time)

            # Add 2 milliseconds to the drift to account for Redis expires
            # precision, which is 1 milliescond, plus 1 millisecond min drift
            # for small TTLs.
            drift = (self.ttl * CLOCK_DRIFT_FACTOR) + 2

            if acquired_node_count >= self.quorum and \
                    self.ttl > (elapsed_milliseconds + drift):
                return True
            else:
                for node in self.redis_nodes:
                    self.release_node(node)
                time.sleep(self.retry_delay)
        return False


class RedisLock(object):

    def __init__(self, keys, retry_times=50, retry_delay=0.1, ttl=None, wait=True):
        self.redis = redis_store
        self.lock_prefix = 'redis_lock:'
        self.keys = keys if isinstance(keys, (list, tuple)) else [keys]
        self.retry_times = retry_times  # 重试次数
        self.retry_delay = retry_delay  # 每次重试的间隔 单位：s
        self.ttl = ttl  # 锁的存活时间 单位：ms
        self.wait = wait  # 是否要等待锁
        self.lock_list = []
        self.failed_keys = []

    def _lock_one(self, key):
        lock = MyRedLock(resource=self.lock_prefix + str(key),
                         connection_details=[self.redis],
                         retry_times=self.retry_times,
                         retry_delay=self.retry_delay,
                         ttl=self.ttl,
                         wait=self.wait)
        result = lock.acquire()
        if not result:
            self.failed_keys.append(key)
        else:
            self.lock_list.append(lock)

    def lock(self):
        pool = ThreadPool(100)  # 开启线程池，最优线程数需在线上环境测试

        for key in self.keys:
            pool.apply_async(self._lock_one, args=(key,))

        pool.close()
        pool.join()
        return self.failed_keys

    def release(self):
        pool = ThreadPool(100)  # 开启线程池，最优线程数需在线上环境测试

        for lock in self.lock_list:
            pool.apply_async(lock.release)

        pool.close()
        pool.join()


if __name__ == '__main__':
    keys = [x for x in range(1000)]
    redis_lock = RedisLock(keys, wait=False)
    print(redis_lock.lock())
    redis_lock.release()
