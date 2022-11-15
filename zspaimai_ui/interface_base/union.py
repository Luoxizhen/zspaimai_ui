from interface_base.user import base_url,admin_headers,update_token,get_user_headers
import requests

from utils import rwyaml,times
from common.readconfig import ini
from utils.rwjson import getjson
def union_topic():
    '''获取进行中的专场，用于设定推广素材所关联的专场'''
    url = base_url + '/admin/union/union_topic'
    headers = admin_headers
    data ={"union_id":0}
    r = requests.request('post', url=url, json=data, headers=headers)
    # topic_list = r.json()['data'][0]['id']
    return r
def union_add(**union_info):
    '''新增推广素材
    rebates_rate: 推广值返点， rebates_quota：返回额度
    接口返回信息：
    # union_id = r.json()['data']
    # union_info = {"union_info": {"new_union_id": union_id}}
    # rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', union_info)
    '''
    new_union = getjson.readjson('interface_data', 'union.json')
    url = base_url + '/admin/union/union_add'
    headers = admin_headers
    h5_url = ini.h5_url()
    new_union['h5_url'] = h5_url
    new_union.update(union_info)
    r = requests.request('post', url=url, json=new_union, headers=admin_headers)
    return r
def union_list():
    '''后台获取推广活动列表
    推广活动列表信息包含每个推广活动的详细信息
    返回数据如下：
    {"status":200,"msg":"操作成功",
    "data":{"total":5,"per_page":10,"current_page":1,"last_page":1,
    "data":[{
    "id":6,"name":"五月四期推广计划",
    "h5_url":"https:\/\/www.zsonline.cn\/",
    "appid":"wx50c05e976769b587",
    "mini_url":"pages\/switchPages\/index",
    "enable":1,"rebates_rate":3,"rebates_quota":2000,
    "start_time":1653616800,"end_time":1654516800,
    "copywriter":"珍稀苏维埃银行货币首次亮相中晟在线，原滋原味红色天安门1元，等待有缘人，加入推广计划赚取佣金！",
    "images":"[\"thumbnail\/tao\/5007-1.jpg\",\"thumbnail\/tao\/5004-1.jpg\",\"thumbnail\/wangli\/3024-1.jpg\"]",
    "poster":"[\"union\/1001.jpeg\"]",
    "create_time":"2022-05-24 18:32:26",
    "update_time":"2022-05-25 11:11:50","delete_time":0,"topic":[54]},
    {"id":5,"name":"五月四期推广计划","h5_url":"https:\/\/www.zsonline.cn\/","appid":"wx50c05e976769b587","mini_url":"pages\/switchPages\/index","enable":2,"rebates_rate":3,"rebates_quota":2000,"start_time":1653616800,"end_time":1653912000,"copywriter":"罕见苏维埃银行货币首次登场亮相中晟在线，原滋原味红色天安门，等待有缘人，加入推广计划与平台共享佣金！","images":"[\"union\/1001.jpeg\"]","poster":"[\"thumbnail\/tao\/5007-1.jpg\",\"thumbnail\/tao\/5004-1.jpg\",\"thumbnail\/wangli\/3024-1.jpg\"]","create_time":"2022-05-24 18:27:48","update_time":"2022-05-25 08:53:30","delete_time":0,"topic":[54]}
    ]},
    "shop_switch":"0"}
    '''
    url = base_url + '/admin/union/union_list'
    headers = admin_headers
    data = "page=1"
    r = requests.request('get', url=url, params=data, headers=headers)
    return r

def union_edit(**union_info):
    '''后台编辑推广活动
    {"name":"五月四期推广计划",
    "h5_url":"https://www.zsonline.cn/",
    "copywriter":"罕见苏维埃银行货币首次登场亮相中晟在线，原滋原味红色天安门，等待有缘人，加入推广计划与平台共享佣金！",
    "appid":"wx50c05e976769b587",
    "mini_url":"pages/switchPages/index",
    "enable":2,"rebates_rate":3,
    "rebates_quota":2000,
    "start_time":1653616800,"end_time":1653912000,
    "images":"[\"union/1001.jpeg\"]",
    "poster":"[\"thumbnail/tao/5007-1.jpg\",\"thumbnail/tao/5004-1.jpg\",\"thumbnail/wangli/3024-1.jpg\"]",
    "topic":"[54]","id":5}
    '''
    url = base_url + '/admin/union/union_edit'
    headers = admin_headers
    json = union_info
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def union_del(id):
    '''删除推广素材'''
    url = base_url + '/admin/union/union_del'
    headers = admin_headers
    data = {'id': id}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def act_edit(union_id, act_value):
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

