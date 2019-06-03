# -*- coding:utf-8 -*-
# author: will
import re


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""

    if uchar >= '/u4e00' and uchar <= '/u9fa5':

        return True

    else:

        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""

    if uchar >= '/u0030' and uchar <= '/u0039':

        return True

    else:

        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""

    if (uchar >= '/u0041' and uchar <= '/u005a') or (uchar >= '/u0061' and uchar <= '/u007a'):

        return True

    else:

        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""

    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):

        return True

    else:

        return False


# 移除表情特殊符号
emoji_pattern = re.compile(
    "(\ud83d[\ude00-\ude4f])|"  # emoticons
    "(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    "(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    "(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    "(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


def remove_emoji(text):
    return emoji_pattern.sub(r'', text)
