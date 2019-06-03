# -*- coding:utf-8 -*-
# author: will
import base64
import datetime
import logging
import random

import time

import pymysql
from lxml import etree

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymysql import connect
from selenium import webdriver

from app import mongo_store
from utils.article_service.keywords_filter import ArticleFilter
from utils.log_service import Logging
from utils.oss_service.storage import storage_by_url


class WechatUrlSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.article = dict()

    def get_article(self, url):
        # browser = webdriver.PhantomJS('/usr/local/phantomjs/bin/phantomjs')
        # 测试
        browser = webdriver.PhantomJS('/usr/local/lib/python3.5/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        # 正式
        # browser = webdriver.PhantomJS('/usr/local/lib/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

        browser.get(url)
        time.sleep(3)
        html = browser.page_source

        try:
            # 转换页面格式
            selector = etree.HTML(html)
            title = selector.xpath('//*[@id="activity-name"]/text()')[0]
            title = "".join(title.split())
            name = selector.xpath('//*[@id="js_name"]/text()')[0]
            name = "".join(name.split())
            # date = selector.xpath('//*[@id="publish_time"]/text()')[0]
            spider_time = time.time()
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(spider_time))
            self.article['title'] = title
            self.article['name'] = name
            self.article['date'] = date
            self.article['web_name'] = name
            is_original = selector.xpath('//*[@id="copyright_logo"]/text()')
            if len(is_original) == 0:
                self.article['is_original'] = 0  # 不是原创
            else:
                self.article['is_original'] = 1  # 是原创

            title_list = self.get_title_list(name)
            if title in title_list:
                # 文章已存在MySQL
                return -1

            # 用xpath取出需要的内容页面部分
            result = selector.xpath('//*[@id="js_content"]')[0]
            # 转为html
            content = etree.tostring(result, method='html')
            # 获取bs4对象
            soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
            new_list = []

            # 通过标签来获取内容
            # ls = soup.find_all(["a", "p", "img", "strong", "span"])
            ls = soup.find_all(["p", "img"])
            for table in ls:
                res = {}

                data = table.get_text()
                if data:
                    # 去除空字符和特殊字符
                    new_data = "".join(data.split())
                    new_data = new_data.replace('\ufeff', '')
                    if new_data != "":
                        res["text"] = new_data
                        new_list.append(res)

                link = table.get('data-src')
                if link:
                    Logging.logger.info("抓取到文章内图片链接link:{0}".format(link))
                    # 上传图片到oss
                    oss_url = self.upload_oss(link)
                    res["img"] = oss_url
                    # res["img"] = link
                    new_list.append(res)

            self.article['content'] = new_list
            browser.quit()
            Logging.logger.info('爬虫完成,进程退出')
            # print self.article
            return self.article
        except Exception as e:
            browser.quit()
            Logging.logger.error('errmsg:{0}'.format(e))
            return 1
        # finally:
        #     browser.quit()
        #     Logging.logger.info('爬虫中断,进程退出')
        #     return 1

    # 爬虫入口
    def start(self, url, admin_id):
        res = self.get_article(url)
        if res == 1:
            Logging.logger.info('该文章已被发布者删除')
            return 1
        elif res == -1:
            Logging.logger.info('该文章已存在MySQL')
            return -1
        else:
            web_name = res.get('name')
            title = res.get('title')
            content = res.get('content')
            # print web_name, title
            Logging.logger.info('准备分类')
            article_filter_obj = ArticleFilter(title, content)
            group_id_list = article_filter_obj.article_filter()
            Logging.logger.info('获取到的文章公众号是:{0},文章标题是:{1}'.format(web_name, title))
            result = self.upload_mysql(res['title'], res['name'], res['date'], res['web_name'], url, admin_id,
                                       res['is_original'], group_id_list)
            if isinstance(result, list):
                res['article_id'] = result[0]
                self.upload_mongo(res)
            Logging.logger.info('爬取完成')

    # 上传图片到oss
    def upload_oss(self, url):
        try:
            oss_url = storage_by_url(url)
            if oss_url:
                oss_url = oss_url.replace('maxpr.oss-cn-shanghai.aliyuncs.com', 'cdn.max-digital.cn')
                Logging.logger.info('oss_url=%s' % oss_url)
                return oss_url
            else:
                return None
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))

    # 数据上传mongo
    def upload_mongo(self, article_dict):
        try:
            mongo_store.articles.insert_one(article_dict)
            Logging.logger.info('上传到mongo成功')
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))

    # 插入到mysql
    def upload_mysql(self, title, name, date, web_name, url, admin_id, is_original, group_id_list):
        try:
            # 上传mysql
            # 创建Connection连接
            conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                           db='zjlive',
                           user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
            # 获得Cursor对象
            cursor = conn.cursor()
            data = list()
            # 执行insert语句，并返回受影响的行数：添加一条数据
            # 增加
            title = pymysql.escape_string(title)
            now = datetime.datetime.now()
            default_pic = "https://cdn.max-digital.cn/miniprogram/goose/image/mrtx@2x.png"
            sql1 = "insert into zj_article_info (title,author,wechat_art_date,is_show,is_big,web_name,round_head_img,link,admin_id,is_original,create_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                title, name, date, 0, 0, web_name, default_pic, url, admin_id, is_original, now)
            cursor.execute(sql1)
            article_id = int(conn.insert_id())
            data.append(article_id)
            Logging.logger.info("公众号:%s, 文章:%s, 插入成功, 获得文章ID: %s" % (web_name, title, article_id))

            if group_id_list:
                group_id_list = set(group_id_list)
                for group_id in group_id_list:
                    now2 = datetime.datetime.now()
                    # 文章自动上线到关键词对应的文章分类,并显示在最前
                    sql2 = 'insert into zj_article_group (article_id, group_id, sort_num, create_time) values ("%s", "%s", "%s", "%s")' % (
                        article_id, group_id, 1, now2)
                    cursor.execute(sql2)

                    sql3 = 'update zj_article_info set is_show = 1, zj_art_date="%s" where id="%s"' % (
                        now2, article_id)
                    cursor.execute(sql3)
                Logging.logger.info("公众号:%s,文章标题:%s, 自动上线成功" % (web_name, title))
                data.append(666)
            conn.commit()
            cursor.close()
            conn.close()
            return data
        except Exception as e:
            Logging.logger.error('公众号:%s,文章标题:%s,自动上线失败:' % (web_name, title))
            Logging.logger.error('errmsg:{0}'.format(e))
            return False

    def get_title_list(self, query):
        # 查询mysql
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zjlive',
                       user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()

        res = 'select title from zj_article_info where web_name = "%s" ' % query
        cs1.execute(res)
        docs = cs1.fetchall()

        title_list = []
        for doc in docs:
            recent_title = doc[0]
            title_list.append(recent_title)
        # print(title_list)
        cs1.close()
        conn.close()
        return title_list
