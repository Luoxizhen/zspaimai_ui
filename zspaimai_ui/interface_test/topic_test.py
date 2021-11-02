import time
import json
from interface_base import union, user, finance, goods, order,topic
from utils import rwyaml,utils
from interface_test.user_test import add_pwd
import pytest
def test_add():
    begin_time = round(time.time())+120
    end_time = begin_time + 800
    topic_info = {"title": "information_test_18", "begin_time": begin_time, "end_time": end_time}
    r = topic.add(**topic_info)

    assert r.json()['status'] == 200


def act(**search_info):
    '''将已结束的专场全部下架'''
    search_info = {"status": 30, "is_shelves": 1}
    act_key = search_info.keys()[1]
    act_value = 1 if search_info[act_key] == 0 else 1

    last_page = topic.list(**search_info).json()['data']['last_page']

    for k in range(last_page):
        if last_page > 2 & k != last_page-1:
            current_page_num = 10,
        else:
            current_page_num = topic.list(**search_info).json()['data']['total']
        r = topic.list(**search_info).json()
        for i in range(current_page_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": act_key, "value": act_value}
            topic.edit_action(**act_info)


def test_add_is_recommended():
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
    last_page = topic.list(**search_info).json()['data']['last_page']

    for k in range(last_page):
        if last_page > 2 & k != last_page-1:
            current_page_num = 10,
        else:
            current_page_num = topic.list(**search_info).json()['data']['total']
        r = topic.list(**search_info).json()
        for i in range(current_page_num):
            topic_id = r['data']['data'][i]['id']
            act_info = {"id": topic_id, "act": "is_shelves", "value": 0}
            topic.edit_action(**act_info)










def test_list():
    search_info = {"status": 30, "is_shelves": 1}
    r = topic.list(**search_info).json()
    print(r)
    assert 1==2
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