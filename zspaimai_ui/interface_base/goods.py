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

def goods_add(begin_time, end_time, name):
    '''后台添加拍品'''
    url = base_url + '/admin/goods/goods_add'
    headers = admin_headers
    # begin_time = round(time.time())
    # end_time = begin_time + 3600 #3600 为一小时
    json = {"category_id": 35,
            "platform": "1",
            "begin_time": begin_time,
            "end_time": end_time,
            "top_price": "",
            "name": name,
            "delay_time": 60,
            "shape": "98",
            "price": "10",# 起拍价
            "retain_price": "",
            "seller_name": "大罗",
            "agreement_no": "a0000152",
            "create_user": "",
            "create_date": "",
            "content": "<p>1960年第三版人民币壹圆拖拉机狮子号一枚</p>",
            "original_image": "[\"picture/wxTj7wm3XN2JkhFZXQCSpiRKRhZx5C.jpeg\"]",
            "images": "[\"thumbnail/fjZac4eFCsxk2Py2z4BiQ4N4fbbC6x.png\"]",
            "freight_id": 51,
            "is_freight": 0,
            "goods_weight": "",
            "buyer_service_rate": "8",
            "meta": "{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"1\",\"seller_insure_no_deal\":\"1\",\"service_fee_deal\":\"2\",\"service_fee_no_deal\":\"1\",\"production_fee_deal\":\"15\",\"production_fee_no_deal\":\"15\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}",
            "type": 1,
            "topic_id": "[15]"
        }
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def goods_list():
    '''后台拍品列表'''
    url = base_url + '/admin/goods/goods_list'
    headers = admin_headers
    json = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"category_id\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"},{\"key\":\"type\",\"value\":1}]","page":1,"admin_name":"","topic_id":""}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def bidding(good_id, price, token):
    url = base_url + '/user/user/bid'
    json ={"goods_id": good_id,
             "price": price
           }
    print (json)
    updata_token(token)

    headers = get_user_headers()
    print(headers)

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

