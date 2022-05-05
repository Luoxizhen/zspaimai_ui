import requests
from utils import rwcfg
from utils import util
from common.readconfig import ini
from common.rwjson import rwjson
from interface_base.headers import admin_headers,base_url,get_user_headers,get_user_headers_unlogin,update_token



def login(**userinfo):
    '''获取用户的token '''
    url = base_url+"/user/user/login?from=pc"
    headers = get_user_headers_unlogin()
    json = {"phone": "15622145010",
            "pwd": "123456"}
    for key in userinfo:
        if key in json.keys():
            json[key] = userinfo[key]
    r = requests.request('post', url=url, json=json, headers=headers)
    return r
def user_login(**userinfo):
    '''获取用户登陆后的token'''
    r = login(**userinfo)
    token = update_token(r.json()['data']['token'])
    return token
def get_token(phone):
    '''快捷登陆获取token'''
    get_msg(phone=phone)
    r = quick_login(phone)
    return r.json()['data']['token']

def get_msg(token=None, phone = '15622145010'):
    '''发送短信验证码'''
    url = base_url + '/user/user/msg'
    if token:
        update_token(token)
        headers = get_user_headers()
    else:
        headers = get_user_headers_unlogin()
    data = {"phone": phone}
    r = requests.request('post', url=url,  json=data, headers=headers)

def quick_login(phone):
    '''快捷登陆，该接口调用前先调用get_msg 接口发送验证码'''
    url = base_url + '/user/user/quick_login'
    headers = get_user_headers_unlogin()
    data = {"phone": phone, "vcode": "123456", "inv":""}

    r = requests.request('post', url=url, json=data, headers=headers)
    return r

def quick_login_union(inv, phone):
    url = base_url + '/user/user/quick_login'
    headers = get_user_headers_unlogin()
    data = {"phone": phone, "vcode": "123456", "inv": inv}
    r = requests.request('post', url=url, json=data, headers=headers)
    return r



def verify(phone, token=None):
    '''修改短信的时候，发送短信校验码
    接口输出：
     {
        "status": 200,
        "msg": "操作成功",
        "data": {
            "user_code": "eceb1edcdd191546d8877403aeae23e3"
        },
        "shop_switch": "0"
    }
    '''
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

def add_pwd(user_code, new_pwd=None):
    '''用户设置密码
    接口输出：
    {
        "status": 200,
        "msg": "设置成功",
        "data": [],
        "shop_switch": "0"
    }
    '''
    url = base_url + '/user/user/add_pwd'
    headers = get_user_headers()

    new_pwd = "246810"if new_pwd is None else new_pwd

    json = {
        "user_code": user_code,
        "new_pwd": new_pwd
    }
    r = requests.request('post', url=url, json=json, headers=headers)
    return r


def add_addr(token=None, **addr):
    """增加收获地址"""
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
    '''前台获取用户地址列表
    返回r
    {"status":200,"msg":"操作成功","data":[{"id":192,"name":"大罗","phone":"15622145020","address":"珠江嘉苑","zipcode":"","province":19,"city":289,"county":3040,"is_default":1,"area":"广东省,广州市,天河区","province_name":"广东省","city_name":"广州市","county_name":"天河区"}],"shop_switch":"0"}
    '''
    url = base_url + '/user/addr/list'
    if token:
        update_token(token)
    headers = get_user_headers()
    r = requests.request('get', url=url, headers=headers)

    return r
def list(page=1,**user_info):
    '''后台获取用户列表'''
    url = base_url + '/admin/user/list'
    headers = admin_headers
    list_info = {"where":"[{\"key\":\"userno\",\"value\":\"\"},{\"key\":\"phone\",\"value\":\"\"},{\"key\":\"is_mobile\",\"value\":\"\"},{\"key\":\"is_real\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_robot\",\"value\":\"\"}]","page":1}

    if page:
        list_info['page'] = page
    if user_info != {}:
        user_infos = util.str_to_dict(list_info["where"])
        for key in user_info:
            if key in user_infos.keys():
                user_infos[key] = user_info[key]
        ui = util.kwargs_to_str(**user_infos)
        list_info["where"] = ui

    r = requests.request('post', url=url, json=list_info, headers=headers)
    return r
def info(user_id):
    '''后台获取用户信息'''
    url = base_url + '/admin/user/info'
    headers = admin_headers
    user_info = {"user_id":user_id}
    r = requests.request('post', url=url, json=user_info, headers=headers)
    return r
def nickname_add(**info):
    '''新增昵称'''
    url = base_url + "/user/nickname/add"
    headers = get_user_headers()
    # info = {"nickname":"宝黛","id":""}
    r = requests.request('post',url=url, json=info, headers=headers)
    return r
def nickname_set(**info):
    '''设置默认昵称'''
    url = base_url +"/user/nickname/set"
    headers = get_user_headers()
    #{"id":1442}
    r = requests.request('post',url=url,json=info,headers=headers)
    return r
def nickname_edit(**info):
    '''修改昵称'''
    url = base_url + "/user/nickname/edit"
    headers = get_user_headers()
    # {"nickname":"大雁","id":882}
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def nickname_list():
    '''获取昵称列表'''
    url = base_url + "/user/nickname/list"
    headers = get_user_headers()
    # {"nickname":"大雁","id":882}
    r = requests.request('get', url=url, headers=headers)
    return r
def bid(**info):
    '''用户竞价'''
    url = base_url + "/user/user/bid"
    #{"goods_id":"1901","price":52}
    headers = get_user_headers()
    r = requests.request('post', url=url, json=info, headers=headers)
    return r

