#-*- coding utf-8 -*-
# @Time : 2020/6/1 14:27
# !/usr/bin/env python
# coding: utf-8


from gensim import corpora, models, similarities
from recommend_test.algorithm.Utils import tokenization_for_search, get_train_file_name, create_stop_word, _tokenization
import pickle


def load_tfidf_model():
    with open('D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_tfidf_vectors', 'rb') as f:
        tfidf_vectors = pickle.load(f)
    dictionary = corpora.Dictionary.load(
        "D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_tfidf_dictionary")

    return tfidf_vectors, dictionary


def get_tfidf_recommend_policy(fileList, text_content, top_n=5):
    tfidf_vectors, dictionary = load_tfidf_model()
    query_bow = dictionary.doc2bow(text_content)
    index = similarities.MatrixSimilarity(tfidf_vectors)
    simtf = index[query_bow]
    # 相似度排序
    scores = sorted(enumerate(simtf), key=lambda item: -item[1])  # 排序
    # 输出分值
    dict_re = {"article": [], "score": []}
    _top_n = top_n
    if len(fileList) < top_n:
        _top_n = len(fileList)
    for index in scores[:_top_n]:
        dict_re['article'].append(fileList[index[0]])
        dict_re['score'].append(index[1])
    return dict_re

# if __name__ == "__main__":
#     stopwords,stop_flag=create_stop_word('D:/workspace/PycharmWorkspace/recommend_test/data_polies/stop_words.txt')
#     query=tokenization_for_search("光伏发电",stopwords,stop_flag)
#     fileList = []
#     get_train_file_name("D:/workspace/jupyterWorkspace/政策推荐/policy_data/train/", fileList)
#     re=get_tfidf_recommend_policy(fileList,query,200)
#     print(re)

