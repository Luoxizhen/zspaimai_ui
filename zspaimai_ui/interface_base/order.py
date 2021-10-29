import requests
import time, json
from utils import rwjson, utils
from interface_base.user import update_token, get_user_headers,base_url,admin_headers



def confirm_order(id):
    '''后台确认订单'''
    url =  base_url + '/admin/order/confirm_order'
    headers = admin_headers
    json = {'id': id}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def take_delivery(order_id,**userinfo):
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
    if userinfo != {}:
        for key in userinfo:
            if key in json.keys():
                json['key'] = userinfo[key]
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def deliver(order_id, **deliverinfo):
    '''后台发货'''
    url = base_url +'/admin/order/deliver'
    headers = admin_headers
    json = {'id': order_id,
            'express_id': 4,
            'express_number': "SF6090856325401"}
    for key in deliverinfo:
        if key in json.keys():
            json[key] = json[key]
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def recharge_list(token=None):
    '''获取支付方式'''
    url = base_url + '/user/wallet/recharge_list'
    if token:
        update_token(token)
    headers = get_user_headers()
    json = {"is_charge":0}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_region(token=None):
    '''获取中国省市'''
    url = base_url + '/user/addr/region'
    data = 'pid = 0 & inv ='
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def article(token=None):
    '''获取文章信息'''
    url = base_url + '/user/post/article'
    data = 'keywords=insurance_fee'
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, params=data, headers=headers)
    return r.json()
def get_bid_info(goods_id,token=None):
    '''获取拍品的竞标信息'''
    url = base_url + '/user/goods/get_bid_info'
    json = {"goods_id": goods_id}
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def addr_list(token=None):
    '''获取用户的地址信息'''
    '''{'status': 200, 'msg': '操作成功', 'data': [{'id': 177, 'name': '张生', 'phone': '18023038634', 'address': '我家', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3036, 'is_default': 1, 'area': '广东省,广州市,萝岗区', 'province_ny_name': '广州市', 'county_name': '萝岗区'}, {'id': 164, 'name': '大罗', 'phone': '15622145010', 'address': '黄沙', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3045, 'is_default': 0, 'area': '广东省,广州市,荔湾区', 'province__name': '广州市', 'county_name': '荔湾区'}, {'id': 165, 'name': '大罗', 'phone': '15622145010', 'address': '如意坊', 'zipcode': '', 'province': 19, 'city': 289, 'county': 3045, 'is_default': 0, 'area': '广东省,广州市,荔湾区', 'province_name': '广州市', 'county_name': '荔湾区'}], 'shop_switch': '0'}
'''
    url = base_url + '/user/addr/list'
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url,headers=headers)
    return r
def express(token=None):
    '''获取快递方式'''
    '''{'status': 200, 'msg': '操作成功', 'data': [{'id': 1, 'show': 1, 'icon': '', 'name': '快递到付'}, {'id': 3, 'show': 2, 'icon': '', 'name': '上门自提'}], 'shop_switch': '0'}
'''
    url = base_url + '/user/order/express'
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, headers=headers)
    return r

def order_coupon(goods_id,token=None):
    '''订单支付时获取可以使用的优惠劵'''
    url = base_url + '/user/coupon/order_coupon'
    if token:
        update_token(token)
    headers = get_user_headers()
    #goods = "[{\"goods_id\":2306,\"num\":1}]" goods 格式
    goods = "[{\"goods_id\":"+goods_id+",\"num\":1}]"
    print(goods)
    json = {"goods_total": 10,
            "goods": goods,
            "order_model": 10}#余额支付
    r = requests.request('post', url=url, headers=headers, json=json)
    return r.json()


# def add_order1(goods_id,addr_id,token=None):
#     '''用户提交订单'''
#     if token:
#         update_token(token)
#     #"coupon":"[]", 优惠劵
#     url = base_url + '/user/order/add_order'
#     #updata_token(token)
#     headers = get_user_headers()
#     #goods_ids = "[\"2185\"]"
#     #goods_ids = "["+str(goods_id)+"]"
#     print(goods_id)
#
#     json = {"goods_ids":goods_id,
#             "addr_id":addr_id,
#             "express":2,
#             "express_chd":0,
#             "payment_id":1,
#             "pay_pwd":"246810",
#             "express_fee":14,
#             "insure_price":0,
#             "insure_fee":0,
#             "appointment":'',
#             "total":40,
#             "order_model":10,
#             "coupon":"[]",
#             "AppFrom": "pc"}
#     print(json)
#     r = requests.request('post', url=url, json=json, headers=headers)
#     return r

