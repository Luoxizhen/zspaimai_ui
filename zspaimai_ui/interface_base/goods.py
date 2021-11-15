import requests
import time
from utils import rwjson, rwcfg, util
from interface_base.user import update_token, get_user_headers,base_url,admin_headers,mini_headers




def goods_list(page=1,**goods_info):
    '''后台拍品列表'''
    url = base_url + '/admin/goods/goods_list'
    headers = admin_headers
    info = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"category_id\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"},{\"key\":\"type\",\"value\":1}]","page":1,"admin_name":"","topic_id":""}
    search_info ={"name":"", "category_id":"", "status":"", "is_shelves": "", "top": "", "is_recommended": "", "type": "1"}
    if goods_info !={}:
        for key in goods_info:
            if key in search_info:
                search_info[key] = goods_info[key]
        search_str = util.kwargs_to_str(**search_info)
        info["where"] = search_str
    if page != 1:
        info["page"] = page


    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def bidding(token=None,header=None, **bidinfo):
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

    if header:
        headers = header
    else:
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

def batch_shelves(**goods_infos):
    '''后台批量上下架拍品'''
    url = base_url + '/admin/goods/batch_shelves'
    headers = admin_headers
    info = {"goods_ids":"[2613,2601,2593,2592,2530,2529,2528,2527,2526,2525]", "is_shelves":0}
    if goods_infos != {}:
        for key in goods_infos:
            if key in info.keys():
                info[key] = goods_infos[key]

    r = requests.request('post', url=url, json=info, headers=headers)

    return r

def del_goods(**goods_infos):
    '''后台批量上下架拍品'''
    url = base_url + '/admin/goods/del_goods'
    headers = admin_headers
    # info = {"ids":"[2458,2457,2456,2455,2454,2414,2397,2396,2387,2386,2613,2601,2593,2592,2590,2575,2574,2573,2569,2568]"}
    # if goods_infos != {}:
    #     for key in goods_infos:
    #         if key in info.keys():
    #             info[key] = goods_infos[key]

    r = requests.request('post', url=url, json=goods_infos, headers=headers)

    return r
def goods_edit_action(**act_infos):
    '''拍品操作- 下架、置顶、推荐'''
    url = base_url + '/admin/goods/goods_edit_action'
    headers = admin_headers
    # info = {"id":2567,"act":"is_recommended","value":0}
    # {"id": 533, "act": "top", "value": 0}
    r = requests.request('post', url=url, json=act_infos, headers=headers)

    return r
def goods_edit_shelves(**act_infos):
    '''拍品操作- 下架、置顶、推荐'''
    url = base_url + '/admin/goods/goods_edit_shelves'
    headers = admin_headers
    # info = {"id":2567,"act":"is_recommended","value":0}
    # {"id":2375,"is_shelves":0}
    r = requests.request('post', url=url, json=act_infos, headers=headers)
    return r
def goods_info(**info):
    '''获取拍品的信息'''
    url = base_url + '/admin/goods/goods_info'
    headers = admin_headers
    #info = {"id":2624}
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def goods_edit(**goods_info):
    '''编辑拍品'''
    url = base_url + '/admin/goods/goods_edit'
    headers = admin_headers
    info = {"topic_id":"[15]",
            "type":1,
            "id":2624,
            "category_id":3,
            "platform":"1",
            "begin_time":1635906328,
            "end_time":1635992730,
            "top_price":"0.00",
            "name":"优惠劵",
            "delay_time":0,
            "shape":"98",
            "price":"50000.00",
            "retain_price":"0.00",
            "seller_name":"大罗",
            "agreement_no":"a0000152",
            "create_user":"",
            "create_date":"",
            "freight_id":51,
            "is_freight":0,
            "goods_weight":"0.000",
            "buyer_service_rate":"10",
            "content":"<p>1960年第三版人民币壹圆拖拉机狮子号一枚</p>",
            "meta":"{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"1\",\"seller_insure_no_deal\":\"1\",\"service_fee_deal\":\"2\",\"service_fee_no_deal\":\"1\",\"production_fee_deal\":\"15\",\"production_fee_no_deal\":\"15\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}",
            "original_image":"[\"picture/wxTj7wm3XN2JkhFZXQCSpiRKRhZx5C.jpeg\"]",
            "images":"[\"thumbnail/fjZac4eFCsxk2Py2z4BiQ4N4fbbC6x.png\"]"}
    for key in goods_info:
        if key in info.keys():
            info[key] = goods_info[key]
    print(info)
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def list(**list_info):
    '''前端获取商品列表'''
    url = base_url + '/user/goods/list'
    headers = mini_headers
    # data = "category_id=0&page=2&sort=default&type=2"
    data = {"category_id":0,
            "page":1,
            "sort":"default",
            "type":2}
    for key in list_info:
        if key in data.keys():
            data[key] = list_info[key]
    r = requests.request('post', url=url, data=data, headers=headers)
    return r
def detail(id):
    '''前端获取商品详情'''
    url = base_url + '/user/goods/detail?id=1634'
    headers = mini_headers
    data = {"id":id}
    r = requests.request('get', url=url, data=data, headers=headers)
    return r
def add(goods_id, number=1):
    '''前端添加商品到购物车'''
    url = base_url + '/user/cart/add'
    headers = mini_headers
    # data = "goods_id=1634&goods_number=1"
    data = {"goods_id": goods_id,"goods_number":number}
    r = requests.request('post', url=url, data=data, headers=headers)
    return r