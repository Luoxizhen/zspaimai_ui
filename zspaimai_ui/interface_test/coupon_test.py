import time

from interface_base import coupon
def test_list():
    '''测试获取优惠劵列表'''
    searchinfo = {"coupon_type": 10, "status": 2}
    r = coupon.list(**searchinfo)
    print(r.json())
    assert 1 == 2
def test_action():
    '''对后台所有已生效的红包优惠劵停用'''
    searchinfo = {"coupon_type": 10, "status": 2}
    r = coupon.list()
    total = r.json()['data']['total']
    page = r.json()['data']['last_page']
    per_page = r.json()['data']['per_page']

    for i in range(1, page+1):
        r = coupon.list(page=i)
        if i != page:
            j = per_page
        else:
            j = total - per_page * (page-1)
        for k in range(j):
            if r.json()['data']['data'][k]["is_enable"] == 1:
                id = r.json()['data']['data'][k]["id"]
                act_info = {"id": id, "is_enable": 2}
                coupon.edit_action(**act_info)

def test_action_disable():
    '''批量停用优惠劵'''
    searchinfo = {"is_enable": 1}
    r = coupon.list(**searchinfo)
    total = r.json()['data']['total']
    page = r.json()['data']['last_page']
    per_page = r.json()['data']['per_page']


    # for i in range(1, page + 1):
    #     r = coupon.list(page=i)
    #
    #     if i < page:
    #         j = per_page
    #     else:
    #         j = total - per_page * (page - 1)
    #     for k in range(j):
    #         act_info = {"id": id, "is_enable": 2}
    #         coupon.edit_action(**act_info)
    for i in range(total):
        id = r.json()['data']['data'][i]["id"]
        act_info = {"id": id, "is_enable": 2}
        coupon.edit_action(**act_info)

def test_add_coupon():
    '''添加优惠劵'''
    #cp_info = {"id":11,"status":2,"name":"在线有礼-满10000减118优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":6,"use_num":0,"coupon_type":10,"using_threshold":"10000.00","coupon_content":118,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 12:32:26","discount":0,"money":0}
    #cp_info = {"id":10,"status":2,"name":"在线有礼-满5000减58优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":6,"use_num":0,"coupon_type":10,"using_threshold":"5000.00","coupon_content":58,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 12:26:38","discount":0,"money":0}
    #cp_info = {"id":9,"status":2,"name":"在线有礼-满3000减28优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":8,"use_num":0,"coupon_type":10,"using_threshold":"3000.00","coupon_content":28,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 12:19:14","discount":0,"money":0}
    #cp = [{"id":8,"status":2,"name":"在线有礼-满1000减9优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":8,"use_num":0,"coupon_type":10,"using_threshold":"1000.00","coupon_content":9,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 12:11:58","discount":0,"money":0}]
    #cp =[{"id":5,"status":2,"name":"十月四期-锦绣纸秋纸钞专场服务费七折优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1635768000,"amount":40,"send_amount":6,"use_num":0,"coupon_type":20,"using_threshold":"0.00","coupon_content":0,"platform":"0","range":40,"vali_type":1,"vali_day":5,"start_time":0,"end_time":0,"create_time":"2021-10-25 10:17:11","discount":70,"money":0}]
    # cp = [{"id":7,"status":2,"name":"在线有礼-五元无门槛优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":16,"use_num":0,"coupon_type":10,"using_threshold":"0.00","coupon_content":5,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 11:59:07","discount":0,"money":0}]
    send_time_s = round(time.time())
    send_time_e = send_time_s +36000
    start_time = send_time_s
    end_time = send_time_e
    # cp = {"name":"500-18元无门槛优惠券","send_time_s":send_time_s,"send_time_e":send_time_e,"amount":200,"coupon_type":10,"using_threshold":"500","coupon_content":18,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":start_time,"end_time":end_time,"discount":0,"money":0}
    cp = {"name": "服务费5折优惠券",  "send_time_s": send_time_s,"send_time_e": send_time_e, "amount": 40,  "coupon_type": 20,"using_threshold": "0.00", "coupon_content": 0, "platform": "0", "range": 40, "vali_type": 1, "vali_day": 5,"start_time": start_time, "end_time": end_time, "discount": 50, "money": 0,"range_list": "[358]","use_restrictions": 1}
    '''name: 优惠劵名称
    send_time: 领劵时间
    vali_type: 有效使用时间：1 ，按照领劵后多少天算，2，按照start_time,end_time 算
    coupon_type: 10 ，满减卷，20，折扣卷
    using_threshold： 使用门槛
    coupon_content: 优惠金额
    discount: 折扣额度
    use_restrictions： 1 互斥 0 不互斥
    range : 使用平台 40 专场 10 所有平台   
    range_list: 适用专场
    '''
    r = coupon.add(**cp)
    print(r.json())
    assert r.json()['status'] == 200





