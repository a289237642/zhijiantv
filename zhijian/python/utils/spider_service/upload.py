# -*- coding:utf-8 -*-
# author: will
import datetime

from pymongo import MongoClient
from pymysql import connect

from app.models import Article
from utils.log_service import Logging
from utils.oss_service.storage import storage_by_url


# 接收神箭手数据使用
from utils.redis_service.Redis_Client import RedisClient


class Upload(object):

    # 上传图片到oss
    @staticmethod
    def upload_oss(url):
        try:
            # res = requests.get(url)
            # data = base64.b64encode(res.content)
            # kw = {
            #     'imgdata': data,
            #     'filepath': 'gander_goose/dev/test2'
            # }
            # result = requests.post(url='http://api.max-digital.cn/Api/oss/baseUpload', data=kw)
            # result = result.json()
            # oss_url = result.get('oss_file_url')
            oss_url = storage_by_url(url)
            if oss_url:
                return oss_url
        except Exception as e:
            Logging.logger.error('上传oss挂了:{0}'.format(e))
            return ''

    # 数据上传mongo
    def upload_mongo(self, article_dict, title):
        try:
            client = MongoClient('47.100.63.158', 27017)
            # my_db = client.will
            my_db = client.wechat
            articles = my_db.articles.find({'title': title})
            try:
                article = articles[0]
                Logging.logger.info('文章已存在MongoDB中,标题是:{0}'.format(title))
            except Exception as e:
                my_db.articles.insert_one(article_dict)
                Logging.logger.info('上传到mongo成功')
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))

    # 爬虫文章通过公众号插入到mysql
    @staticmethod
    def upload_mysql_by_webname(title, author, wechat_art_date, min_pic, summary, web_name, link, round_head_img, alias,
                                is_original):
        try:
            now1 = datetime.datetime.now()
            Logging.logger.info("获取到公众号:%s, 文章标题是:%s, 准备插入" % (web_name, title))
            data = list()
            conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                           database='zjlivenew',
                           user='maxpr_mysql', password='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
            # 获得Cursor对象 "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"
            cursor = conn.cursor()
            sql1 = "insert into zj_article_info (title,author,wechat_art_date,min_pic, summary, web_name, link, round_head_img, alias,is_show,is_big,create_time,is_original) " \
                   "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                       title, author, wechat_art_date, min_pic, summary, web_name, link, round_head_img, alias, 0, 0,
                       now1, is_original)
            cursor.execute(sql1)

            article_id = int(conn.insert_id())
            data.append(article_id)
            Logging.logger.info("公众号:%s, 文章:%s, 插入成功, 获得文章ID: %s" % (web_name, title, article_id))

            # 查询文章所属公众号是否有加入PC的公众号库
            sql2 = 'select id from zj_webname_info where wechat_name = "%s" and alias= "%s"' % (web_name, alias)
            num2 = cursor.execute(sql2)
            if num2 == 0:
                Logging.logger.info("公众号:%s,不在公众号库中,文章存入爆料库" % web_name)
            else:
                Logging.logger.info("公众号:%s,在公众号库中,检查对应文章类型关系" % web_name)
                # 获取文章所属公众号ID
                docs = cursor.fetchall()
                wechat_id = docs[0][0]

                # 公众号所对应的文章分类
                sql3 = 'select group_id from zj_webname_group where wechat_id = "%s"' % wechat_id
                num3 = cursor.execute(sql3)
                if num3 == 0:
                    Logging.logger.info("公众号:%s,未设置对应上线分类关系,文章存入爆料库" % web_name)
                else:
                    Logging.logger.info("公众号:%s,已设置对应上线分类关系,准备上线" % web_name)
                    groups = cursor.fetchall()
                    # print 'groups=', groups
                    now2 = datetime.datetime.now()
                    for group in groups:
                        group_id = group[0]
                        # # 先更改当前分类下所有文章的自定义排序数值
                        # sql4 = 'update zj_article_group set sort_num = sort_num + 1 where group_id="%s"' % group_id
                        # cursor.execute(sql4)

                        # 文章自动上线到所属公众号对应的文章分类,并显示在最前
                        sql5 = 'insert into zj_article_group (article_id, group_id, sort_num, create_time) values ("%s", "%s", "%s", "%s")' % (
                            article_id, group_id, 1, now2)
                        cursor.execute(sql5)

                    sql6 = 'update zj_article_info set is_show = 1, zj_art_date="%s" where id="%s"' % (now2, article_id)
                    cursor.execute(sql6)
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

    # 爬虫文章通过关键字插入到mysql
    @staticmethod
    def upload_mysql_by_keyword(title, author, wechat_art_date, min_pic, summary, web_name, link, round_head_img, alias,
                                is_original, group_id_list):

        now1 = datetime.datetime.now()
        Logging.logger.info("获取到公众号:%s, 文章标题是:%s, 准备插入" % (web_name, title))
        data = list()
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       database='zjlivenew',
                       user='maxpr_mysql', password='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # 获得Cursor对象 "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"
        cursor = conn.cursor()
        try:
            sql1 = "insert into zj_article_info (title,author,wechat_art_date,min_pic, summary, web_name, link, round_head_img, alias,is_show,is_big,create_time,is_original) " \
                   "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                       title, author, wechat_art_date, min_pic, summary, web_name, link, round_head_img, alias, 0,
                       0, now1, is_original)
            cursor.execute(sql1)

            article_id = int(conn.insert_id())
            redis_client = RedisClient.create_redis_cli()
            redis_client.rpush('article_id_list', article_id)
            data.append(article_id)
            Logging.logger.info("公众号:%s, 文章:%s, 插入成功, 获得文章ID: %s" % (web_name, title, article_id))

            if group_id_list and article_id > 0:
                group_id_list = set(group_id_list)
                now2 = datetime.datetime.now()
                for group_id in group_id_list:
                    if group_id:
                        # 文章自动上线到关键词对应的文章分类,并显示在最前
                        sql2 = 'insert into zj_article_group (article_id, group_id, sort_num, create_time) values ("%s", "%s", "%s", "%s")' % (
                            article_id, group_id, 1, now2)
                        cursor.execute(sql2)

                        sql3 = 'update zj_article_info set is_show = 1, zj_art_date="%s" where id="%s"' % (
                            now2, article_id)
                        cursor.execute(sql3)
                    break  # 3.11北京要求:文章筛选出现多个分类时,随便上架到一个分类即可
                Logging.logger.info("公众号:%s,文章标题:%s, 自动上线成功" % (web_name, title))
                data.append(666)
            conn.commit()
            return data
        except Exception as e:
            conn.rollback()
            Logging.logger.error('公众号:%s,文章标题:%s,自动上线失败:' % (web_name, title))
            Logging.logger.error('errmsg:{0}'.format(e))
            return False
        finally:
            cursor.close()
            conn.close()

    # def upload_mysql(self, title, author, wechat_art_date, min_pic, summary, web_name, link, round_head_img, alias):
    #     try:
    #         now = datetime.datetime.now()
    #         print "当前时间: ", now
    #         print "获取到公众号:%s, 文章标题是:%s, 准备插入并自动上线" % (web_name, title)
    #         article = Article()
    #         article.title = title
    #         article.author = author
    #         article.wechat_art_date = wechat_art_date
    #         article.min_pic = min_pic
    #         article.summary = summary
    #         article.web_name = web_name
    #         article.is_show = 0
    #         article.is_big = 0
    #         article.link = link
    #         article.round_head_img = round_head_img
    #         article.alias = alias
    #
    #         db.session.add(article)
    #         db.session.commit()
    #
    #         # 获取文章所属公众号ID
    #         wechat = WeChatName.query.filter(WeChatName.wechat_name == web_name, WeChatName.alias == alias).first()
    #         if not wechat:
    #             print "公众号:%s,不在公众号库中,文章存入爆料库" % web_name
    #             return True
    #         else:
    #             # 公众号所对应的文章分类
    #             groups = WeChatNameGroup.query.filter(WeChatNameGroup.wechat_id == wechat.id).all()
    #             if not groups:
    #                 print "公众号:%s,未设置对应上线分类关系,文章存入爆料库" % web_name
    #                 return True
    #             else:
    #                 for group in groups:
    #                     # 当前分类下的所有文章
    #                     articles = ArticleGroup.query.filter(ArticleGroup.group_id == group.group_id).all()
    #                     for article_obj in articles:
    #                         # 先更改文章的自定义排序数值
    #                         article_obj.sort_num += 1
    #                         db.session.add(article_obj)
    #
    #                     # 文章自动上线到所属公众号对应的文章分类
    #                     obj = ArticleGroup()
    #                     obj.article_id = article.id
    #                     obj.group_id = group.group_id
    #                     # 再给新上线的文章的自定义排序数值赋值,显示在最前
    #                     obj.sort_num = 1
    #                     db.session.add(obj)
    #
    #                 article.is_show = 1
    #                 article.zj_art_date = now
    #                 db.session.add(article)
    #
    #                 db.session.commit()
    #                 print "公众号:%s,文章标题:%s, 自动上线成功" % (web_name, title)
    #                 return True
    #     except Exception as e:
    #         print '公众号:%s,文章标题:%s,自动上线失败:'% (web_name, title)
    #         print e
    #         db.session.rollback()
    #         return False

    def get_title_list(self, title):
        # 查询mysql
        num = Article.query.filter(Article.title == title).count()
        # conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
        #                database='zjlivenew',
        #                user='maxpr_mysql', password='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        # # 获得Cursor对象
        # cs1 = conn.cursor()
        #
        # res = 'select * from zj_article_info where web_name = "%s" and title= "%s"' % (query, title)
        # num = cs1.execute(res)
        return num
