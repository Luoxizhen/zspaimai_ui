import time
import json
from interface_base import union, user, finance, goods, order,topic
from utils import rwyaml,util
from interface_test.user_test import add_pwd
import pytest
def test_add():
    begin_time = round(time.time())+120
    end_time = begin_time + 800
    topic_info = {"title": "优惠劵", "begin_time": begin_time, "end_time": end_time}
    r = topic.add(**topic_info)

    assert r.json()['status'] == 200


def act():
    '''将已结束的专场全部下架'''
    search_info = {"status": 30, "is_shelves": 1}# 上架，已结束
    act_key = "is_shelves"
    # act_value = 1 if search_info[act_key] == 0 else 1
    r = topic.list(**search_info).json()['data']
    last_page = r['last_page']
    per_page = r['per_page']
    total = r['total']

    for k in range(last_page):
        if last_page > 2 and k != last_page-1:
            topic_num = 10
        elif total > 0:
            topic_num = total - per_page * (last_page-1)
        print(topic_num)
        r = topic.list(**search_info).json()

        for i in range(topic_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": "is_shelves", "value": 0}
            topic.edit_action(**act_info)
def test_act():

    act()

def test_add_is_recommended():
    '''添加专场并首页推荐'''
    begin_time = round(time.time()) + 120
    end_time = begin_time + 2000
    topic_info = {"title": "information_test_19", "begin_time": begin_time, "end_time": end_time}
    r = topic.add(**topic_info)
    id =r.json()['data']
    act_info = {"id":id, "act": "is_recommended", "value": 1}
    topic.edit_action(**act_info)





def test_shelves():
    '''将已结束的专场全部下架'''
    search_info = {"status": 30, "is_shelves": 1}
    r = topic.list(**search_info).json()['data']
    last_page = r['last_page']
    total = r['total']
    per_page = r['per_page']

    for k in range(last_page):
        if last_page > 2 and k != last_page-1:
            current_page_num = 10,
        else:
            current_page_num = total - per_page * (total-1)
        r = topic.list(**search_info).json()
        for i in range(current_page_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": "is_shelves", "value": 0}
            topic.edit_action(**act_info)










def test_list():
    search_info = {"status": 30, "is_shelves": 1}
    r = topic.list(**search_info).json()

def test_top():
    '''将已置顶的专场全部取消置顶'''
    search_info = {"status": 30, "top": 1}
    last_page = topic.list(**search_info).json()['data']['last_page']

    for k in range(last_page):
        if last_page > 2 & k != last_page-1:
            current_page_num = 10,
        else:
            current_page_num = topic.list(**search_info).json()['data']['total']
        r = topic.list(**search_info).json()
        for i in range(current_page_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": "top", "value": 0}
            topic.edit_action(**act_info)
def test_is_recommended():
    '''将已首页推荐的专场全部取消首页推荐'''
    search_info = {"status": 30, "is_recommended": 1}
    last_page = topic.list(**search_info).json()['data']['last_page']

    for k in range(10):
        if last_page > 2 & k != last_page-1:
            current_page_num = 10,
        else:
            current_page_num = topic.list(**search_info).json()['data']['total']
        r = topic.list(**search_info).json()
        for i in range(current_page_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": "is_recommended", "value": 0}
            topic.edit_action(**act_info)


def list_unrecommend():
    topic_info = {"is_recommended": 1}
    r = topic.list(**topic_info).json()['data']
    last_page = r['last_page']
    per_page = r['per_page']
    total = r['total']
    for k in range(last_page):
        if last_page > 2 and k != last_page-1:
            topic_num = per_page
        elif total > 0:
            topic_num = total - per_page * (last_page-1)
        r = topic.list(**topic_info).json()['data']['data']
        for i in range(topic_num):
            topic_id = r[i]['id']
            act_info = {"id": topic_id, "act": "is_recommended", "value": 0}
            topic.edit_action(**act_info)# 取消推荐

def test_list_unrecommend():
    list_unrecommend()
    assert 1==2






    '''列表编辑函数'''


def add_recommend(**topic_info):
    '''将推奖的专场全部下架，然后上传新专场，并首页推荐'''
    # list_unrecommend()
    # begin_time = round(time.time()) + 120
    # end_time = begin_time + 360000
    # topic_info = {"title": "11月专场", "begin_time": begin_time, "end_time": end_time}
    topic_id = topic.add(**topic_info).json()['data']
    act_info = {"id": topic_id, "act": "is_recommended", "value": 1} #首页推荐
    topic.edit_action(**act_info)
    return topic_id
def edit_topic():
    '''编辑专场: 将首页推荐的专场进行编辑'''
    search_info = {"is_shelves": 1,"is_recommended":1}
    topic_id = topic.list(**search_info).json()['data']['data'][0]['id']
    topic_info = topic.info(topic_id).json()['data']
    name = "topic"
    a = time.strptime('2021-11-5 00:00:00', '%Y-%m-%d %H:%M:%S')
    begin_time = time.mktime(a)#round(time.time())
    b = time.strptime('2021-11-30 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = time.mktime(b)
    topic_info['title'] = name
    topic_info['begin_time'] = begin_time
    topic_info['end_time'] = end_time
    print(topic_info)
    r = topic.edit(**topic_info)
    print(r.json())
def test_edit_topic():
    edit_topic()
    assert 1==2