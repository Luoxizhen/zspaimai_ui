from interface_base import union, user
from utils import rwyaml

def test_quick_login():
    '''验证用户快捷登陆成功'''
    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['phone']
    user.get_msg(phone)

    token = user.quick_login(phone)

    user.update_token(token)
def test_add_union():
    '''验证后台添加推广计划成功'''
    r = union.union_add()
    status = r.json()['status']
    union_id = r.json()['data']
    union.union_del(union_id)
    assert status == 200


def test_add_union_001():
    '''验证后台添加推广计划后，推广计划列表增加一条数据'''
    union_total_pre = union.union_list().json()['data']['total']
    r = union.union_add()
    union_id = r.json()['data']
    union_total = union.union_list().json()['data']['total']
    union.union_del(union_id)
    assert union_total == union_total_pre + 1

def test_add_union_002():
    '''验证后台添加推广计划后，pc 端可以看见该推广计划'''
    union_total_pre = union.union_list_1().json()['data']['total']
    r = union.union_add()
    union_id = r.json()['data']
    union_total = union.union_list_1().json()['data']['total']
    union.union_del(union_id)
    assert union_total == union_total_pre + 1

def test_add_union_003():
    '''验证后台添加推广计划后，小程序 端可以看见该推广计划'''
    status = union.union_add()
    assert status == 200

def test_union_del():
    '''验证后台删除推广活动功能'''
    union_id = union.union_add().json()['data']
    r = union.union_del(union_id)
    status = r.json()['status']
    assert status == 200
def test_union_del_001():
    '''验证后台删除推广活动后，后台列表-1条记录'''
    union_id = union.union_add().json()['data']
    r = union.union_list()
    union_total_pre = r.json()['data']['total']
    union.union_del(union_id)
    union_total = union.union_list().json()['data']['total']
    union.union_del(union_id)
    assert union_total == union_total_pre -1
def test_union_del_002():
    '''验证后台删除推广活动后，pc-1条记录'''
    union_id = union.union_add().json()['data']
    r = union.union_list_1()
    union_total_pre = r.json()['data']['total']
    union.union_del(union_id)
    union_total = union.union_list_1().json()['data']['total']
    union.union_del(union_id)
    assert union_total == union_total_pre -1

def test_act_edit():
    '''验证后台上架、下架推广计划'''
    union_id = union.union_add().json()['data']
    act_value = 2
    status = union.union_act_edit(union_id, act_value).json()['status']
    union.union_del(union_id)
    assert status == 200

def test_act_edit_002():
    '''验证后台下架推广计划后pc 端无法查看到该活动'''
    union_id = union.union_add().json()['data']
    union_total_pre = union.union_list_1().json()['data']['total']
    act_value = 2
    union.union_act_edit(union_id, act_value)
    union_total = union.union_list_1().json()['data']['total']
    union.union_del(union_id)
    assert union_total_pre == union_total + 1

def test_act_edit_003():
    '''验证后下架推广计划后，小程序 端无法查看到该活动'''
    union_id = union.union_add().json()['data']
    union_total_pre = union.union_list_1().json()['data']['total']
    act_value = 2
    union.union_act_edit(union_id, act_value)
    union_total = union.union_list_1().json()['data']['total']
    union.union_del(union_id)
    assert union_total_pre == union_total + 1

def test_union_list():
    '''验证后台获取推广活动列表功能'''
    r = union.union_list()
    assert r.json()['status'] == 200

def test_get_user_info():
    '''验证后台获取推广用户'''
    file_data = rwyaml.get_yaml_data('interface_data', 'union.yml')
    userno = file_data['userno']
    r = union.union_user_info(userno)
    status = r.json()['status']
    assert status == 200

def test_set_user_role():
    '''验证后台设置推广用户的角色功能，先检查用户的角色，再设置为另一个角色'''
    user_role_pre = union.union_search_user().json()['data']['data'][0]['role']
    if (user_role_pre == 10):
        union.union_set_role(20)
        user_role = 20
    elif(user_role_pre == 20):
        union.union_set_role(10)
        user_role = 10
    user_role_real = union.union_search_user().json()['data']['data'][0]['role']
    assert user_role_real == user_role

def test_search_user():
    '''验证后台搜索推广用户列表功能：根据用户编号搜索'''
    r = union.union_index()
    assert r.json()['status'] == 200
def test_get_union_user():
    '''验证后台查询某一个用户的关联用户列表详情'''
    r = union.union_user()
    status = r.json()['status']
    assert status == 200
def test_get_union_order():
    '''验证后台查询某一个用户的关联订单列表详情'''
    r = union.union_order()
    status = r.json()['status']
    assert status == 200
def test_get_union_commi():
    '''验证后台查询某一个用户的推广值明细详情'''
    r = union.union_commi()
    status = r.json()['status']
    assert status == 200

def test_union_join():
    '''验证后台查询某一个用户的推广值明细详情'''
    r = union.union_join()
    status = r.json()['data']['msg']
    msg = "该用户已加入推广计划"
    assert status == msg
def test_union_user_1():
    '''验证从pc 查看用户自己的关联用户'''
    r = union.union_user_1()
    status = r.json()['status']
    assert status == 200
def test_union_order_1():
    '''验证从pc 查看用户自己的关联订单'''
    r = union.union_order_1()
    status = r.json()['status']
    assert status == 200

def test_union_commi_1():
    '''验证从pc 查看用户自己的推广值'''
    r = union.union_commi_1()
    status = r.json()['status']
    assert status == 200

def test_union_list_1():
    '''验证从pc 查看用户自己的推广值'''
    r = union.union_list_1()
    status = r.json()['status']
    assert status == 200