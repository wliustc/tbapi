#coding:utf-8
"""
@file:      KickTaskManager
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2016/11/22 23:37
@description:
            --
"""

import os,sys
sys.path.append(
    os.path.dirname(
        sys.path[0]
    )
)

from generate_daren_static_data import DarenStaticDataGenerator

import random,time
import pymysql
def get_conn():
    conn = pymysql.connect(
        db = 'spiderpython',
        user = 'root',
        password = 'xingguang@123',
        host = '123.57.213.217',
        port = 3306
    )
    conn.autocommit=True
    return conn


def get_unfinished_range():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'select `left`,`right`,`id` from task_flag where is_crawled=0'
    )
    data = cur.fetchall()
    return data

def mark_ok(id,success_cot):
    conn = get_conn()
    cur = conn.cursor()
    sql = 'update task_flag set `is_crawled`=1 , `success_cot`={} \
                WHERE `id`={}'.format(success_cot,id)
    print(sql)
    cur.execute(sql)
    print('update {} ok'.format(id))
    conn.commit()
    cur.close()
    conn.close()


def run():
    while(1):
        range = random.choice(get_unfinished_range())
        print(range)
        left = range[0]
        right = range[1]
        id = range[2]
        #mark_ok(id,2)
        try:
            spider = DarenStaticDataGenerator(left,right)
            success_cot = spider.run(
                mysql=True,
                thread_cot=64,
                use_proc_pool=False,
                use_email=True,
                dynamic_range_length=right-left,
                err_print=True,
                visit_shuffle=False,
                save_db_type=0,
                debug=True,
                save_by_django=False
            )

            #print(success_cot)
            #time.sleep(3)
            mark_ok(id,success_cot)
            #time.sleep(3)

        except Exception as e:
            print(str(e))
       

if __name__=="__main__":
     import time
     while(1):
        try:
            run()
        except:
            pass
            time.sleep(1)
