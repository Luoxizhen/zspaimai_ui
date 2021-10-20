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
def confirm_order():
    '''后台确认订单'''
    url = 'http://api.online.zspaimai.cn/admin/order/confirm_order'
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http://home.online.zspaimai.cn/',
               'AdminToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ5eWxBZG1pbiIsImlhdCI6MTYyNzAwNDc0OCwibmJmIjoxNjI3MDA0NzQ4LCJleHAiOjE2MjcwNDc5NDgsImRhdGEiOnsiYWRtaW5fdXNlcl9pZCI6MiwibG9naW5fdGltZSI6IjIwMjEtMDctMjMgMDk6NDU6NDgiLCJsb2dpbl9pcCI6IjE3Mi4xOS4wLjQifX0.KQfyTIx3MSRafMvKthxG-9yoQaMRaDLMA1gAYxtEOGo',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    json = {'id': 3}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    status = r.json()['status']
    return status
def take_delivery():
    '''后台确认提货'''
    url = 'http://api.online.zspaimai.cn/admin/order/take_delivery'
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http://home.online.zspaimai.cn/',
               'AdminToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ5eWxBZG1pbiIsImlhdCI6MTYyNzAwNDc0OCwibmJmIjoxNjI3MDA0NzQ4LCJleHAiOjE2MjcwNDc5NDgsImRhdGEiOnsiYWRtaW5fdXNlcl9pZCI6MiwibG9naW5fdGltZSI6IjIwMjEtMDctMjMgMDk6NDU6NDgiLCJsb2dpbl9pcCI6IjE3Mi4xOS4wLjQifX0.KQfyTIx3MSRafMvKthxG-9yoQaMRaDLMA1gAYxtEOGo',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    json = {"order_id": 713,
            "name": "大罗",
            "self": 1,
            "id_card": "4444444444444444444",
            "phone": "15622145010",
            "extract_time": 1626969600,
            "remarks": ""}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    status = r.json()['status']
    return status
def delivery():
    '''后台发货'''
    url = 'http://api.online.zspaimai.cn/admin/order/delivery'
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http://home.online.zspaimai.cn/',
               'AdminToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ5eWxBZG1pbiIsImlhdCI6MTYyNzAwNDc0OCwibmJmIjoxNjI3MDA0NzQ4LCJleHAiOjE2MjcwNDc5NDgsImRhdGEiOnsiYWRtaW5fdXNlcl9pZCI6MiwibG9naW5fdGltZSI6IjIwMjEtMDctMjMgMDk6NDU6NDgiLCJsb2dpbl9pcCI6IjE3Mi4xOS4wLjQifX0.KQfyTIx3MSRafMvKthxG-9yoQaMRaDLMA1gAYxtEOGo',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    json = {id: 714,
            express_id: 4,
            express_number: "SF1408640481240"}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    status = r.json()['status']
    return status
def recharge_list(token):
    '''获取支付方式'''
    url = base_url + '/user/wallet/recharge_list'
    updata_token(token)
    headers = get_user_headers()
    json = {"is_charge":0}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_region(token):
    '''获取中国省市'''
    url = base_url + '/user/addr/region'
    data = 'pid = 0 & inv ='
    updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def article(token):
    '''获取文章信息'''
    url = base_url + '/user/post/article'
    data = 'keywords=insurance_fee'
    updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def get_bid_info(goods_id,token):
    '''获取拍品的竞标信息'''
    url = base_url + '/user/goods/get_bid_info'
    json = {"goods_id": goods_id}
    updata_token(token)
    headers = get_user_headers()
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_list(token):
    '''获取用户的地址信息'''
    url = base_url + '/user/addr/list'
    updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url,headers=headers)
    return r.json()
def express(token):
    '''获取快递方式'''
    url = base_url + '/user/order/express'
    updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, headers=headers)
    return r.json()

def order_coupon(token, goods_id):
    '''进行订单支付'''
    url = base_url + '/user/coupon/order_coupon'
    updata_token(token)
    headers = get_user_headers()
    #goods = "[{\"goods_id\":2306,\"num\":1}]" goods 格式
    goods = "[{\"goods_id\":"+goods_id+",\"num\":1}]"
    print(goods)
    json = {"goods_total": 10000,
            "goods": goods,
            "order_model": 10}#余额支付
    r = requests.request('post', url=url, headers=headers, json=json)
    return r.json()
def calculate_freight(token):
    '''进行拍品的运费计算'''
    url = base_url + '/user/delivery/calculate_freight'
    updata_token(token)
    headers = get_user_headers()
    json = {"user_addr_id":177,
            "goods":"[{\"goods_id\":2185,\"buy_number\":1}]"}
    r = requests.request('post', url=url, headers=headers, json=json)
    return r.json()

def add_order(token):
    '''用户提交订单'''
    url = base_url + '/user/order/add_order'
    updata_token()
    headers = get_user_headers()
    json = {"goods_ids":"[\"2185\"]",
            "addr_id":177,
            "express":1,
            "express_chd":0,
            "payment_id":1,
            "pay_pwd":"246810",
            "express_fee":12,
            "insure_price":0,
            "insure_fee":0,
            "appointment":null,
            "total":21,
            "order_model":10,
            "coupon":"[]"}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()


