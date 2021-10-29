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







