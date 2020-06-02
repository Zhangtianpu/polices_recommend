#!/usr/bin/env python
# coding: utf-8


from recommend_test.algorithm.Doc2vec_train import doc2vec_train_job



doc2vec_train_job()

from apscheduler.schedulers.blocking import BlockingScheduler

import datetime
import shutil
def movefile(source, dest):    
    shutil.move(source, dest)
# 输出时间
def job():
    print(datetime.now().strtime("%Y-%m-%d %H:%M:%S"))




# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(doc2vec_train_job,"cron", day_of_week="1-5", hour=10,minute=20)
scheduler.start()

