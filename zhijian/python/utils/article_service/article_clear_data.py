# -*- coding:utf-8 -*-
# author: will
import datetime

from pymysql import connect

from .article_model_build import ArticleModel


def get_today():
    now = datetime.datetime.now()
    # 获取今天零点
    today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    return today


# 文章数据清理及模型重建
def article_clear():
    conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                   db='zjlivenew',
                   user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
    cs1 = conn.cursor()
    try:
        today = get_today()
        seven_day = today + datetime.timedelta(days=-7)  # 7天前
        sql = 'delete from zj_article_info where is_show=0 and wechat_art_date < "%s"' % seven_day
        num = cs1.execute(sql)

        obj = ArticleModel()
        obj.data_init()
        # cs1.close()
        # conn.close()
        print('成功清理了{0}篇爆料库文章'.format(num))
        return num
    except Exception as e:
        print(e)
        return False
    finally:
        cs1.close()
        conn.close()


if __name__ == '__main__':
    article_clear()

