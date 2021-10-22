from interface_base import goods
import pytest
import time
def test_goods_add():
    begin_time = round(time.time())
    end_time = begin_time + 60
    #name = '1960年第三版人民币壹圆拖拉机狮子号一枚-退货退款-3'
    name = '退货退款-5'
    r = goods.goods_add(begin_time, end_time, name)
    print(r)
    status = r['status']
    assert status == 200
def test_goods_list():

    r = goods.goods_list()
    assert r['status'] == 200


def test_goods_add_001():
    begin_time = round(time.time())
    end_time = begin_time + 30
    good_infos = {"begin_time": begin_time, "end_time": end_time, "name": "13111111111", "price": 20}
    print(good_infos)
    r = goods.goods_add(**good_infos)
    assert r.json()['status']==200