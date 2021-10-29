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
    cp = [{"id":7,"status":2,"name":"在线有礼-五元无门槛优惠券","is_enable":1,"send_time_s":1635487200,"send_time_e":1636905600,"amount":200,"send_amount":16,"use_num":0,"coupon_type":10,"using_threshold":"0.00","coupon_content":5,"platform":"0","range":10,"vali_type":2,"vali_day":20,"start_time":1635487200,"end_time":1637078400,"create_time":"2021-10-29 11:59:07","discount":0,"money":0}]
    for i in range(len(cp)):
        cp_info = cp[i]
        r = coupon.add(**cp_info)




