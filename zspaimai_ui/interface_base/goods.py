import requests
import time
from utils import rwjson, rwcfg, utils
from interface_base.user import update_token, get_user_headers,base_url,admin_headers




def goods_list(**goods_info):
    '''后台拍品列表'''
    url = base_url + '/admin/goods/goods_list'
    headers = admin_headers
    info = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"category_id\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"},{\"key\":\"type\",\"value\":1}]","page":1,"admin_name":"","topic_id":""}
    search_info ={"name":"", "category_id":"", "status":"", "is_shelves": "", "top": "", "is_recommended": "", "type": ""}
    if goods_info !={}:
        for key in goods_info:
            if key in search_info:
                search_info[key] = goods_info[key]
        search_str = utils.kwargs_to_str(**search_info)
        info["where"] = search_str


    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def bidding(token=None, **bidinfo):
    '''用户竞买拍品'''
    if token:
        update_token(token)
    url = base_url + '/user/user/bid'
    json = {"goods_id": 2391,
            "price": 1000
            }
    for key in bidinfo:
        if key in json.keys():
            json[key] = bidinfo[key]

    headers = get_user_headers()
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()
def user_bid(token=None):
    '''获取用户的中标记录'''
    url = base_url + '/user/goods/user_bid'
    if token:
        update_token(token)
    headers = get_user_headers()
    json = {"page":1,"act":"finish"}
    r = requests.request('post', url=url, json=json, headers=headers)
    return r.json()

def goods_add(**good_infos):
    '''后台添加拍品'''
    url = base_url + '/admin/goods/goods_add'
    headers = admin_headers
    goods_info_real = rwjson.RwJson().readjson('interface_data', 'goods.json')
    if good_infos != {}:
        for key in good_infos:
            if key in goods_info_real.keys():
                goods_info_real[key] = good_infos[key]
    r = requests.request('post', url=url, json=goods_info_real, headers=headers)

    return r