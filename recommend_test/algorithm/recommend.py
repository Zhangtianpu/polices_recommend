#!/usr/bin/env python
# coding: utf-8


from recommend_test.algorithm.Utils import get_train_file_name,create_stop_word,_tokenization,tokenization_for_search
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import numpy as np
from recommend_test.algorithm.doc2vec import get_recommend_policy
from recommend_test.algorithm.base_tfidf import get_tfidf_recommend_policy

def get_removal_duplicate(doc2vec_recommend_re,tfidf_recommend_re):
    doc2vec_recommend_re['policy'].extend(tfidf_recommend_re['article'])
    doc2vec_recommend_re['sim'].extend(tfidf_recommend_re['score'])
    helper_set=set()
    re_dict={'policy':[],'sim':[]}
    for index,policy in enumerate(doc2vec_recommend_re['policy']):
        if policy not in helper_set:
            re_dict['policy'].append(policy)
            re_dict['sim'].append(float(doc2vec_recommend_re['sim'][index]))
            helper_set.add(policy)
    return re_dict

def get_policy_feature(policyList):
    return np.ones((len(policyList),5),dtype=float)

def get_click_proba_dict(click_proba):
    click_proba_dict={}
    for i, text in enumerate(click_proba):
        click_proba_dict[i]=text
    return click_proba_dict

def get_sorted_recommend_policy(result_policy,click_proba_dict_sorted):
    result_sorted_recommend_dict={'policy':[],'score':[]}
    for index,score in click_proba_dict_sorted:
        policy=result_policy['policy'][index]
        score=result_policy['sim'][index]
        result_sorted_recommend_dict['policy'].append(policy)
        result_sorted_recommend_dict['score'].append(score)
    return result_sorted_recommend_dict



def get_result(search_content):
    fileList=[]
    get_train_file_name("D:\workspace\jupyterWorkspace\政策推荐\policy_data", fileList)
    stopwords, stop_flag = create_stop_word('D:/workspace/PycharmWorkspace/recommend_test/data_polies/stop_words.txt')
    test_text = tokenization_for_search(search_content, stopwords, stop_flag)
    #Doc2vec的推荐结果
    doc2vec_recommend_re=get_recommend_policy(fileList, test_text)
    #print(type(doc2vec_recommend_re['sim'][0]))
    #tfidf的推荐结果
    tfidf_recommend_re = get_tfidf_recommend_policy(fileList, test_text)
    #print(type(tfidf_recommend_re['score'][0]))
    #得到doc2vec和tfidf去重后的结果
    result_policy=get_removal_duplicate(doc2vec_recommend_re,tfidf_recommend_re)
    policyList = result_policy['policy']
    X=get_policy_feature(policyList)
    log_reg=joblib.load("D:/workspace/PycharmWorkspace/recommend_test/algorithm/model/log_reg.pkl")
    click_proba=log_reg.predict_proba(X)[:,1]
    click_proba_dict=get_click_proba_dict(click_proba)
    click_proba_dict_sorted=sorted(click_proba_dict.items(),key=lambda x:x[1],reverse=True)
    result_sorted_recommend_dict=get_sorted_recommend_policy(result_policy,click_proba_dict_sorted)
    return result_sorted_recommend_dict

# if __name__ == '__main__':
#     re=get_result("光伏发电")
#     print(re['policy'])
#     print(re['score'])