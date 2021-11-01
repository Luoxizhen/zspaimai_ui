import time, json
from utils import rwjson, utils
import requests
from interface_base.user import update_token, get_user_headers,base_url,admin_headers
def add(**topic_info):
    url = base_url + "/admin/topic/add"
    headers = admin_headers
    info = {"title":"订阅信息测试","begin_time":1635502200,"end_time":1635502800,"sort":"100","images":"picture/QCFNhmCJJ6fNijxWYQJFkixSYx6Mkm.png","small_images":"picture/RjNDKXXknaJF7W5hKCnYY4WEJjBe7P.png","content":"","mini_small_images":"picture/Kp5ykpFpT5CRXpspQfzpfj5MQ87DFy.png","mini_images":"picture/hhMMwMBFHwfcGZjeJZYKEE4fCAk8Z8.png"}
    for key in topic_info:
        if key in info.keys():
            info[key] = topic_info[key]
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
    search_str = utils.kwargs_to_str(**search_info)

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
    url = base_url + "/admin/topic/goods_add_list"
    headers = admin_headers
    info = {"topic_id":129,"goods":"[{\"goods_id\":2495,\"is_recommended\":0}]"}
    # for key in topic_info:
    #     if key in info.keys():
    #         info[key] = topic_info[key]
    r = requests.request('post', url=url, json=info, headers=headers)
    return r