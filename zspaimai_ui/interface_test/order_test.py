import time
import pytest
from interface_base import goods, order, user
def test_order_coupon():
    begin_time = round(time.time())
    end_time = begin_time + 30
    goods_name = "退货退款测试-17"
    goods_id = goods.goods_add(begin_time, end_time, goods_name)['data']
    # token = user.get_token()
    # goods.updata_token(token)
    token = 'c42a217ca29950d478aec78c84f95f99'
    time.sleep(2)
    r =goods.bidding(goods_id, 10, token)
    # time.sleep(100)
    # order.get_bid_info(goods_id, token) #获取拍品的竞标信息
    # order.recharge_list(token) #获取各种支付方式的手续费说明
    # order.addr_list(token) #获取用户的地址
    # order.express(token) #获取支付方式
    # order.order_coupon(token, goods_id)
    assert r['status'] == 200
def test_get_bid_info():
    token = user.get_token()
    print(token)
    r = order.get_bid_info("2306", token)
    print(r)
    assert r['status'] == 200


def test_calculate_freight():
    token = user.get_token()
    r = order.calculate_freight(token)
    print(r)
    assert ['status'] == 300

def test_bidding():
    token = user.get_token()
    print(token)

    r = goods.bidding("2308", 12, token)
    print(r)
    assert r['status']==200


def test_add_order():
    begin_time = round(time.time())
    end_time = begin_time +30
    goods_name1 = "退款退货测试-30"
    goods_name2 = "退款退货测试-31"
    goods_id1 = goods.goods_add(begin_time, end_time, goods_name1)['data']
    goods_id2 = goods.goods_add(begin_time, end_time, goods_name2)['data']
    # token = user.get_token()
    # goods.updata_token(token)
    token = 'c42a217ca29950d478aec78c84f95f99'
    time.sleep(2)
    goods.bidding(goods_id1, 10, token)
    goods.bidding(goods_id2, 10, token)
    time.sleep(30)
    r1 = order.get_bid_info(goods_id1, token) #获取拍品的竞标信息
    r1 = order.get_bid_info(goods_id2, token)
    print("获取拍品的竞标信息")
    print(r1)
    r1 = order.recharge_list(token) #获取各种支付方式的手续费说明
    print("获取各种支付方式的手续费说明")
    print(r1)
    r1 = order.addr_list(token) #获取用户的地址
    print("获取用户的地址")
    print(r1.json())
    addr_id = r1.json()['data'][0]['id']

    r1 = order.express(token) #获取支付方式
    print("获取支付方式")
    print(r1.json())
    express_id = r1.json()['data'][0]['id']

    goods_id = "["+str(goods_id1)+","+str(goods_id2)+"]"
    r = order.add_order(token,str(goods_id),addr_id)
    print(r.json())
    assert r.json()['status'] == 200
def test_add_order1():
    '''下单'''
    pass

def test_take_delivery():
    order_id = 1452
    r = order.take_delivery(order_id)
    print(r)
    assert r['status'] == 200

def test_deliver():
    order_id = 1451
    r = order.deliver(order_id)
    print(r)
    assert r.json()['status'] == 200
def test_refund():
    r = order.refund()
    print(r)
    assert r.json()['status'] == 200
def test_confirm_order():
    r = order.confirm_order()
    assert r.json()['status'] == 200