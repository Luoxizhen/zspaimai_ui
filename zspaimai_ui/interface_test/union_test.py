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
    status = union.union_add()
    assert status == 200
    union.union_del()
def test_add_union_001():
    '''验证后台添加推广计划后，推广计划列表增加一条数据'''
    union_total = union.union_list().json()['data']['total']
    status = union.union_add()
    assert status == 200
def test_add_union_002():
    '''验证后台添加推广计划后，pc 端可以看见该推广计划'''
    status = union.union_add()
    assert status == 200
def test_add_union_003():
    '''验证后台添加推广计划后，小程序 端可以看见该推广计划'''
    status = union.union_add()
    assert status == 200
def test_act_edit():
    '''验证后台上架、下架推广计划'''
    file_data = rwyaml.get_yaml_data('interface_data', 'union.yml')
    union_id = file_data['new_union_id']
    act_value = 1
    status = union.union_act_edit(union_id, act_value)
    assert status == 200
def test_union_del():
    '''验证后台删除推广活动功能'''
    union.union_del()
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