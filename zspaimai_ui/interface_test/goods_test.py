from interface_base import goods
import pytest
import time
from utils import utils
def test_goods_add():
    begin_time = round(time.time())
    end_time = begin_time + 30
    #name = '1960年第三版人民币壹圆拖拉机狮子号一枚-退货退款-3'
    name = '支付'
    r = goods.goods_add(begin_time, end_time, name)
    print(r)
    status = r['status']
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
    for i in range(last_page):
        if last_page > 1 and i < last_page - 1:
            page_total = 10
        else:
            page_total = total - per_page * (last_page - 1)
        for j in range(page_total):
            goods_id = goods.goods_list(page=i, **goods_info).json()['data']['data'][j]
            goods_ids.append(goods_id)
    goods_ids_str = utils.object_to_str(*goods_ids)
    batch_info = {"goods_ids": goods_ids_str, "is_shelves":0}
    goods.batch_shelves(**batch_info)

