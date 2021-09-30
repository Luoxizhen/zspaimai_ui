import requests
def add_goods():
    '''后台添加拍品'''
    url = 'http://api.online.zspaimai.cn/admin/goods/goods_add'
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http://home.online.zspaimai.cn/',
               'AdminToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ5eWxBZG1pbiIsImlhdCI6MTYyNzAwNDc0OCwibmJmIjoxNjI3MDA0NzQ4LCJleHAiOjE2MjcwNDc5NDgsImRhdGEiOnsiYWRtaW5fdXNlcl9pZCI6MiwibG9naW5fdGltZSI6IjIwMjEtMDctMjMgMDk6NDU6NDgiLCJsb2dpbl9pcCI6IjE3Mi4xOS4wLjQifX0.KQfyTIx3MSRafMvKthxG-9yoQaMRaDLMA1gAYxtEOGo',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    json = {"category_id": 35,
            "platform": "1",
            "begin_time": {{begin_time}},
            "end_time": {{end_time}},
            "top_price": "",
            "name": "中标测试-{{$randomInt}}",
            "delay_time": 60,
            "shape": "98",
            "price": "10",
            "retain_price": "",
            "seller_name": "大罗",
            "agreement_no": "123",
            "create_user": "",
            "create_date": "",
            "content": "<p>我的竞买流程测试</p>",
            "original_image": "[\"picture/YTfwFGWFEhDZrHf4GBX3fKdE27kJzn.png\"]",
            "images": "[\"thumbnail/54pNBGaXPzYcwNpW8pk56JGSyC63k4.png\"]",
            "freight_id": 51,
            "is_freight": 0,
            "goods_weight": "",
            "buyer_service_rate": "8",
            "meta": "{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"0\",\"seller_insure_no_deal\":\"0\",\"service_fee_deal\":\"0\",\"service_fee_no_deal\":\"0\",\"production_fee_deal\":\"0\",\"production_fee_no_deal\":\"0\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}"
        }
    r = requests.request('post', url=url, json=json, headers=headers)
    goog_id = r.json()['data']
    # {
    #     "status": 200,
    #     "msg": "操作成功",
    #     "data": "1160"
    # }
    return r.json()
def bidding():
    url = 'http://api.online.zspaimai.cn/user/user/bid'
    json ={"goods_id": {{good_id}},
             "price": {{price}} }
    headers = {"Content-Type": "application/json; charset=utf-8",
               'Connection': 'keep-alive',
               'host': 'api.online.zspaimai.cn',
               'Origin': 'http://home.online.zspaimai.cn',
               'Referer': 'http://home.online.zspaimai.cn/',
               'token': token,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
               }
    r = requests.request('post', url=url, json=json, headers=headers)