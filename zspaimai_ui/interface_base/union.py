import interface_base.interface_base as itf
import config.readCfg as cfg
import requests
import time

from utils import rwyaml, rwjson
# user_headers = itf.get_user_headers()
# admin_headers = itf.get_admin_headers()
base_url = cfg.ReadCfg().get_base_url()
user_headers = rwjson.RwJson().readjson('interface_data', 'user_headers.json')
admin_headers = rwjson.RwJson().readjson('interface_data', 'admin_headers.json')
user_headers_app = rwjson.RwJson().readjson('interface_data', 'user_headers_app.json')
def get_union_topic():
    '''获取进行中的专场，用于设定推广素材所关联的专场'''
    url = base_url + '/admin/union/union_topic'
    headers = admin_headers
    data = {"union_id": "0"}
    r = requests.request('post', url=url, json=data, headers=headers)
    topic_list = r.json()['data'][0]['id']
    print(r)
    return topic_list
def union_add():
    '''新增推广素材'''
    url = base_url + '/admin/union/union_add'
    headers = admin_headers

    begin_time = time.time()
    end_time = begin_time + 360000
    topic_id = get_union_topic()
    #topic = [topic_id]
    topic = '[' + str(topic_id) +']'
    '''rebates_rate: 推广值返点， rebates_quota：返回额度 '''
    union_name = rwyaml.get_yaml_data('interface_data', 'union.yml')['union_name']
    data = {
        "name": union_name,
        "h5_url": "http://home.online.zspaimai.cn/",
        "copywriter": "中晟在线--慧眼识宝，悦享收藏！",
        "appid": "wx50c05e976769b587",
        "mini_url": "pages/switchPages/index",
        "enable": 1,
        "rebates_rate": "10",
        "rebates_quota": "2000",
        "start_time": begin_time,
        "end_time": end_time,
        "images": "[\"picture/2HKbk2JxdSAZnTQ2fmPKD8zAKjWxSi.JPG\"]",
        "poster": "[\"thumbnail/yBA5rkeEpijN7MaRQ8ZK4iWxcabYfC.JPG\"]",
        "topic": topic
    }
    print(data)
    r = requests.request('post', url=url, json=data, headers=headers)
    union_id = r.json()['data']
    union_info = {"union_info": {"new_union_id": union_id}}

    rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', union_info)

    return r
def union_list():
    '''推广活动列表'''
    url = base_url + '/admin/union/union_list'
    headers = admin_headers
    data = "page=1"
    r = requests.request('get', url=url, params=data, headers=headers)
    union_list_info = {'最新推广计划': time.time(),
                       'total': r.json()['data']['total'],
                       'data': r.json()['data']['data'][0]}
    rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', union_list_info)
    return r
def union_del(id):
    '''推广活动列表'''
    url = base_url + '/admin/union/union_del'
    headers = admin_headers

    data = {'id': id}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def union_act_edit(union_id, act_value):
    '''素材下架,value=2, 素材上架，value=1'''
    url = base_url + '/admin/union/act_edit'
    headers = admin_headers
    if (act_value == 1):
        data = {
            "id": union_id,
            "act": "enable",
            "value": 1
        }# 素材上架
    else:
        data = {
            "id": union_id,
            "act": "enable",
            "value": 2
        }# 素材下架

    r = requests.request('post', url=url, json=data, headers=headers)
    return r

def union_index():
    '''从推广用户列表搜索用户'''
    url = base_url + '/admin/union/index'
    headers = admin_headers
    userno = rwyaml.get_yaml_data('interface_data', 'union.yml')['userno']
    data = 'role=&userno=' + userno +'&page=1'
    r = requests.request('get', url=url, params=data, headers=headers)
    rwyaml.generate_yaml_doc('interface_data', 'union.yml', r.json())
    return r
def union_user_info(userno):
    '''获取推广用户信息'''
    url = base_url + '/admin/user/list'
    headers = admin_headers
    search_str = '[{\"key\":\"userno\",\"value\":\"' + userno + '\"},{\"key\":\"phone\",\"value\":\"\"},{\"key\":\"is_mobile\",\"value\":\"\"},{\"key\":\"name\",\"value\":\"\"},{\"key\":\"is_real\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_robot\",\"value\":\"\"}]'
    data = {
        "page": 1,
        "where": search_str
    }
    r = requests.request('post', url=url, json=data, headers=headers)
    user_info = {'user_info': {'userno': userno, 'data': r.json()['data']}}
    rwyaml.generate_yaml_doc('interface_data', 'union.yml', user_info)
    return r

