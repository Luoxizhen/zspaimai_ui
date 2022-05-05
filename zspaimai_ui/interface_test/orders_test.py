import json

from interface_base import order

from utils import times

import csv

def test_get_order_list():
    order_list_info = {"status":"5","express_id":3} # 快递到付1，已完成，上门自提3，快递2

    r = order.list(page=1,**order_list_info)
    page_num = r.json()["data"]["last_page"] #总页数
    orders_infos = [] #保存订单的基本信息
    for i in range(page_num):

        order_info_this_list = order.list(page=i+1,**order_list_info).json()['data']['data']
        for j in range(len(order_info_this_list)):

            orders_infos.append(order_info_this_list[j])

    file_path = "/Users/yuanyuanhe/Desktop/货/成交记录/成交表_上门自提.csv"
    with open(file_path,'w') as f:
        fileheader = ["id","user_id","pay_time","status","pay_status","express_id","express_number","order_no","phone","userno","goods_count"]
        csv_writer = csv.DictWriter(f,fileheader)
        csv_writer.writeheader()

        csv_writer.writerows(orders_infos)

    assert 1 == 2


def test_get_order_detail():
    '''获取订单详情并保存到指定地址'''
    file_path = "/Users/yuanyuanhe/Desktop/货/成交记录/成交表.csv"
    file_path_output = "/Users/yuanyuanhe/Desktop/货/成交记录/成交表详情_快递到付.csv" # 订单详情输出地址
    order_ids = [] # 保存所查询到订单id
    order_infos = [] # 保存订单详细信息
    with open(file_path,'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            order_ids.append(row['id'])
        print(order_ids)
    for order_id in order_ids:
        order_info = order.order_info(order_id).json()['data']
        goods_detail = order_info['goods_detail']
        for i in range(len(goods_detail)):
            good_detail = goods_detail[i]
            good_detail['id'] = order_info['id']
            good_detail['u_phone']= order_info['phone']
            good_detail['user_name'] = order_info['address']['name']
            good_detail['phone'] = order_info['address']['phone']
            good_detail['address'] = order_info['address']['province_name'] + order_info['address']['city_name'] +order_info['address']['county_name']+order_info['address']['address']
            order_infos.append(good_detail)
            del(good_detail['refund_num'])
            del (good_detail['refund_status'])
            del (good_detail['refund_price'])

    with open(file_path_output, 'w') as f:
        fileheader = ["id","goods_id","name","num","total_price","buyer_service_price","total_coupon","price","u_phone","user_name","phone","address"]
        csv_writer = csv.DictWriter(f, fileheader)
        csv_writer.writeheader()
        csv_writer.writerows(order_infos)
    assert 1==2













