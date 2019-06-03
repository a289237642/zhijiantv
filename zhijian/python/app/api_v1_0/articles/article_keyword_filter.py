# -*- coding:utf-8 -*-
# author: will
import json

from aip import AipSpeech, AipImageCensor
from flask import request, jsonify

from app import mongo_store, db, redis_store
from app.api_v1_0.articles import api_article
from app.models import Article, ArticleKeyWords, Group, ArticleSensitiveWords
from config.lib_config import LibConfig
from utils.article_service.keywords_filter import ArticleFilter
from utils.article_service.sensitive_words_filter import SensitiveFilter
from utils.log_service import Logging
from utils.redis_service.Redis_Client import RedisClient
from utils.user_service.login import login_required, admin_required


# PC文章关键词添加
@api_article.route('/article_keyword_add', methods=['POST'])
@login_required
@admin_required
def article_keyword_add():
    try:
        res = request.get_json()
        article_group_id = res.get('article_group_id')
        first_keywords = res.get('first_keywords').replace(' ', '')
        second_keywords = res.get('second_keywords').replace(' ', '')

        Logging.logger.info('request_args:{0}'.format(res))

        if not all([article_group_id, first_keywords, second_keywords]):
            return jsonify(errno=-1, errmsg='参数不完整')

        article_group = Group.query.get(article_group_id)
        if not article_group:
            return jsonify(errno=-1, errmsg='参数错误,文章类别不存在')

        if first_keywords.count('，'):
            first_keywords = first_keywords.replace('，', ',')

        if first_keywords[len(first_keywords) - 1] == ',':
            first_keywords = first_keywords[:len(first_keywords) - 1]

        if second_keywords.count('，'):
            second_keywords = second_keywords.replace('，', ',')

        if second_keywords[len(second_keywords) - 1] == ',':
            second_keywords = second_keywords[:len(second_keywords) - 1]

        article_keyword = ArticleKeyWords.query.filter_by(article_group_id=article_group_id).first()
        if not article_keyword:
            obj = ArticleKeyWords()
            obj.article_group_id = article_group_id
            obj.first_keywords = first_keywords
            obj.second_keywords = second_keywords
            db.session.add(obj)

        else:
            article_keyword.first_keywords += (',' + first_keywords)
            article_keyword.second_keywords += (',' + second_keywords)
            db.session.add(article_keyword)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC文章关键词修改
@api_article.route('/article_keyword_update', methods=['POST'])
@login_required
@admin_required
def article_keyword_update():
    try:
        res = request.get_json()
        keyword_id = res.get('keyword_id')
        first_keywords = res.get('first_keywords').replace(' ', '')
        second_keywords = res.get('second_keywords').replace(' ', '')
        article_group_id = res.get('article_group_id')

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([article_group_id, first_keywords, second_keywords]):
            return jsonify(errno=-1, errmsg='参数不完整')

        first_obj = ArticleKeyWords.query.get(keyword_id)
        if not first_obj:
            return jsonify(errno=-1, errmsg='参数错误,关键词ID不存在')

        if first_keywords.count('，'):
            first_keywords = first_keywords.replace('，', ',')

        if first_keywords[len(first_keywords) - 1] == ',':
            first_keywords = first_keywords[:len(first_keywords) - 1]

        if second_keywords.count('，'):
            second_keywords = second_keywords.replace('，', ',')

        if second_keywords[len(second_keywords) - 1] == ',':
            second_keywords = second_keywords[:len(second_keywords) - 1]

        first_obj.article_group_id = article_group_id
        first_obj.first_keywords = first_keywords
        first_obj.second_keywords = second_keywords
        db.session.add(first_obj)
        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC文章关键词管理列表
