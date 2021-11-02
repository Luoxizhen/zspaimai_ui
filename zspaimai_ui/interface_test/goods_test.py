from interface_base import goods
import pytest
import time
from utils import utils
def test_goods_add():
    begin_time = round(time.time())+120
    end_time = begin_time + 600
    #name = '1960年第三版人民币壹圆拖拉机狮子号一枚-退货退款-3'
    # a = time.strptime('2021-11-2 14:20:00', '%Y-%m-%d %H:%M:%S')
    # b = time.strptime('2021-11-2 14:23:00', '%Y-%m-%d %H:%M:%S')

    # begin_time = time.mktime(a)
    # end_time = time.mktime(b)
    name = '订阅信息验证-6'

    good_info = {"name": name, "begin_time": int(begin_time), "end_time": int(end_time)}
    r = goods.goods_add(**good_info)

    status = r.json()['status']
    assert status == 200
def test_goods_list():
    r = goods.goods_list()
    assert r['status'] == 200


def test_goods_add_001():
    begin_time = round(time.time())
    end_time = begin_time + 6000
    good_infos = {"begin_time": begin_time, "end_time": end_time, "name": "拍品删除测试", "price": 10}
    #good_infos={"type":2,"inventory":"1000","inventory_unit":"套","category_id":9,"platform":"1","begin_time":0,"end_time":0,"top_price":"","name":"第三套人民币7 枚1-2","delay_time":0,"shape":"100","price":"100","retain_price":"","seller_name":"","agreement_no":"","create_user":"","create_date":"","content":"<p>第三套人民币小全套7枚一枚(同分 PMG68E)</p>","original_image":"[\"picture/hPRswrxWWys8wDG7DzRK47GN4b33RK.jpeg\"]","images":"[\"thumbnail/aRFBN6MXYbrsrmF2KHKNZx8ZdATwRC.jpeg\"]","freight_id":51,"is_freight":0,"goods_weight":"","buyer_service_rate":"10","meta":"{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"1\",\"seller_insure_no_deal\":\"1\",\"service_fee_deal\":\"2\",\"service_fee_no_deal\":\"1\",\"production_fee_deal\":\"15\",\"production_fee_no_deal\":\"15\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}"}
    r = goods.goods_add(**good_infos)
    assert r.json()['status']==200

def test_goods_list():
    goods_info = {"status": 31}
    r = goods.goods_list(**goods_info)
    assert r.json()['data']['status'] == 200

def test_batch_shelves():
    goods_ids = []
    goods_info = {"status": 31, "is_shelves": 1}
    r = goods.goods_list(**goods_info).json()
    total = r['data']['total']
    per_page = r['data']['per_page']
    last_page = r['data']['last_page']
    for i in range(2):
        if last_page > 1 and i < last_page - 1:
            page_total = 10
        else:
            page_total = total - per_page * (last_page - 1)
        for j in range(page_total):
            goods_id = goods.goods_list(page=i, **goods_info).json()['data']['data'][j]['id']
            goods_ids.append(goods_id)
    goods_ids_str =str(goods_ids)
    batch_info = {"goods_ids": goods_ids_str, "is_shelves":0}
    print (batch_info)
    goods.batch_shelves(**batch_info)
    # goods.del_goods()
    assert 1 == 2

def test_batch_shelves_1():
    for k in range(9):
        goods_ids = []
        goods_info = {"status": 31, "is_shelves": 1}
        r = goods.goods_list(**goods_info).json()
        for i in range(10):
            goods_id = r['data']['data'][i]['id']
            goods_ids.append(goods_id)

        batch_info = {"goods_ids": str(goods_ids), "is_shelves": 0}
        # print(batch_info)
        goods.batch_shelves(**batch_info)
def test_goods_del():
    for k in range(109):
        goods_ids = []
        goods_info = {"status": 31, "is_shelves": 0,"top":0, "type":1, "is_recommended":0}
        r = goods.goods_list(**goods_info).json()
        for i in range(10):
            goods_id = r['data']['data'][i]['id']
            goods_ids.append(goods_id)
        batch_info = {"ids": str(goods_ids)}
        goods.del_goods(**batch_info)


def test_goods_recommended_del():
    '''将流拍的拍品取消推荐、取消置顶后删除'''
    goods_info = {"status": 31, "is_shelves":0, "type":1}
    r = goods.goods_list(**goods_info).json()
    goods_ids = []

    for i in range(r['data']['total']):
        good_id = r['data']['data'][i]['id']
        goods_ids.append(good_id)
        if r['data']['data'][i]["is_recommended"] == 1:
            act_info = {"id": good_id, "act": "is_recommended", "is_recommended": 0}
            goods.goods_edit_action(**act_info)
        if r['data']['data'][i]["top"] == 1:
            act_info = {"id": good_id, "act": "top", "top": 0}
            goods.goods_edit_action(**act_info)
    goods_info = {"ids": str(goods_ids)}
    goods.del_goods(**goods_info)

# def test_goods_delete():
#     for i in range(11,111):
#         r = goods.goods_list(i).json()
#         goods_ids = []
#         for j in range(10):
#             good_id = r['data']['data'][j]['id']
#             goods_ids.append(good_id)
#             if r['data']['data'][j][]

