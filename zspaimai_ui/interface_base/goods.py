import requests
import time
from utils import  rwcfg, util
from common.rwjson import rwjson
from interface_base.headers import admin_headers,base_url,get_user_headers,update_token


def goods_list(page=1,**goods_info):
    '''后台拍品列表
    返回结果
    {"status":200,"msg":"操作成功","data":{"total":2235,"per_page":10,"current_page":1,"last_page":224,
    "data":[{"id":4136,"is_recommended":0,"type":1,"inventory":0,"freight_id":51,"name":"第一套人民币5元牧羊票样一枚(03891 8品)","category_id":3,"price":"1.00","retain_price":"0.00","top_price":"0.00","begin_time":1643338800,
    "end_time":1644496140,"delay_time":60,"platform":1,"shape":" 8品","status":10,"is_shelves":1,"top":0,"admin_id":2,"admin_name":"yylAdmin","create_time":"2022-01-25 15:16:48","category_name":"新中国纸钞","delivery_mode":"1","topic_title":"预展验证"},{"id":4135,"is_recommended":0,"type":1,"inventory":0,"freight_id":51,
    "name":"第一套人民币5000元耕地与工厂一枚(312-19084174 PMG 58)","category_id":3,"price":"1.00","retain_price":"0.00","top_price":"0.00","begin_time":1643338800,"end_time":1644496110,"delay_time":60,"platform":1,"shape":" 评级币","status":10,"is_shelves":1,"top":0,"admin_id":2,"admin_name":"yylAdmin",
    "create_time":"2022-01-25 15:16:48","category_name":"新中国纸钞","delivery_mode":"1","topic_title":"预展验证"},{"id":4134,"is_recommended":0,"type":1,"inventory":0,"freight_id":51,"name":"第一套人民币5元织布一枚(123-11794032 PMG40E)","category_id":3,"price":"1.00","retain_price":"0.00","top_price":"0.00",
    "begin_time":1643338800,"end_time":1644496080,"delay_time":60,"platform":1,"shape":" 评级币","status":10,"is_shelves":1,"top":0,"admin_id":2,"admin_name":"yylAdmin","create_time":"2022-01-25 15:16:47","category_name":"新中国纸钞","delivery_mode":"1","topic_title":"预展验证"},......
    ]},
    "shop_switch":"0"}
    '''
    url = base_url + '/admin/goods/goods_list'
    headers = admin_headers
    info = {"where":"[{\"key\":\"name\",\"value\":\"\"},{\"key\":\"category_id\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_shelves\",\"value\":\"\"},{\"key\":\"top\",\"value\":\"\"},{\"key\":\"is_recommended\",\"value\":\"\"},{\"key\":\"type\",\"value\":1}]","page":1,"admin_name":"","topic_id":""}
    search_info ={"name":"", "category_id":"", "status":"", "is_shelves": "", "top": "", "is_recommended": "", "type": "1"}
    search_info.update(goods_info)
    search_str = util.kwargs_to_str(**search_info)
    info["where"] = search_str
    if page != 1:
        info["page"] = page
    r = requests.request('post', url=url, json=info, headers=headers)
    return r
def bidding(token=None,header=None, **bidinfo):
    '''用户竞买拍品,
    token ： 不同用户竞拍
    header: 不同平台竞拍
    传入不同token 及不同 header 可以实现不同用户及不同平台的竞拍'''
    if token:
        update_token(token)
    url = base_url + '/user/user/bid'
    json = {"goods_id": 2391,
            "price": 1000
            }
    json.update(bidinfo)

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
    goods_info_real = rwjson.get_json('goods.json')
    goods_info_real.update(good_infos)
    r = requests.request('post', url=url, json=goods_info_real, headers=headers)
    return r

def batch_shelves(**goods_infos):
    '''后台批量上下架拍品'''
    url = base_url + '/admin/goods/batch_shelves'
    headers = admin_headers
    info = {"goods_ids":"[2613,2601,2593,2592,2530,2529,2528,2527,2526,2525]", "is_shelves":0}
    info.update(goods_info)
    r = requests.request('post', url=url, json=info, headers=headers)

    return r

def del_goods(**goods_infos):
    '''后台批量上下架拍品
    info =
    {"ids":
    "[2458,2457,2456,2455,2454,2414,2397,2396,2387,2386,2613,2601,2593,2592,2590,2575,2574,2573,2569,2568]"}'''
    url = base_url + '/admin/goods/del_goods'
    headers = admin_headers
    r = requests.request('post', url=url, json=goods_infos, headers=headers)
    return r
