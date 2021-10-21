import requests
from utils import rwjson
import logging
import interface_base.interface_base as itf
import config.readCfg as cfg
from utils import rwjson
from config import readCfg
# base_url = "http://api.online.zspaimai.cn"
# def get_user_headers():
#     return rwjson.RwJson().readjson('interface_data', 'user_headers.json')
# def get_admin_headers():
#     return rwjson.RwJson().readjson('interface_data', 'admin_headers.json')
user_headers = itf.get_user_headers()
admin_headers = itf.get_admin_headers()
base_url = cfg.ReadCfg().get_base_url()
def get_user_headers():
    return rwjson.RwJson().readjson('interface_data', 'user_headers.json')
def get_token():
    '''获取用户的token '''
    url = base_url+"/user/user/login?from=pc"
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http: // home.online.zspaimai.cn /',
               'token': 'xu16kny28l12lhnmitevanfpb - yzul_v',
               'Appfrom': 'pc',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    json = {"phone": "15622145010",
            "pwd": "123456"}
    r = requests.request('post', url=url, json=json, headers=headers)
    if r.json()['status']==200:
        return r.json()['data']['token']

def update_token(token):

    dict = rwjson.RwJson().readjson('interface_data', 'user_headers.json')

    dict["token"] = token
    rwjson.RwJson().writejson('interface_data', 'user_headers.json', dict)




def get_msg(phone):
    url = base_url + '/user/user/msg'
    headers = user_headers
    data = {"phone": phone}
    r = requests.request('post', url=url,  json=data, headers=headers)
def quick_login(phone):
    url = base_url + '/user/user/quick_login'
    headers = user_headers
    data = {"phone": phone, "vcode": "123456"}
    r = requests.request('post', url=url, json=data, headers=headers)
    #token = r.json()['data']['token']
    #userno = r.json()['data']['userno']
    return r
def get_msg_union(inv, phone):
    url = base_url + '/user/user/msg'
    headers = user_headers
    data = {"phone": phone, "from": "pc", "inv": inv}
    r = requests.request('post', url=url,  json=data, headers=headers)
def quick_login_union(inv, phone):
    url = base_url + '/user/user/quick_login'
    headers = user_headers
    data = {"phone": phone, "vcode": "123456", "inv": inv}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r



def verify(phone):
    url = base_url + '/user/user/verify'
    headers = get_user_headers()
    json = {
        "phone": phone,
        "vcode": "123456"
    }
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
    # {
    #     "status": 200,
    #     "msg": "操作成功",
    #     "data": {
    #         "user_code": "eceb1edcdd191546d8877403aeae23e3"
    #     },
    #     "shop_switch": "0"
    # }
def add_pwd(user_code):
    url = base_url + '/user/user/add_pwd'
    headers = get_user_headers()
    json = {
        "user_code": user_code,
        "new_pwd": "246810"
    }
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
    # {
    #     "status": 200,
    #     "msg": "设置成功",
    #     "data": [],
    #     "shop_switch": "0"
    # }