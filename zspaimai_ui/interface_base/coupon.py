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
                     "send_time_e": ""}
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
