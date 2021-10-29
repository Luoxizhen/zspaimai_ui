from interface_base.user import update_token, get_user_headers,base_url,admin_headers
import requests
from utils import utils
def list(page=1,**searchinfo):
    '''后台获取优惠劵列表'''
    url = base_url + '/admin/coupon/list'
    headers = admin_headers
    search_info = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"coupon_type\",\"value\":\"\"},{\"key\":\"start_time\",\"value\":\"\"},{\"key\":\"end_time\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"}]",
                   "page":1}
    search_kwargs = {"name": "",
                     "coupon_type": "",
                     "start_time": "",
                     "end_time": "",
                     "status": "",
                     "send_time_s": "",
                     "send_time_e": "",
                     "is_enable": ""}
    if searchinfo != {}:
        for key in searchinfo:
            if key in search_kwargs:
                search_kwargs[key] = searchinfo[key]
    search_str = utils.kwargs_to_str(**search_kwargs)
    search_info["where"] = search_str
    if page > 1:
        search_info["page"] = page

    r = requests.request('post', url=url, json=search_info, headers=headers)
    return r

def edit_action(**action):
    '''后台操作'''
    url = base_url + '/admin/coupon/edit_action'
    headers = admin_headers
    info = {"id": 56, "is_enable": 2}
    if action != {}:
        for key in action:
            if key in info.keys():
                info[key] = action[key]
    r = requests.request('post', url=url, json=info, headers=headers)

    return r
def edit_action(**action):
    '''后台操作'''
    url = base_url + '/admin/coupon/edit_action'
    headers = admin_headers
    info = {"id": 56, "is_enable": 2}
    if action != {}:
        for key in action:
            if key in info.keys():
                info[key] = action[key]
    r = requests.request('post', url=url, json=info, headers=headers)

    return r

def add(**cp_info):
    '''后台操作'''
    url = base_url + '/admin/coupon/add'
    headers = admin_headers
    info = {"name":"满30000减388优惠券",
            "amount":200,
            "coupon_type":10,
            "using_threshold":30000,
            "coupon_content":388,
            "platform":0,
            "range":10,
            "range_list":"",
            "send_time_s":1635487200,
            "send_time_e":1637078400,
            "vali_type":2,
            "vali_day":0,
            "start_time":1635487200,
            "end_time":1636905600,
            "user_type":1,
            "num":0,
            "use_restrictions":2,
            "remind":0,
            "desc":"优惠劵信息",
            "discount":0,
            "money":0}
    if cp_info != {}:
        for key in cp_info:
            if key in info.keys():
                info[key] = cp_info[key]
    r = requests.request('post', url=url, json=info, headers=headers)

    return r