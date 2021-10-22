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
    url =  base_url + '/admin/order/confirm_order'
    headers = admin_headers
    json = {'id': 1451}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def take_delivery(order_id):
    '''后台确认提货'''
    url = 'http://api.online.zspaimai.cn/admin/order/take_delivery'
    headers = admin_headers
    extract_time = round(time.time())
    json = {"order_id": order_id,
            "name": "大罗",
            "self": 1,
            "id_card": "4444444444444444444",
            "phone": "15622145010",
            "extract_time": extract_time,
            "remarks": ""}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def deliver(order_id):
    '''后台发货'''
    url = base_url +'/admin/order/deliver'
    headers = admin_headers
    json = {'id': order_id,
            'express_id': 4,
            'express_number': "SF6090856325401"}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def recharge_list(token=None):
    '''获取支付方式'''
    url = base_url + '/user/wallet/recharge_list'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    json = {"is_charge":0}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_region(token=None):
    '''获取中国省市'''
    url = base_url + '/user/addr/region'
    data = 'pid = 0 & inv ='
    if not token:
        updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def article(token=None):
    '''获取文章信息'''
    url = base_url + '/user/post/article'
    data = 'keywords=insurance_fee'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def get_bid_info(goods_id,token=None):
    '''获取拍品的竞标信息'''
    url = base_url + '/user/goods/get_bid_info'
    json = {"goods_id": goods_id}
    if not token:
        updata_token(token)
    headers = get_user_headers()
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_list(token=None):
    '''获取用户的地址信息'''
    '''{'status': 200, 'msg': '操作成功', 'data': [{'id': 177, 'name': '张生', 'phone': '18023038634', 'address': '我家', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3036, 'is_default': 1, 'area': '广东省,广州市,萝岗区', 'province_ny_name': '广州市', 'county_name': '萝岗区'}, {'id': 164, 'name': '大罗', 'phone': '15622145010', 'address': '黄沙', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3045, 'is_default': 0, 'area': '广东省,广州市,荔湾区', 'province__name': '广州市', 'county_name': '荔湾区'}, {'id': 165, 'name': '大罗', 'phone': '15622145010', 'address': '如意坊', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3045, 'is_default': 0, 'area': '广东省,广州市,荔湾区', 'province_name': '广州市', 'county_name': '荔湾区'}], 'shop_switch': '0'}
'''
    url = base_url + '/user/addr/list'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url,headers=headers)
    return r
def express(token=None):
    '''获取快递方式'''
    '''{'status': 200, 'msg': '操作成功', 'data': [{'id': 1, 'show': 1, 'icon': '', 'name': '快递到付'}, {'id': 3, 'show': 2, 'icon': '', 'name': '上门自提'}], 'shop_switch': '0'}
'''
    url = base_url + '/user/order/express'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, headers=headers)
    return r

def order_coupon(token=None, goods_id):
    '''进行订单支付'''
    url = base_url + '/user/coupon/order_coupon'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    #goods = "[{\"goods_id\":2306,\"num\":1}]" goods 格式
    goods = "[{\"goods_id\":"+goods_id+",\"num\":1}]"
    print(goods)
    json = {"goods_total": 10,
            "goods": goods,
            "order_model": 10}#余额支付
    r = requests.request('post', url=url, headers=headers, json=json)
    return r.json()
def calculate_freight(token=None):
    '''进行拍品的运费计算'''
    url = base_url + '/user/delivery/calculate_freight'
    if not token:
        updata_token(token)
    headers = get_user_headers()
    json = {"user_addr_id":177,
            "goods":"[{\"goods_id\":2185,\"buy_number\":1}]"}
    r = requests.request('post', url=url, headers=headers, json=json)
    return r.json()

def add_order(token=None,goods_id,addr_id):
    '''用户提交订单'''
    if not token:
        updata_token(token)
    #"coupon":"[]", 优惠劵
    url = base_url + '/user/order/add_order'
    #updata_token(token)
    headers = get_user_headers()
    #goods_ids = "[\"2185\"]"
    #goods_ids = "["+str(goods_id)+"]"
    print(goods_id)

    json = {"goods_ids":goods_id,
            "addr_id":addr_id,
            "express":2,
            "express_chd":0,
            "payment_id":1,
            "pay_pwd":"246810",
            "express_fee":14,
            "insure_price":0,
            "insure_fee":0,
            "appointment":'',
            "total":40,
            "order_model":10,
            "coupon":"[]",
            "AppFrom": "pc"}
    print(json)
    r = requests.request('post', url=url, json=json, headers=headers)
    return r

def add_order1(token=None,goods_id):
    '''用户提交订单-上门自提'''
    if not token:
        updata_token(token)
    #"coupon":"[]", 优惠劵
    url = base_url + '/user/order/add_order'
    #updata_token(token)
    headers = get_user_headers()
    #goods_ids = "[\"2185\"]"
    #goods_ids = "["+str(goods_id)+"]"
    print(goods_id)

    json = {"goods_ids":goods_id,
            "addr_id":0,
            "express":3,
            "express_chd":0,
            "payment_id":1,
            "pay_pwd":"246810",
            "express_fee":0,
            "insure_price":0,
            "insure_fee":0,
            "appointment":'2021-10-21',
            "total":40,
            "order_model":10,
            "coupon":"[]",
            "AppFrom": "pc"}
    print(json)
    r = requests.request('post', url=url, json=json, headers=headers)
    # {
    #     "status": 200,
    #     "msg": "操作成功",
    #     "data": {
    #         "verify_code": "",
    #         "reId": "1455",
    #         "orderNo": "2021102115580233428",
    #         "money": 40,
    #         "qrcode": "",
    #         "name": "余额",
    #         "pay_logo": "icon\/wallet.png",
    #         "pay_status": 1
    #     },
    #     "shop_switch": "0"
    # }
    return r
def refund_goods():
    '''查找订单包含的拍品，商品'''
    '''{"status":200,"msg":"操作成功","data":[{"goods_id":2334,"name":"退化退款测试-13"},{"goods_id":2335,"name":"退化退款测试-14"}],"shop_switch":"0"}'''
    url = base_url + '/admin/order/refund_goods'
    headers = admin_headers
    json = {"order_id":1449}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def refund():
    '''售后-仅退款'''
    '''{"status":200,"msg":"操作成功","data":null,"shop_switch":"0"}'''
    url = base_url +'/admin/order/refund'
    headers = admin_headers
    json = {"order_id":1450,
            "type":1,
            "refund_desc":"退化退款测试-8 退款",
            "refund_money":"20",
            "goods_id":"[2328]"}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r

def remittance_finish(id):
    '''后台确认转账汇款告知'''
    '''{"status":200,"msg":"操作成功","data":[],"shop_switch":"0"}'''
    url = base_url + ''
    headers = admin_headers
    json = {"id":id,
            "remarks":""}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
