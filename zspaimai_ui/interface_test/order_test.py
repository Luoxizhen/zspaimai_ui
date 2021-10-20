import time
import pytest
from interface_base import goods, order, user
def test_order_coupon():
    begin_time = round(time.time())
    end_time = begin_time + 300
    goods_name = "完成订单支付测试"
    goods_id = goods.goods_add(begin_time, end_time, goods_name)['data']
    token = user.get_token()
    goods.updata_token(token)
    goods.bidding(goods_id, 10, token)
    time.sleep(300)
    order.get_bid_info(goods_id, token) #获取拍品的竞标信息
    order.recharge_list(token) #获取各种支付方式的手续费说明
    order.addr_list(token) #获取用户的地址
    order.express(token) #获取支付方式
    order.order_coupon(token, goods_id)
    assert 1==2
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



