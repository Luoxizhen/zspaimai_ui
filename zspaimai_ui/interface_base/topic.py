import time, json
from utils import rwjson, util
from utils.rwjson import getjson
import requests
from interface_base.user import update_token, get_user_headers,base_url,admin_headers
def add(**topic_info):
    url = base_url + "/admin/topic/add"
    headers = admin_headers
    info = getjson.readjson('interface_data','topic.json')
    info.update(topic_info)
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def edit_action(**act_info):
    url = base_url + "/admin/topic/edit_action"
    headers = admin_headers
    # info = {"id":111,"act":"is_recommended","value":0}
    # info = {"id":111,"act":"top","value":0}
    info = {"id": 111, "act": "is_shelves", "value": 0}
    for key in act_info:
        if key in info.keys():
            info[key] = act_info[key]
    r = requests.request('post', url=url, json=info, headers=headers)
    return r

def list(page=1, **topic_info):
    url = base_url + "/admin/topic/list"
    headers = admin_headers
    info = {"where":"[{\"key\":\"title\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"}]","page":1}
    search_info = {"title": "", "status": "", "is_shelves": "", "top": "", "is_recommended": ""}
    for key in topic_info:
        if key in search_info.keys():
            search_info[key] = topic_info[key]
    search_str = util.kwargs_to_str(**search_info)

    info["where"] = search_str
    if page > 1:
        info["page"] = page
    r = requests.request('post', url=url, json=info, headers=headers)
    return r

def goods_add_list(**topic_info):
    url = base_url + "/admin/topic/goods_add_list"
    headers = admin_headers
    info = {"topic_id":129,"name":"","page":1}
    # for key in topic_info:
    #     if key in info.keys():
    #         info[key] = topic_info[key]
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def add_topic_goods(**topic_info):
    '''专场添加拍品'''
    url = base_url + "/admin/topic/add_topic_goods"
    headers = admin_headers
    info = {"topic_id":129,"goods":"[{\"goods_id\":2495,\"is_recommended\":0}]"}
    for key in topic_info:
        if key in info.keys():
            info[key] = topic_info[key]
    print(info)
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def edit(**topic_info):
    '''编辑专场'''
    url = base_url + "/admin/topic/edit"
    headers = admin_headers
    info = {"title":"ggg",
            "begin_time":1635912287,
            "end_time":1638201600,
            "sort":1,
            "images":"picture/3pAmz8c7cH5tNMChNG5detGwCXcr5X.png",
            "small_images":"picture/nMhCp8sKindBmNmnkFrGSjs7KxEBKP.png",
            "mini_images":"picture/kHd5DGCiAkmnZ5eiQDhna4AyYQSa45.png",
            "mini_small_images":"picture/6Cdw5QwZ74ixSbsYhA22yRJfGHYcXn.png",
            "id":162,
            "content":""}
    for key in topic_info:
        if key in info.keys():
            info[key] = topic_info[key]
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def info(id):
    '''获取专场信息'''
    url = base_url + "/admin/topic/info"
    headers = admin_headers
    info = {"id": id}
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def user_list(page=1,status=30):
    '''pc 端获取专场列表，参数
    status: 0 全部状态， 30 已结束
    page: 2'''
    url = base_url + "/user/topic/list"
    headers = get_user_headers()
    info = {"page":page,"status":status}



    r = requests.request('get', url=url, params=info, headers=headers)
    return r