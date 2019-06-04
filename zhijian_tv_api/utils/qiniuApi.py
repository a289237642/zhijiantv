# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 3:38 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : qiniuApi.py
# @Software: PyCharm

import datetime
from qiniu import Auth, PersistentFop, build_op, op_save, urlsafe_base64_encode, put_file, etag
from config.qiniu_config import QiniuConfig
from qiniu import BucketManager


def file_oss(key, localfile):
    access_key = QiniuConfig.get_qn_access_key()
    secret_key = QiniuConfig.get_qn_secret_key()
    bucket_name = QiniuConfig.get_qn_bucket_name()
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, localfile)
    if info.status_code == 200:
        return {"errmsg": 0, "url": f"https://oss.max-tv.net.cn/{key}"}
    else:
        return {"errmsg": -1}


def get_oss_token(key):
    access_key = QiniuConfig.get_qn_access_key()
    secret_key = QiniuConfig.get_qn_secret_key()
    bucket_name = QiniuConfig.get_qn_bucket_name()
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, key, 3600)
    return token


if __name__ == "__main__":
    pass
    # a = get_file_info(key='luF-OClz4B5wIv-9Z5g25jTxabWF')
    # print(a)
