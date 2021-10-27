import requests
import time
from utils import rwjson
from config import readCfg

admin_headers = rwjson.RwJson().readjson('interface_data', 'admin_headers.json')
base_url = readCfg.ReadCfg().get_base_url()
def updata_token(token):
    '''更新 user_headers'''
    user_headers = rwjson.RwJson().readjson('interface_data', 'user_headers.json')
    user_headers["token"] = token
    rwjson.RwJson().writejson('interface_data', 'user_headers.json', user_headers)

def get_user_headers():
    return rwjson.RwJson().readjson('interface_data', 'user_headers.json')


def goods_list():
    '''后台拍品列表'''
    url = base_url + '/admin/goods/goods_list'
    headers = admin_headers
    json = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"category_id\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"},{\"key\":\"type\",\"value\":1}]","page":1,"admin_name":"","topic_id":""}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def bidding(good_id, price, token=None):
    if token:
        updata_token(token)
    url = base_url + '/user/user/bid'
    json ={"goods_id": good_id,
             "price": price
           }
    updata_token(token)

    headers = get_user_headers()
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def user_bid(token):
    '''获取用户的中标记录'''
    url = base_url + '/user/goods/user_bid'
    updata_token(token)
    headers = get_user_headers()
    json = {"page":1,"act":"finish"}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()

def goods_add(**good_infos):
    '''后台添加拍品'''
    url = base_url + '/admin/goods/goods_add'
    headers = admin_headers
    goods_info_real = rwjson.RwJson().readjson('interface_data', 'goods.json')
    good_info_list = ["category_id", "platform", "begin_time", "end_time", "top_price", "name", "delay_time", "shape",
                      "price", "retain_price", "seller_name", "agreement_no", "buyer_service_rate", "type", "topic_id"]
    if good_infos != {}:
        print("真")
        for key in good_infos:

            if key in good_info_list:
                goods_info_real[key] = good_infos[key]

    r = requests.request('post', url=url, json=goods_info_real, headers=headers)
    print (r.json())
    return r