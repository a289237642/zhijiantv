# -*- coding:utf-8 -*-
# author: will
from utils.log_service import Logging
from utils.redis_service.Redis_Client import RedisClient


class ArticleFilter(object):
    def __init__(self, title, content):
        self.redis_client = RedisClient.create_redis_cli()
        self.first_keywords = self.redis_client.get('first_keywords').split(',')
        self.second_keywords = self.redis_client.get('second_keywords').split(',')
        self.title = title
        self.content = content
        self.group_id_list = list()

    # 一级关键词在内容中的频次
    def article_content_filter(self):
        first_keyword_dict = dict()
        second_keyword_dict = dict()

        # 内容查找
        if isinstance(self.content, list):
            text = ''.join([item.get('text') for item in self.content if item.get('text')])
            # 查询文章内容含有的频次最高的一级关键词
            for first_keyword in self.first_keywords:
                num = 0
                num += text.count(first_keyword)
                if num > 0:
                    first_keyword_dict[first_keyword] = num
            first_res = self.select_high(first_keyword_dict)
            if len(first_res) == 1:
                keyword, num = first_res[0][0], first_res[0][1]
                Logging.logger.info('内容中频次最高的一级关键词和词频是:%s,%s' % (keyword, num))
                keyword = {'first_keywords': keyword}
            else:
                # 频次最高的一级关键词没有或者有多个,采用二级属性词分类标准
                for second_keyword in self.second_keywords:
                    num = 0
                    num += text.count(second_keyword)
                    if num > 0:
                        second_keyword_dict[second_keyword] = num
                second_res = self.select_high(second_keyword_dict)
                if len(second_res) == 1:
                    keyword, num = second_res[0][0], second_res[0][1]
                    keyword = {'second_keywords': keyword}
                    Logging.logger.info('内容中频次最高的二级属性词和词频是:%s,%s' % (keyword, num))
                elif len(second_res) > 1:
                    # 频次最高的二级属性词有多个,文章分别上架到二级属性词对应的文章分类
                    keyword = [x[0] for x in second_res]
                    keyword = {'second_keywords': keyword}
                    Logging.logger.info('内容中频次最高的多个二级属性词分别是:%s' % keyword)
                else:
                    # 没有匹配到二级属性词,但频次最高的一级关键词有多个,文章分别上架到一级关键词对应的文章分类
                    if len(first_res) > 1:
                        keyword = [x[0] for x in first_res]
                        Logging.logger.info('内容中频次最高的多个一级关键词分别是:%s' % keyword)
                        keyword = {'first_keywords': keyword}
                    else:
                        return False
            return keyword
        return False

    # 标题查找
    def article_title_filter(self):
        first_keyword_dict = dict()

        for first_keyword in self.first_keywords:
            num = 0
            num += self.title.count(first_keyword)
            if num > 0:
                first_keyword_dict[first_keyword] = num
        first_res = self.select_high(first_keyword_dict)
        if len(first_res) == 1:
            keyword, num = first_res[0][0], first_res[0][1]
            first_keywords = {'first_keywords': keyword}
            Logging.logger.info('标题中频次最高的一级关键词和词频是:%s,%s' % (keyword, num))
            return first_keywords
        return False

    # 关键词查找--主函数,返回文章关键词对应的分类ID
    def article_filter(self):
        # 1.标题查找
        title_keyword = self.article_title_filter()
        if title_keyword:
            first_keywords = title_keyword.get('first_keywords')
            group_id = self.get_keyword_group_id(first_keywords)
            self.group_id_list.append(group_id)
            Logging.logger.info('标题中频次最高的一级关键词只有一个:{0},文章上架到对应分类ID:{1}'.format(first_keywords, group_id))
        else:
            # 2.内容查找
            content_keyword = self.article_content_filter()
            if content_keyword:
                first_keywords = content_keyword.get('first_keywords')
                if isinstance(first_keywords, str):
                    group_id = self.get_keyword_group_id(first_keywords)
                    Logging.logger.info('内容中频次最高的一级关键词只有一个:{0},文章上架到对应分类ID:{1}'.format(first_keywords, group_id))
                    self.group_id_list.append(group_id)

                elif isinstance(first_keywords, list):
                    Logging.logger.info('无频次最高的二级属性词,频次最高的一级关键词有多个:{0},文章分别上架到对应分类'.format(first_keywords))
                    for first_keyword in first_keywords:
                        group_id = self.get_keyword_group_id(first_keyword)
                        self.group_id_list.append(group_id)

                else:
                    second_keywords = content_keyword.get('second_keywords')
                    if isinstance(second_keywords, str):
                        group_id = self.get_keyword_group_id(second_keywords)
                        Logging.logger.info('频次最高的二级属性词只有一个:{0},文章上架到对应分类ID:{1}'.format(second_keywords, group_id))
                        self.group_id_list.append(group_id)

                    elif isinstance(second_keywords, list):
                        Logging.logger.info('频次最高的二级属性词有多个:{0},文章分别上架到对应分类'.format(second_keywords))
                        for second_keyword in second_keywords:
                            group_id = self.get_keyword_group_id(second_keyword)
                            self.group_id_list.append(group_id)
                    else:
                        self.group_id_list = None
                        Logging.logger.info('无匹配关键词,存入爆料库')
            else:
                self.group_id_list = None
                Logging.logger.info('无匹配关键词,存入爆料库')

        return self.group_id_list

    # 选取出现频次最高的关键字
    @staticmethod
    def select_high(keyword_dict):
        ls = sorted(list(keyword_dict.items()), key=lambda a: a[1], reverse=True)
        index = 0
        for i, x in enumerate(ls):
            if x[1] == ls[0][1]:
                index = i + 1
            else:
                break
        print((ls[:index]))
        return ls[:index]

    # Redis取出关键词对应的文章分类ID
    def get_keyword_group_id(self, keyword):
        article_group_id = self.redis_client.hget('group_id_of_keyword', keyword)
        return article_group_id

    # 文章敏感词过滤
    def sensitive_words_filter(self):
        try:
            sensitive_words = self.redis_client.get('sensitive_words')
            if sensitive_words:
                sensitive_words = sensitive_words.split(',')
                text = ''.join([item.get('text') for item in self.content if item.get('text')])
                for sensitive_word in sensitive_words:
                    resp_title = self.title.find(sensitive_word)
                    resp_content = text.find(sensitive_word)
                    if resp_title != -1 or resp_content != -1:
                        return True
                    else:
                        return False
            else:
                return False
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return False

