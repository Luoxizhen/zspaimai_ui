import requests
from utils import rwjson, rwcfg

admin_headers = rwjson.RwJson().readjson('interface_data', 'admin_headers.json')
base_url = "http://api.online.zspaimai.cn"

def get_user_headers():
    return rwjson.RwJson().readjson('interface_data', 'user_headers.json')
def get_user_headers_unlogin():
    return rwjson.RwJson().readjson('interface_data', 'user_headers_unlogin.json')
def get_token(**userinfo):
    '''获取用户的token '''
    url = base_url+"/user/user/login?from=pc"
    headers = get_user_headers_unlogin()
    json = {"phone": "15622145010",
            "pwd": "123456"}
    for key in userinfo:
        if key in json.keys():
            json[key] = userinfo[key]

    r = requests.request('post', url=url, json=json, headers=headers)
    # if r.json()['status']==200:
    #     return r.json()['data']['token']
    return r

def update_token(token):
    dict = rwjson.RwJson().readjson('interface_data', 'user_headers.json')
    dict["token"] = token
    rwjson.RwJson().writejson('interface_data', 'user_headers.json', dict)

def get_token(phone):
    # 快捷登陆获取token
    get_msg(phone=phone)
    r = quick_login(phone)
    return r.json()['data']['token']

def get_msg(token=None, phone = '15622145010'):
    # 发送短信验证码
    url = base_url + '/user/user/msg'
    if token:
        update_token(token)
        headers = get_user_headers()
    else:
        headers = get_user_headers_unlogin()
    data = {"phone": phone}
    r = requests.request('post', url=url,  json=data, headers=headers)
    print(r.json())
def quick_login(phone):
    # 快捷登陆，该接口调用前先调用get_msg 接口发送验证码
    url = base_url + '/user/user/quick_login'
    headers = get_user_headers_unlogin()
    data = {"phone": phone, "vcode": "123456"}
    r = requests.request('post', url=url, json=data, headers=headers)
    #token = r.json()['data']['token']
    #userno = r.json()['data']['userno']
    print(r.json())
    return r
# def get_msg_union(inv, phone):
#     url = base_url + '/user/user/msg'
#     headers = get_user_headers()
#     data = {"phone": phone, "from": "pc", "inv": inv}
#     r = requests.request('post', url=url,  json=data, headers=headers)
def quick_login_union(inv, phone):
    url = base_url + '/user/user/quick_login'
    headers = get_user_headers_unlogin()
    data = {"phone": phone, "vcode": "123456", "inv": inv}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r



def verify(phone, token=None):
    '''修改短信的时候，发送短信校验码'''
    url = base_url + '/user/user/verify'
    if token:
        update_token(token)
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
def add_pwd(user_code, new_pwd=None):
    '''用户设置密码'''
    url = base_url + '/user/user/add_pwd'
    headers = get_user_headers()

    new_pwd = "246810"if new_pwd is None else new_pwd

    json = {
        "user_code": user_code,
        "new_pwd": new_pwd
    }
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
    # {
    #     "status": 200,
    #     "msg": "设置成功",
    #     "data": [],
    #     "shop_switch": "0"
    # }

def add_addr(token=None, **addr):
    url = base_url + '/user/addr/add'
    if token:
        update_token(token)
    headers = get_user_headers()
    addr_info = {"id":"","name":"大罗","phone":"15622145020","address":"珠江嘉苑","zipcode":"","province":19,"city":289,"county":3040,"is_default":1}
    for key in addr:
        if key in addr_info.keys():
            addr_info[key] = addr[key]
    r = requests.request('post', url=url, json=addr_info, headers=headers)
    return r

def addr_list(token=None):
    url = base_url + '/user/addr/list'
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, headers=headers)
    #{"status":200,"msg":"操作成功","data":[{"id":192,"name":"大罗","phone":"15622145020","address":"珠江嘉苑","zipcode":"","province":19,"city":289,"county":3040,"is_default":1,"area":"广东省,广州市,天河区","province_name":"广东省","city_name":"广州市","county_name":"天河区"}],"shop_switch":"0"}
    return r