def add_order(token=None, **info):
    '''用户提交订单，各参数：
    express: 订单配送方式， 3-上门自提，2-快递到付
    addr_id: 收货地址，0-上门自提的地址，即公司地址，express 选择快递到付时，应填入用户地址列表中的地址编号
    order_model: 支付方式， 10-余额，20-微信，30-银行转账
    total：支付总金额
    '''
    print(token)

    if token:
        update_token(token)
    url = base_url + '/user/order/add_order'
    headers = get_user_headers()

    order_info = rwjson.RwJson().readjson('interface_data', 'order.json')
    for key in info:
        if key in order_info.keys():
            order_info[key] = info[key]
    if order_info['addr_id'] != 0: #如果收货地址不是上门自提地址，公司地址，则将配送方式改为快递到付
        order_info['express'] = 1
        order_info['appointment'] = ''
        # order_info['express'] = 1

    # json = {"goods_ids":goods_id,
    #         "addr_id":0,
    #         "express":3,
    #         "express_chd":0,
    #         "payment_id":1,
    #         "pay_pwd":"246810",
    #         "express_fee":0,
    #         "insure_price":0,
    #         "insure_fee":0,
    #         "appointment":'2021-10-21',
    #         "total":40,
    #         "order_model":10,
    #         "coupon":"[]",
    #         "AppFrom": "pc"}
    # print(json)

    r = requests.request('post', url=url, json=order_info, headers=headers)
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
def refund_goods(order_id):
    '''查找订单包含的拍品，商品'''
    '''{"status":200,"msg":"操作成功","data":[{"goods_id":2334,"name":"退化退款测试-13"},{"goods_id":2335,"name":"退化退款测试-14"}],"shop_switch":"0"}'''
    url = base_url + '/admin/order/refund_goods'
    headers = admin_headers
    json = {"order_id": order_id}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def refund(**info):
    '''售后-仅退款'''
    '''{"status":200,"msg":"操作成功","data":null,"shop_switch":"0"}'''
    url = base_url +'/admin/order/refund'
    headers = admin_headers

    refund_info = {"order_id":1450,
            "type":1,
            "refund_desc":"退化退款测试-8 退款",
            "refund_money":"20",
            "goods_id":"[2328]"}

    for key in info:
        if key in refund_info.keys():
            refund_info[key] = info[key]
    r = requests.request('post', url=url, json=refund_info, headers=headers)
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
def calculate_freight(token=None,**info):
    '''计算运费'''
    url = base_url + '/user/delivery/calculate_freight'
    if token:
        update_token(token)
    headers = get_user_headers()
    delivery_info = {
        "user_addr_id": 193,
        "goods": "[{\"goods_id\":2419,\"buy_number\":1}]"
    }
    for key in info:
        if key in delivery_info.keys():
            delivery_info[key] = info[key]
    r = requests.request('post', url=url, json=delivery_info, headers=headers)
    return r

def confirm_send(order_id, token=None):
    '''用户确认收货'''
    url = base_url + '/user/order/confirm_send'
    if token:
        update_token(token)
    headers = get_user_headers()
    #json = {"order_id":1502}
    json = {"order_id": order_id}
    print(json)
    r = requests.request('post', url=url, json=json, headers=headers)
    return r


def express_info(order_id, token=None):
    '''用户查看物流信息'''
    #{"order_id":"1502"}
    url = base_url + '/user/delivery/calculate_freight'
    if token:
        update_token(token)
    headers = get_user_headers()
    # json = {"order_id":1502}
    json = {"order_id": order_id}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def logistics_list(page=1,**orderinfo):
    '''物流列表'''
    url = base_url + '/admin/order/logistics_list'
    headers = admin_headers
    order_info = {"where":"[{\"key\":\"order_no\",\"value\":\"\"},{\"key\":\"goods_name\",\"value\":\"\"},{\"key\":\"userno\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"payment_id\",\"value\":\"\"},{\"key\":\"express_id\",\"value\":\"\"}]",
            "page":1,
            "type":2}
    search_info = {"order_no":"","goods_name":"","userno":"","status":"","payment_id":"","express_id":""}



    if orderinfo != {}:
        info_s = []
        info_r = "["
        for key in orderinfo:
            print(key)
            print(url)
            if key in search_info.keys():
                search_info[key] = orderinfo[key]
        search_str = utils.kwargs_to_str(**search_info)
        order_info["where"] = search_str
    if page !=1:
        order_info["page"] = page
    r = requests.request('post', url=url, json=order_info, headers=headers)
    return r
def list(page=1, **orderinfo):
    '''用户查看订单列表'''
    url = base_url + '/admin/order/list'
    headers = admin_headers
    order_info = {"page":1,
                  "type":1,
                  "where":"[{\"key\":\"order_no\",\"value\":\"\"},{\"key\":\"goods_name\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"userno\",\"value\":\"\"},{\"key\":\"payment_id\",\"value\":\"\"},{\"key\":\"express_id\",\"value\":\"\"},{\"key\":\"id\",\"value\":\"\"},{\"key\":\"start_time\",\"value\":\"\"},{\"key\":\"end_time\",\"value\":\"\"}]"}
    search_info = {"order_no": "", "goods_name": "", "userno": "", "status": "", "payment_id": "", "express_id": "","start_time":"","end_time":"","id":""}

    if orderinfo != {}:
        for key in orderinfo:
            print(key)
            print(url)
            if key in search_info.keys():
                search_info[key] = orderinfo[key]
        search_str = utils.kwargs_to_str(**search_info)
        order_info["where"] = search_str
    if page != 1:
        order_info["page"] = page
    r = requests.request('post', url=url, json=order_info, headers=headers)

    return r




