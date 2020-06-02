#!/usr/bin/env python
# coding: utf-8

# In[3]:


import jieba.posseg as pseg
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
import gensim
import os
import numpy as np


from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator




def get_train_file_name(path,fileList):
    fileNames=os.listdir(path)
    for fileName in fileNames:
        newFileName=os.path.join(path,fileName)
        if os.path.isdir(newFileName):
            get_train_file_name(newFileName,fileList)
        else:
            if fileName=='.DS_Store':
                continue
            fileList.append(newFileName)


def tokenization_for_search(keywords,stopwords,stop_flag):
    result=[]
    words = pseg.cut(keywords)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result


# In[11]:





# In[12]:


def getVecs(model, corpus, size):
   vecs = [np.array(model.docvecs[z.tags[0]].reshape(1, size)) for z in corpus]
   return np.concatenate(vecs)

def train(x_train, size=200, epoch_num=1):
   model_dm = Doc2Vec(x_train,min_count=1, window = 3, size = size, sample=1e-3, negative=5, workers=4)
   model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
   model_dm.save('./model/model_dm_wangyi')

   return model_dm

def test(test_text,topn=5):
   model_dm = Doc2Vec.load("D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/model_dm_wangyi")
   inferred_vector_dm = model_dm.infer_vector(test_text)
   #print (inferred_vector_dm)
   sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=topn)
   return sims


# In[13]:


def get_recommend_policy(fileList,search_content_by_cut):

    sims = test(search_content_by_cut, 5)

    recommend_dict={"policy":[],"sim":[]}
    for count,sim in sims:
        recommend_dict["policy"].append(fileList[count])
        recommend_dict["sim"].append(sim)
    return recommend_dict
