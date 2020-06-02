#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8


from gensim import corpora, models, similarities
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
import gensim
from recommend_test.algorithm.Utils import get_train_file_name,create_stop_word,_tokenization,tokenization_for_search


def get_train_data(corpus):
    TaggededDocument_1 = gensim.models.doc2vec.TaggedDocument
    x_train=[]
    for i, text in enumerate(corpus):
        document = TaggededDocument_1(text, tags=[i])
        x_train.append(document)
    return x_train
 
def train(x_train, size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train,min_count=1, window = 3, size = size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
    model_dm.save('D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_dm_wangyi')
 
    return model_dm



def doc2vec_train_job():   

    fileList=[]
    get_train_file_name("./policy_data/train/",fileList)
    #构建停用词
    stopwords,stop_flag=create_stop_word('./data/stop_words.txt')
    #读取文章并去除停用词
    #outpu [[word1,word2...],[word1,word2...]..]
    corpus = []
    for filename in fileList:
        fileName=filename
        corpus.append(_tokenization(fileName,stopwords,stop_flag))
    x_train=get_train_data(corpus)
    train(x_train)

