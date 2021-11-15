import requests
import time
from utils import rwjson, rwcfg, util
from interface_base.user import update_token, get_user_headers,base_url,admin_headers,mini_headers

def add():
    '''前端添加商品到购物车'''
    url = base_url + '/user/cart/add'
    headers = mini_headers
    data = "goods_id=1634&goods_number=1"
    r = requests.request('post', url=url, data=data, headers=headers)
    return r
def list():
    '''购物车列表'''
    url = base_url + '/user/cart/list'
    headers = mini_headers
    data = "page=1"
    r = requests.request('get', url=url, data=data, headers=headers)
    return r