# -*- coding:utf-8 -*-
# author: will
import datetime
import json
import os

import jieba
import redis

from gensim import models, corpora, similarities
from collections import defaultdict

from pymongo import MongoClient

from pymysql import connect


class ArticleModel(object):
    def __init__(self):
        # self.redis_client = redis.StrictRedis(host='101.132.186.25', port='6379', db=9)
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port='6379', db=9)
        self.mongo_client = MongoClient('47.100.63.158', 27017)
        # 本地
        # self.docs_file_path = '/Users/will/Desktop/workspace/zhijian_live/python/utils/article_service/documents.txt'
        # self.dict_file_path = '/Users/will/Desktop/workspace/zhijian_live/python/utils/article_service/dictionary.txt'
        # 正式
        self.docs_file_path = '/www/zjlive/zhijian_live_miniprogram/python/utils/article_service/documents.txt'
        self.dict_file_path = '/www/zjlive/zhijian_live_miniprogram//python/utils/article_service/dictionary.txt'

    @staticmethod
    def get_article_id():
        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zjlivenew',
                       user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        cursor = conn.cursor()
        sql = 'select id from zj_article_info'
        cursor.execute(sql)
        docs = cursor.fetchall()
        article_id_ls = [doc[0] for doc in docs]
        cursor.close()
        conn.close()
        return article_id_ls

    # 1.对文档进行分词
    def content_to_cut(self, article_id):

        conn = connect(host='rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com', port=3306,
                       db='zjlivenew',
                       user='maxpr_mysql', passwd='COFdjwD*$*m8bd!HtMLP4+Az0eE9m', charset='utf8')
        cursor = conn.cursor()
        sql = 'select title from zj_article_info where id=%s' % article_id
        cursor.execute(sql)
        title = cursor.fetchall()[0][0]
        cursor.close()
        conn.close()

        # mongo_store = self.mongo_client.will
        mongo_store = self.mongo_client.wechat
        # docs1 = mongo_store.articles.find({'article_id': article_id})
        docs1 = mongo_store.articles.find({'title': title})
        try:
            doc1 = docs1[0]
            content1 = doc1.get('content')
            text1 = ''.join([item.get('text') for item in content1 if item.get('text')])
            data1 = jieba.cut(text1)
            data11 = ''.join([item + ' ' for item in data1])
            return data11
        except Exception as e:
            print (e)
            obj.redis_client.rpush('wrong_article_id', article_id)
            return False

    # 1.对文档进行分词
    @staticmethod
    def content_to_cut_by_data(content):
        text = ''.join([item.get('text') for item in content if item.get('text')])

        data = jieba.cut(text)

        data = ''.join([item + ' ' for item in data])
        return data

    # 2.计算词频
    @staticmethod
    def get_words_num(docs):
        texts = [[word for word in document.split()] for document in docs]
        # 3.计算词语的频率，对词语整理
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        return texts

    # 4.通过语料库建立词典
    def build_dictionary(self, texts):
        dictionary = corpora.Dictionary(texts)
        # 去除极低频的杂质词
        dictionary.filter_extremes(no_below=1, no_above=1, keep_n=None)
        dictionary.save(self.dict_file_path)
        return dictionary

    # 6.对比的文档,得到相似度
    @staticmethod
    def get_sim(data, texts, dictionary):
        # 6.将要对比的文档通过doc2bow转化为稀疏向量/词袋模型
        new_vec = dictionary.doc2bow(data.split())

        # 7.对稀疏向量/词袋模型进一步处理，得到新语料库
        corpus = [dictionary.doc2bow(text) for text in texts]

        # 8.通过tf-idf model模型处理新语料库，得到tfidf值
        tfidf = models.TfidfModel(corpus)

        # 9.通过token2id得到特征数（字典里面的键的个数）
        feature_Num = len(list(dictionary.token2id.keys()))

        # 10.计算稀疏矩阵相似度，建立一个索引
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_Num)  # 稀疏矩阵相似度

        # 11.根据索引得到最终的相似度
        sim = index[tfidf[new_vec]]  # 通过tfidf和要对比的文本的稀疏向量计算相似度
        sims = sorted(enumerate(sim), key=lambda item: -item[1])  # 排序

        return sims

    def run(self, content):
        with open(self.docs_file_path, 'r') as f:
            documents = f.read()
        documents = json.loads(documents)
        texts = self.get_words_num(documents)

        # 加载语料库
        dictionary = corpora.Dictionary()
        dic = dictionary.load(self.dict_file_path)

        data = self.content_to_cut_by_data(content)

        sims = self.get_sim(data, texts, dic)

        sim_ls = [i for i in sims if i[1] > 0.6]
        if not sim_ls:
            # os.remove(self.dict_file_path)
            # data = [[word for word in data.split()]]
            # dic.add_documents(data)
            # dic.save(self.dict_file_path)

            documents.append(data)
            # os.remove(self.dict_file_path)
            res = self.get_words_num(documents)
            self.build_dictionary(res)

            # os.remove(self.docs_file_path)
            dct = json.dumps(documents)
            with open(self.docs_file_path, 'w') as f:
                f.write(dct)
        return sim_ls

    # 数据初始化
    def data_init(self):
        try:
            self.redis_client.delete('article_id_list')
            article_id_list = self.get_article_id()
            documents_ls = []
            for article_id in article_id_list:
                print (article_id)
                document = self.content_to_cut(article_id)
                if document:
                    documents_ls.append(document)
                    self.redis_client.rpush('article_id_list', article_id)
            docs = json.dumps(documents_ls)
            with open(self.docs_file_path, 'w') as f:
                f.write(docs)

            # with open(obj.docs_file_path, 'r') as f:
            #     documents = f.read()
            # print 1111
            # documents_ls = json.loads(documents)
            words = self.get_words_num(documents_ls)
            self.build_dictionary(words)
            return True
        except Exception as e:
            print (e)
            return False


if __name__ == '__main__':

    # 数据初始化
    print(('开始时间:', datetime.datetime.now()))
    obj = ArticleModel()
    obj.data_init()
    print(('结束时间:', datetime.datetime.now()))