@api_article.route('/article_keyword_list', methods=['POST'])
@login_required
@admin_required
def article_keyword_list():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        results = ArticleKeyWords.query.paginate(page, pagesize, False)
        count = results.total
        keyword_list = list()
        redis_client = RedisClient.create_redis_cli()
        redis_client.delete('group_id_of_keyword')

        first_ls = list()
        second_ls = list()
        i = (page - 1) * pagesize + 1
        for result in results.items:
            keyword_dict = dict()
            first_keyword = result.first_keywords
            second_keyword = result.second_keywords
            keyword_dict['keyword_id'] = result.id
            keyword_dict['article_group_id'] = result.article_group_id
            group = Group.query.get(result.article_group_id)
            keyword_dict['article_group_name'] = group.name
            keyword_dict['first_keywords'] = first_keyword
            keyword_dict['second_keywords'] = second_keyword
            keyword_dict['location'] = i
            keyword_list.append(keyword_dict)
            i += 1

            # 关键词对应分类ID存Redis
            for first_word in first_keyword.split(','):
                redis_client.hset('group_id_of_keyword', first_word, result.article_group_id)

            for second_word in second_keyword.split(','):
                redis_client.hset('group_id_of_keyword', second_word, result.article_group_id)

            first_ls.append(first_keyword)
            second_ls.append(second_keyword)

        # 关键词数据存入Redis
        first_keywords = ','.join(first_ls)
        second_keywords = ','.join(second_ls)
        redis_client.set('first_keywords', first_keywords)
        redis_client.set('second_keywords', second_keywords)

        return jsonify(errno=0, errmsg="OK", data=keyword_list, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# 文章关键词删除
@api_article.route('/del_article_keyword', methods=['POST'])
@login_required
@admin_required
def del_article_keyword():
    try:
        res = request.get_json()
        keywords_id_list = res.get('keywords_id_list')

        Logging.logger.info('request_args:{0}'.format(res))
        if not isinstance(keywords_id_list, list):
            return jsonify(errno=-1, errmsg='参数错误')

        redis_client = RedisClient.create_redis_cli()
        for keyword_id in keywords_id_list:
            if not keyword_id:
                return jsonify(errno=-1, errmsg="参数错误,请传入删除文章关键词ID")

            obj = ArticleKeyWords.query.get(keyword_id)
            if not obj:
                return jsonify(errno=-1, errmsg="参数错误,文章关键词ID不存在")

            first_keywords = obj.first_keywords
            second_keywords = obj.second_keywords
            for first_word in first_keywords.split(','):
                redis_client.hdel('group_id_of_keyword', first_word)

            for second_word in second_keywords.split(','):
                redis_client.hdel('group_id_of_keyword', second_word)

            db.session.delete(obj)
            db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC敏感词添加/修改
@api_article.route('/sensitive_words_update', methods=['POST'])
@login_required
@admin_required
def sensitive_words_update():
    try:
        res = request.get_json()
        sensitive_words = res.get('sensitive_words').replace(' ', '')
        sensitive_id = res.get('sensitive_id')
        style = res.get('style')  # 1,新增追加 2,修改

        Logging.logger.info('request_args:{0}'.format(res))

        if not sensitive_words:
            return jsonify(errno=-1, errmsg='参数不完整')

        if sensitive_words.count('，'):
            sensitive_words = sensitive_words.replace('，', ',')

        if sensitive_words[len(sensitive_words) - 1] == ',':
            sensitive_words = sensitive_words[:len(sensitive_words) - 1]

        if not sensitive_id:
            # 新增
            obj = ArticleSensitiveWords()
            obj.sensitive_words = sensitive_words
        else:
            # 修改
            obj = ArticleSensitiveWords.query.get(sensitive_id)
            if not obj:
                return jsonify(errno=-1, errmsg='参数错误')
            else:
                if style == 1:
                    obj.sensitive_words += (',' + sensitive_words)
                elif style == 2:
                    obj.sensitive_words = sensitive_words

        db.session.add(obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC敏感词列表
@api_article.route('/sensitive_words_ls')
@login_required
@admin_required
def sensitive_words_ls():
    try:
        result = ArticleSensitiveWords.query.first()
        redis_client = RedisClient.create_redis_cli()

        keyword_dict = dict()
        if result:
            sensitive_words = result.sensitive_words
            keyword_dict['sensitive_id'] = result.id
            keyword_dict['sensitive_words'] = sensitive_words

            # 敏感词数据存入Redis
            redis_client.set('sensitive_words', sensitive_words)

        return jsonify(errno=0, errmsg="OK", data=keyword_dict)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC敏感词删除
@api_article.route('/del_sensitive_words', methods=['POST'])
@login_required
@admin_required
def del_sensitive_words():
    try:
        res = request.get_json()
        sensitive_id = res.get('sensitive_id')

        Logging.logger.info('request_args:{0}'.format(res))

        obj = ArticleSensitiveWords.query.get(sensitive_id)
        if not obj:
            return jsonify(errno=-1, errmsg='参数错误')

        redis_client = RedisClient.create_redis_cli()
        redis_client.delete('sensitive_words')

        db.session.delete(obj)
        db.session.commit()

        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='网络异常')


# PC文章关键词分类上线--测试接口
@api_article.route('/test_article_filter', methods=['POST'])
def test_article_filter():
    try:
        res = request.get_json()
        article_id = res.get('article_id')
        article_images = res.get('article_images')

        Logging.logger.info('request_args:{0}'.format(res))
        if not article_id:
            return jsonify(errno=-1, errmsg='参数错误,请传入要查询的文章的article_id')

        article = Article.query.get(article_id)
        if not article:
            return jsonify(errno=-1, errmsg='参数错误,该文章不存在')

        docs = mongo_store.articles.find({'title': article.title})
        doc = docs[0]
        article_dict = dict()
        content = doc.get('content')
        title = article.title.encode("utf-8")
        article_dict['title'] = title
        article_dict['content'] = content

        obj = SensitiveFilter()
        str11 = ''.join([item.get('text') for item in content if item.get('text')])
        text = {'content': str11}
        txt_data = obj.content_check(text)
        if txt_data.get('errcode') == 40001:
            redis_store.delete('access_token')
            txt_data = obj.content_check(text)
        Logging.logger.info('res_data:{0}'.format(txt_data))

        APP_ID = '15791531'
        API_KEY = 'kajyVlP73XtSGBgoXDIHH5Za'
        SECRET_KEY = 'u2TClEW6LaHIIpRNdFcL2HIexcgG1ovC'

        client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)
        txt_resp = client.antiSpam(str11)
        Logging.logger.info('txt_resp:{0}'.format(txt_resp))

        for img in article_images:
            img_resp = client.imageCensorUserDefined(img)
            print(img_resp)
            Logging.logger.info('img_resp:{0}'.format(img_resp))
            # img_data = obj.img_check(img)
            # print img_data
        return jsonify(errno=0, errmsg="OK", data=txt_data)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='文章详情查询失败')
