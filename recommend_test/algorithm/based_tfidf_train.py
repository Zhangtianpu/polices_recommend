#!/usr/bin/env python
# coding: utf-8

# In[5]:


import jieba.posseg as pseg
import codecs
#import synonyms
#import docx
from gensim import corpora, models, similarities
from recommend_test.algorithm.Utils import create_stop_word,_tokenization,get_train_file_name,tokenization_for_search
import pickle

#2构建停用词表 './data_polies/stop_words.txt'
# def create_stop_word(stop_word_file_name):
#     stop_words =stop_word_file_name
#     stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
#     stopwords = [ w.strip() for w in stopwords ]
#     #3shez结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
#     stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
#     return stopwords,stop_flag



#对一篇文章分词、去停用词
# def tokenization(filename,stopwords,stop_flag):
#     result = []#d1 = open(filenames[1],encoding="utf-8").read()
#     with open(filename,encoding="utf-8") as f:
#         text = f.read()
#         words = pseg.cut(text)
#     for word, flag in words:
#         if flag not in stop_flag and word not in stopwords:
#             result.append(word)
#     return result


# def tokenization_for_search(keywords,stopwords,stop_flag):
#     result=[]
#     words = pseg.cut(keywords)
#     for word, flag in words:
#         if flag not in stop_flag and word not in stopwords:
#             result.append(word)
#     return result


def train_tfidf():
    #构建停用词
    stopwords,stop_flag=create_stop_word('D:/workspace/PycharmWorkspace/recommend_test/data_polies/stop_words.txt')
    #读取文章并去除停用词
    fileList = []
    get_train_file_name("D:/workspace/jupyterWorkspace/政策推荐/policy_data/train/", fileList)
    corpus = []
    for filename in fileList:
        fileName = filename
        corpus.append(_tokenization(fileName, stopwords, stop_flag))
    #[(word,id)]
    dictionary = corpora.Dictionary(corpus)
    dictionary.save("D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_tfidf_dictionary")
    #[(wordid,frequency)]
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    tfidf = models.TfidfModel(doc_vectors)
    tfidf.save('D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_tfidf')
    tfidf_vectors = tfidf[doc_vectors]
    print(tfidf_vectors)
    print(type(tfidf_vectors))
    #tfidf_vectors
    with open('D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_tfidf_vectors', 'wb') as f:
        pickle.dump(tfidf_vectors, f)  ##把列表永久保存到文件中
#
# if __name__ == "__main__":
#     train_tfidf()