def union_manual_operation():
    '''后台关联用户'''
    url = base_url + '/admin/union/manual_operation'
    headers = admin_headers
    data = {
        "user_id": 300,
        "relation_ids": "299"
    }
    r = requests.request('post', url=url, params=data, headers=headers)
def union_set_role(role):
    '''设置用户角色-业务员,role = 20, 设置用户角色-普通用户， role = 10'''
    url = base_url + '/admin/union/set_union_role'
    headers = admin_headers
    if(role==20):
        data = {
            "user_id": 276,
            "role": 20,
            "role_rate": "4"
        }
    elif(role==10):
        data = {
            "user_id": 276,
            "role": 10,
            "role_rate": "0"
        }
    r = requests.request('post', url=url, json=data, headers=headers)
    return r.json()['status']

def union_user():
    '''后台查看某一个推广用户的 关联用户详情'''
    url = base_url + '/admin/union/union_user'
    headers = admin_headers

    userid = rwyaml.get_yaml_data('interface_data', 'union.yml')['user_info']['data']['data'][0]['id']
    print(userid)
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def union_order():
    '''后台查看关联订单详情'''
    url = base_url + '/admin/union/union_order'
    headers = admin_headers
    userid = rwyaml.get_yaml_data('interface_data', 'union.yml')['user_info']['data']['data'][0]['id']
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r

def union_commi():
    '''后台查看推广值明细'''
    url = base_url + '/admin/union/union_commi'
    headers = admin_headers
    userid = rwyaml.get_yaml_data('interface_data', 'union.yml')['user_info']['data']['data'][0]['id']
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def union_join():
    '''用户加入推广计划'''
    url = base_url + '/user/union/union_join'
    headers = user_headers
    data = {"from": "pc"}
    r = requests.request('post', url=url, json=data, headers=headers)
    print(r)
    return r
def union_user_1():
    '''查看用户的关联用户列表'''
    url = base_url + '/user/union/union_user_list'
    headers = user_headers
    data = {"from": "pc", "page": 1}
    r = requests.request('get', url=url, json=data, headers=headers)
    return r

def union_order_1():
    '''查看用户的推广订单列表'''
    url = base_url + '/user/union/union_order_list'
    headers = user_headers
    data = {"from": "pc", "page": 1}
    r = requests.request('get', url=url, json=data, headers=headers)
    return r
def union_commi_1():
    '''查看用户的推广订单列表'''
    url = base_url + '/user/union/union_commi_list'
    headers = user_headers
    data = {"from": "pc", "page": 1}
    r = requests.request('get', url=url, params=data, headers=headers)
    rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', r)
    return r

def union_list_1():
    '''获取推广素材'''
    url = base_url + '/user/union/union_list'
    headers = user_headers
    data = 'page=1&from=pc'
    r = requests.request('get', url=url, params=data, headers=headers)
    rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', r)
    return r


def union_user_info_3():
    '''查看用户关联信息'''
    url = base_url + '/user/union/union_user_info'
    headers = user_headers_app
    data = {"from": "mini"}
    r = requests.request('get', url=url, params=data, headers=headers)
def union_user_list_3():
    '''获取关联用户'''
    url = base_url + '/user/union/union_user_list'
    headers = user_headers_app
    data = {"from": "mini", "page": 1}
    r = requests.request('get', url=url, params=data, headers=headers)
def union_order_list_3():
    '''查看推广订单'''
    url = base_url + '/user/union/union_order_list'
    headers = user_headers_app
    data = {"from": "mini", "page": 1}
    r = requests.request('get', url=url, params=data, headers=headers)
def union_commi_list_3():
    '''查看推广值'''
    url = base_url + '/user/union/union_commi_list'
    headers = user_headers_app
    data = {"from": "mini", "page": 1}
    r = requests.request('get', url=url, params=data, headers=headers)