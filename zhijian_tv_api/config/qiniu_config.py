# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 3:44 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : qiniu_config.py
# @Software: PyCharm

class QiniuConfig(object):
    _qn_conf = {
        'access_key': 'odg9fT6RUNON4MK8Lr_i-7DytJ1vP9a7b-W-pq7O',
        'secret_key': 'toKtxvWeZzIYnyOrsU4oiktJQ0Zl24OejY8_zGZY',
        'bucket_name': 'zhijiantv',
    }

    @classmethod
    def get_qn_access_key(cls):
        return cls._qn_conf.get('access_key')

    @classmethod
    def get_qn_secret_key(cls):
        return cls._qn_conf.get('secret_key')

    @classmethod
    def get_qn_bucket_name(cls):
        return cls._qn_conf.get('bucket_name')