def union_index(userno):
    '''从后台推广用户列表搜索用户
    # {"status": 200, "msg": "操作成功",
    "data": {"total": 1, "per_page": 10, "current_page": 1, "last_page": 1,
    "data": [
    #     {"user_id": 497, "role": 20, "order_money": "0.00", "commission": 0, "quota": "2000.00", "role_rate": 4,
    #      "out_commi": "0.00", "userno": 193297}],
    "order_num": "193",
    "newbie": "138"},
    "shop_switch": "0"}'''
    url = base_url + '/admin/union/index'
    headers = admin_headers

    data = 'role=&userno=' + userno +'&page=1'
    print(data)
    r = requests.request('get', url=url, params=data, headers=headers)

    return r

def user_list(userno):

    '''后台获取推广用户信息
    :rtype: object
    '''
    # union_user_info(userno):
    url = base_url + '/admin/user/list'
    headers = admin_headers
    search_str = '[{\"key\":\"userno\",\"value\":\"' + userno + '\"},{\"key\":\"phone\",\"value\":\"\"},{\"key\":\"is_mobile\",\"value\":\"\"},{\"key\":\"name\",\"value\":\"\"},{\"key\":\"is_real\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_robot\",\"value\":\"\"}]'
    data = {
        "page": 1,
        "where": search_str
    }
    r = requests.request('post', url=url, json=data, headers=headers)
    # user_info = {'user_info': {'userno': userno, 'data': r.json()['data']}}
    # rwyaml.generate_yaml_doc('interface_data', 'union.yml', user_info)
    return r

def manual_operation(user_id, relation_ids):
    '''后台关联用户'''
    url = base_url + '/admin/union/manual_operation'
    headers = admin_headers
    # data = {
    #     "user_id": 300,
    #     "relation_ids": "299"
    # }
    data = {
        "user_id": user_id,
        "relation_ids": relation_ids
    }
    r = requests.request('post', url=url, params=data, headers=headers)
def set_union_role(userno, role):
    '''设置用户角色-业务员,role = 20, 设置用户角色-普通用户， role = 10'''
    url = base_url + '/admin/union/set_union_role'
    headers = admin_headers
    userid = int(userno) - 192800
    if(role==20):
        data = {
            "user_id": userid,
            "role": 20,
            "role_rate": "4"
        }
    elif(role==10):
        data = {
            "user_id": userid,
            "role": 10,
            "role_rate": "0"
        }
    r = requests.request('post', url=url, json=data, headers=headers)
    return r

def union_user(userno):
    '''后台查看某一个推广用户的 关联用户详情'''
    url = base_url + '/admin/union/union_user'
    headers = admin_headers
    userid = int(userno) - 192800
    print(userid)
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def union_order(userno):
    '''后台查看关联订单详情'''
    url = base_url + '/admin/union/union_order'
    headers = admin_headers
    userid = int(userno) - 192800
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r

def union_commi(userno):
    '''后台查看推广值明细'''
    url = base_url + '/admin/union/union_commi'
    headers = admin_headers
    userid = int(userno) - 192800
    data = {"user_id": userid, "page": 1}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r
def union_join(token=None,fr='pc'):
    '''用户加入推广计划'''
    url = base_url + '/user/union/union_join'
    if token:
        update_token(token)
    times.sleep(2)
    headers = get_user_headers()
    data = {}
    r = requests.request('post', url=url, params=data, headers=headers)
    return r
def union_user_list(token=None):
    '''查看用户的关联用户列表'''
    if token:
        update_token(token)
    url = base_url + 'user/union/user_union_list'
    headers = get_user_headers()
    data = {"page": 1}
    r = requests.request('get', url=url, json=data, headers=headers)
    return r

def union_order_list(token=None):
    '''查看用户的推广订单列表'''
    url = base_url + '/user/union/union_order_list'
    if token:
        update_token(token)
    headers = get_user_headers()
    data = {"page": 1}
    r = requests.request('get', url=url, json=data, headers=headers)
    return r
def union_commi_list(token=None):
    '''查看用户的推广订单列表'''
    url = base_url + '/user/union/union_commi_list'
    if token:
        update_token(token)
    headers = get_user_headers()
    data = {"page": 1}
    r = requests.request('get', url=url, params=data, headers=headers)
    rwyaml.generate_yaml_doc('interface_data', 'union_log.yml', r)
    return r


def union_list_user(pageno=1, token=None):
    '''获取推广素材'''
    url = base_url + '/user/union/union_list'
    if token:
        update_token(token)
    headers = get_user_headers()
    data = 'page='+str(pageno)
    print(data)
    r = requests.request('get', url=url, params=data, headers=headers)
    return r

if __name__ == "__main__":
    new_union = getjson.readjson('interface_data', 'union.json')
    print(new_union)
