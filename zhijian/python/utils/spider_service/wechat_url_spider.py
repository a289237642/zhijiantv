# -*- coding:utf-8 -*-
# author: will
import datetime

import time

import pymysql
import lxml.html
etree = lxml.html.etree
from bs4 import BeautifulSoup
from pymysql import connect
from selenium import webdriver

from app import mongo_store
from utils.article_service.article_model_build import ArticleModel
from utils.log_service import Logging
from utils.oss_service.storage import storage_by_url
from utils.redis_service.Redis_Client import RedisClient


class wechat_url_spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.article = dict()

    def get_article(self, url):
        # 本地
        # browser = webdriver.PhantomJS('/usr/local/phantomjs/bin/phantomjs')
        # 测试
        # browser = webdriver.PhantomJS('/usr/local/lib/python3.5/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        # 正式
        browser = webdriver.PhantomJS('/usr/local/lib/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

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
                # pass

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
            # browser.quit()
            Logging.logger.info('爬虫完成,进程退出')
            Logging.logger.info(self.article)
            return self.article
        except Exception as e:
            # browser.quit()
            Logging.logger.error('爬虫中断,进程退出,errmsg:{0}'.format(e))
            return 1
        finally:
            browser.quit()

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
            Logging.logger.info("#" * 20)
            web_name = res.get('name')
            title = res.get('title')
            # 测试文章去重
            content = res.get('content')
            Logging.logger.info(title)
            sim_ls = ArticleModel().run(content)
            Logging.logger.info('对比文章相似度的结果:{0}'.format(sim_ls))
            if not sim_ls:
                Logging.logger.info('获取到的文章公众号是:{0},文章标题是:{1}'.format(web_name, title))
                resp = self.upload_mongo(res, title)
                if resp:
                    article_id = self.upload_mysql(res['title'], res['name'], res['date'], res['web_name'], url,
                                                   admin_id, res['is_original'])
                    print(('article_id=', article_id))
                    if article_id:
                        redis_client = RedisClient.create_redis_cli()
                        redis_client.rpush('article_id_list', article_id)
                Logging.logger.info('爬取完成')
            else:
                # sim_ls = [(1051, 1.0000005)]
                redis_client = RedisClient.create_redis_cli()
                sim_article_ids = [redis_client.lindex('article_id_list', item[0]) for item in sim_ls]
                Logging.logger.info('已存在相似度大于0.6的文章,相似文章ID:{0}'.format(sim_article_ids))
                return 2

    # 上传图片到oss
    @staticmethod
    def upload_oss(url):
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
    @staticmethod
    def upload_mongo(article_dict, title):
        try:
            articles = mongo_store.articles.find({'title': title})
            try:
                article = articles[0]
                Logging.logger.info('文章已存在MongoDB中,标题是:{0}'.format(title))
                return True
            except Exception as e:
                mongo_store.articles.insert_one(article_dict)
                Logging.logger.info('上传到mongo成功')
                return True
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return False

    # 插入到mysql
    @staticmethod
    def upload_mysql(title, name, date, web_name, url, admin_id, is_original):

        # 上传mysql
        # 创建Connection连接
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zjlivenew',
                       user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        # 执行insert语句，并返回受影响的行数：添加一条数据
        # 增加
        try:
            title = pymysql.escape_string(title)
            now = datetime.datetime.now()
            default_pic = "https://cdn.max-digital.cn/miniprogram/goose/image/mrtx@2x.png"
            sql = "insert into zj_article_info (title,author,wechat_art_date,is_show,is_big,web_name,round_head_img,link,admin_id,is_original,create_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                title, name, date, 0, 0, web_name, default_pic, url, admin_id, is_original, now)
            cs1.execute(sql)
            article_id = int(conn.insert_id())

            conn.commit()
            # cs1.close()
            # conn.close()
            Logging.logger.info('上传到mysql成功')
            return article_id
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return False
        finally:
            cs1.close()
            conn.close()

    @staticmethod
    def get_title_list(query):
        # 查询mysql
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zjlivenew',
                       user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        try:
            res = 'select title from zj_article_info where web_name = "%s" ' % query
            cs1.execute(res)
            docs = cs1.fetchall()

            title_list = []
            for doc in docs:
                recent_title = doc[0]
                title_list.append(recent_title)
            # print(title_list)
            # cs1.close()
            # conn.close()
            return title_list
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return False
        finally:
            cs1.close()
            conn.close()
