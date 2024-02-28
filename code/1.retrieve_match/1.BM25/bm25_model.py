#!/usr/bin/env python
import math
import numpy as np


class BM25:
    def __init__(self, corpus, tokenizer=None):
        self.corpus_size = len(corpus)  # N 117
        self.avgdl = 0  # 平均长度
        self.doc_freqs = []  # 存储每个词及出现了该词的文档数量
        self.idf = {}  # 存储每个词的idf值 即权重
        self.doc_len = []  # 每个的文档长度
        self.tokenizer = tokenizer

        if tokenizer:
            corpus = self._tokenize_corpus(corpus)

        nd = self._initialize(corpus)  # 包含该词的文档数
        self._calc_idf(nd)  # 计算该词的权重 idf

    def _initialize(self, corpus):  # 算nd和self.avgdl
        nd = {}  # word -> number of documents with word 包含该词的文档数
        num_doc = 0  # 词的总数
        for document in corpus:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}  # 词频
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                if word not in nd:
                    nd[word] = 0
                nd[word] += 1

        self.avgdl = num_doc / self.corpus_size  # 文档平均长度
        return nd

    def _tokenize_corpus(self, corpus):
        tokenized_corpus = [self.tokenizer(doc) for doc in corpus]
        return tokenized_corpus

    def _calc_idf(self, nd):
        raise NotImplementedError()  # 子类没有实现父类要求一定要实现的接口。

    def get_scores(self, query):
        raise NotImplementedError()

    # def get_top_n(self, query, documents, n=10):
    #
    #     assert self.corpus_size == len(documents), "The documents given don't match the index corpus!"
    #     query = self.tokenizer(str(query)) # 清洗 分词
    #     if not query:
    #         return []
    #
    #     scores = self.get_scores(query)
    #     top_n = np.argsort(scores)[::-1][:n]
    #     return [documents[i] for i in top_n]
    def get_top_n(self, query, qa_df, n=5, calc_recall=False):
        if not calc_recall:
            assert self.corpus_size == len(qa_df), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [{"question": qa_df[i]['question'], "answer": qa_df[i]['answer']} for i in top_n]



class BM25kapi(BM25):
    def __init__(self, corpus, tokenizer=None, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__(corpus, tokenizer)

    def _calc_idf(self, nd):

        idf_sum = 0
        negative_idfs = []

        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)

        self.average_idf = idf_sum / len(self.idf)  # 算平均权重

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_scores(self, query):

        score = np.zeros(self.corpus_size)  # 对应总文档每个的分数
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])  # q在总文档中出现的文档次数
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score