def goods_edit_action(**act_infos):
    '''拍品操作- 置顶、推荐
    info =
    {"id":2567,"act":"is_recommended","value":0}    取消推荐
    {"id": 533, "act": "top", "value": 0} 取消指定
    '''
    url = base_url + '/admin/goods/goods_edit_action'
    headers = admin_headers
    r = requests.request('post', url=url, json=act_infos, headers=headers)
    return r
def goods_edit_shelves(**act_infos):
    '''拍品操作- 下架
    act_infos =
    {"id":2375,"is_shelves":0}'''
    url = base_url + '/admin/goods/goods_edit_shelves'
    headers = admin_headers
    r = requests.request('post', url=url, json=act_infos, headers=headers)
    return r
def goods_info(**info):
    '''获取拍品的信息
    info = {"id":2624}
    返回的拍品信息内容如下：
    data: {id: 2799, category_id: 3, name: "拍品666", simple_desc: "", seller_name: "大罗", agreement_no: "a0000152",…}
    access_count: 0
    admin_id: 2
    admin_name: "yylAdmin"
    agreement_no: "a0000152"
    begin_time: 1637643600
    bid_count: 1
    buyer_service_rate: "10"
    category_id: 3
    content: "<p>1960年第三版人民币壹圆拖拉机狮子号一枚</p>"
    create_date: ""
    create_time: "2021-11-19 10:20:17"
    create_user: ""
    delay_time: 0
    delete_time: 0
    end_time: 1637960400
    freight_id: 51
    goods_weight: "0.000"
    id: 2799
    images: ["thumbnail/fjZac4eFCsxk2Py2z4BiQ4N4fbbC6x.png"]
    0: "thumbnail/fjZac4eFCsxk2Py2z4BiQ4N4fbbC6x.png"
    inventory: 0
    inventory_unit: ""
    is_recommended: 1
    is_shelves: 0
    meta: "{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"1\",\"seller_insure_no_deal\":\"1\",\"service_fee_deal\":\"2\",\"service_fee_no_deal\":\"1\",\"production_fee_deal\":\"15\",\"production_fee_no_deal\":\"15\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}"
    name: "拍品666"
    now_price: "10.00"
    original_image: ["picture/wxTj7wm3XN2JkhFZXQCSpiRKRhZx5C.jpeg"]
    original_price: "0.00"
    platform: 1
    price: "10.00"
    retain_price: "0.00"
    sales_count: 0
    seller_name: "大罗"
    seo_desc: ""
    seo_keywords: ""
    seo_title: ""
    shape: "100"
    show_verify: 2
    simple_desc: ""
    spec_base: null
    status: 10
    top: 0
    top_price: "0.00"
    topic_id: [2, 2, 181, 2, 2, 2, 2, 162, 2, 2, 2, 164]
    0: 2
    1: 2
    2: 181
    3: 2
    4: 2
    5: 2
    6: 2
    7: 162
    8: 2
    9: 2
    10: 2
    11: 164
    type: 1
    update_time: "2021-11-25 17:13:53"
    msg: "操作成功"
    shop_switch: "0"
    status: 200
    '''
    url = base_url + '/admin/goods/goods_info'
    headers = admin_headers
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

    info.update(goods_info)
    r = requests.request('post', url=url, json=info, headers=headers)
    return r

# def list(**list_info):
#     '''前端获取商品列表'''
#     url = base_url + '/user/goods/list'
#     headers = mini_headers
#     # data = "category_id=0&page=2&sort=default&type=2"
#     data = {"category_id":0,
#             "page":1,
#             "sort":"default",
#             "type":2}
#     for key in list_info:
#         if key in data.keys():
#             data[key] = list_info[key]
#     r = requests.request('post', url=url, data=data, headers=headers)
#     return r
# def detail(id):
#     '''前端获取商品详情'''
#     url = base_url + '/user/goods/detail?id=1634'
#     headers = mini_headers
#     data = {"id":id}
#     r = requests.request('get', url=url, data=data, headers=headers)
#     return r
# def add(goods_id, number=1):
#     '''前端添加商品到购物车'''
#     url = base_url + '/user/cart/add'
#     headers = mini_headers
#     # data = "goods_id=1634&goods_number=1"
#     data = {"goods_id": goods_id,"goods_number":number}
#     r = requests.request('post', url=url, data=data, headers=headers)
#     return r
def goods_bid(good_id,page=1):
    '''获取拍品出价信息'''
    url = base_url + '/admin/goods/goods_bid'
    headers = admin_headers

    data = {"id":good_id,"page":page}

    r = requests.request('post', url=url, json=data, headers=headers)
    return r
if __name__ == "__main__":
    print(base_url)
    print(admin_headers)