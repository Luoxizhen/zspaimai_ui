import requests
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
