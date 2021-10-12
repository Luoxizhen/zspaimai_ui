from interface_base import union, user

from utils import rwyaml
import pytest
# @pytest.fixture(scope="module")
def test_user_login():
    '''所有用户登陆，获取token'''
    for i in range(1, 6):
        testuser = "user" + str(i)
        print(testuser)
        phone = rwyaml.get_yaml_data('interface_data', 'union.yml')[testuser]['phone']
        user.get_msg(phone)
        userinfo = user.quick_login(phone).json()
        token = userinfo['data']['token']
        userno = userinfo['data']['user']['userno']
        rwyaml.set_data('interface_data', 'union.yml', testuser, token,userno)

    user1_token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['token']
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    rwyaml.set_data('interface_data', 'union.yml', 'user1', user1_token, user1_no)






# def test_quick_login():
#     '''验证用户快捷登陆成功'''
#     phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['phone']
#     user.get_msg(phone)
#     token = user.quick_login(phone)
#     user.update_token(token)
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
@pytest.mark.skip(reason="no way of currently testing this")
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
@pytest.mark.skip(reason="no way of currently testing this")
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
    userno = file_data['user1']['userno']
    r = union.union_user_info(userno)
    status = r.json()['status']
    assert status == 200

def test_set_user_role():
    '''验证后台设置推广用户的角色功能，先检查用户的角色，再设置为另一个角色'''
    if(union.union_index().json()['data']['total']==0):
        union.union_join()
    user_role_pre = union.union_index().json()['data']['data'][0]['role']
    print(user_role_pre)
    if (user_role_pre == 10):
        union.union_set_role(20)
        user_role = 20
        print(user_role)
    elif(user_role_pre == 20):
        union.union_set_role(10)
        user_role = 10
        print(user_role)
    user_role_real = union.union_index().json()['data']['data'][0]['role']
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
    '''验证已加入推广计划的用户重复加入推广计划的提示信息'''
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
def test_union_join_user2():
    '''验证用户2通过用户1的推广链接加入推广计划'''
    '''先创建一个推广计划： 推广计划_自动化测试，勿删除'''
    union.union_add()
    '''检查用户1是否已经加入推广计划，如果未加入推广计划，先加入'''
    if (union.union_index().json()['data']['total'] == 0):
        union.union_join()
    user_role_pre = union.union_index().json()['data']['data'][0]['role']
    '''检查用户1 的角色是否是业务员，如果不是业务员，设置为业务员'''
    if (user_role_pre == 10):
        union.union_set_role(20)
    '''获取用户1 的推广链接'''
    r = union.union_list_1()

    h5_url = r.json()['data']['data'][0]['h5_url']


    '''用户2通过用户1 发送的h5 链接登陆'''
    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    print(inv)



    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['phone']
    user.get_msg(phone)
    '''获取用户的信息，
    更新到 union.yml 上'''
    print('用户信息')
    userinfo = user.quick_login_union(inv, phone).json()

    print(userinfo)
    token = userinfo['data']['token']

    userno = userinfo['data']['user']['userno']
    rwyaml.set_data('interface_data', 'union.yml', 'user2', token, userno)
    '''后台查看用户1 的关联用户，有用户2'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    r = union.union_user_info(user1_no)
    print(r)

    total = r.json()['data']['total']
    union_user2_no = r.json()['data']['data'][0]['userno']
    union_user2_inv = r.json()['data']['data'][0]['inv']
    assert total == 1



def test_union_join_user2_001():
    '''验证用户1 的第一个关联用户编号为 用户2的编号 及 inv 信息准确信'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    r = union.union_user()
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    union_user2_no = str(r.json()['data']['data'][0]['userno'])
    assert union_user2_no == user2_no


def test_union_join_user2_002():
    '''验证用户1 的第一个关联用户编号为 用户2的编号 及 inv 信息准确信'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    r = union.union_user()
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    union_user2_no = str(r.json()['data']['data'][0]['userno'])
    assert union_user2_no == user2_no
def test_union_join_user2_003():
    '''验证用户2 在推广用户列表中'''
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_index(user2_no)
    total = r.json()['data']['total']
    # union_user2_no = r.json()['data']['data'][0]['userno']
    # union_user2_inv = r.json()['data']['data'][0]['inv']
    assert total == 1
def test_union_join_user2_004():
    '''验证用户2完成订单支付后，从后台查看用户1的推广订单，生成两笔订单，一步是业务奖励，一笔是推广奖励'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']

    total_pre = union.union_order(user1_no)
    '''用户2 完成一笔订单支付'''
    pass

def test_union_join_user3():
    '''验证用户3 在用户2 未加入推广计划之前，通过用户2的 inv 加入推广计划，用户3 不会成为用户2 的推广用户'''
    # '''先创建一个推广计划： 推广计划_自动化测试，勿删除'''
    # union.union_add()
    # '''检查用户1是否已经加入推广计划，如果未加入推广计划，先加入'''
    # if (union.union_index().json()['data']['total'] == 0):
    #     union.union_join()
    # user_role_pre = union.union_index().json()['data']['data'][0]['role']
    # '''检查用户1 的角色是否是业务员，如果不是业务员，设置为业务员'''
    # if (user_role_pre == 10):
    #     union.union_set_role(20)
    '''用户3 为加入用户2 的推广计划前，用户2的推广用户数量：'''
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_user(user2_no)

    total_pre = r.json()['data']['total']

    '''获取用户2的token'''
    token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['token']

    '''获取用户2 的推广链接'''
    r = union.union_list_1(token)



    h5_url = r.json()['data']['data'][0]['h5_url']


    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    rwyaml.set_keyvalue('interface_data', 'union.yml', 'user2', 'inv', inv)
    print(inv)
    '''获取用户3 的手机号码'''
    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user3']['phone']
    user.get_msg(phone)
    '''获取用户的信息，
    更新到 union.yml 上'''

    '''用户3 快捷登陆'''
    userinfo = user.quick_login_union(inv, phone).json()
    print(userinfo)

    print(userinfo)
    token = userinfo['data']['token']

    userno = userinfo['data']['user']['userno']
    '''保存用户3 的基本信息'''
    rwyaml.set_data('interface_data', 'union.yml', 'user3', token, userno)
    '''后台查看用户1 的关联用户，有用户2'''
    #user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_user(user2_no)


    total = r.json()['data']['total']

    assert total == total_pre
def test_union_join_user3_001():
    '''验证用户3 加入推广计划以后，用户3 通过用户2的 inv 加入推广计划，用户3 会成为用户2 的推广用户'''

    '''用户3 为加入用户2 的推广计划前，用户2的推广用户数量：'''
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_user(user2_no)

    total_pre = r.json()['data']['total']

    '''获取用户2的token'''
    token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['token']
    '''用户2 加入推广计划'''
    union.union_join(token)


    '''获取用户2 的推广链接'''
    r = union.union_list_1(token)



    h5_url = r.json()['data']['data'][0]['h5_url']


    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    rwyaml.set_keyvalue('interface_data', 'union.yml', 'user2', 'inv', inv)
    print(inv)
    '''获取用户3 的手机号码'''
    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user3']['phone']
    user.get_msg(phone)
    '''获取用户的信息，
    更新到 union.yml 上'''

    '''用户3 快捷登陆'''
    userinfo = user.quick_login_union(inv, phone).json()
    print(userinfo)

    print(userinfo)
    token = userinfo['data']['token']

    userno = userinfo['data']['user']['userno']
    '''保存用户3 的基本信息'''
    rwyaml.set_data('interface_data', 'union.yml', 'user3', token, userno)
    '''后台查看用户1 的关联用户，有用户2'''
    #user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_user(user2_no)


    total = r.json()['data']['total']

    assert total == total_pre+1
def test_union_join_user3_002():
    '''验证用户3也是用户1的下级'''
    '''获取用户1 的关联用户'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    r = union.union_user(user1_no)

    union_user = str(r.json()['data']['data'][0]['userno'])
    user3_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user3']['userno']
    assert union_user == user3_no
def test_union_join_user3_003():
    '''验证用户3 完成订单后，用户1、用户2 各有一笔关联订单'''
    pass
def union_join(user1,user2):
    '''该函数提供用户关联的基本操作'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')[user1]['userno']# 获取用户1的userno
    user1_token = rwyaml.get_yaml_data('interface_data', 'union.yml')[user1]['token'] #获取用户1的token
    union.union_join(user1_token)#用户1 加入推广计划，增加用户是否已加入推广计划，未加入时，执行加入操作
    r = union.union_list_1(user1_token)# 获取用户1的推广链接
    h5_url = r.json()['data']['data'][0]['h5_url']
    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    rwyaml.set_keyvalue('interface_data', 'union.yml', user1, 'inv', inv)#保存用户1的inv 信息

    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')[user2]['phone']# 获取用户2 的手机号码
    user.get_msg(phone) # 获取验证码
    userinfo = user.quick_login_union(inv, phone) #用户2快捷登陆，成为用户1的成员
    user2_token = userinfo.json()['data']['token']
    user2_userno = userinfo.json()['data']['user']['userno']
    '''保存用户2 的基本信息'''
    rwyaml.set_data('interface_data', 'union.yml', user2, user2_token, user2_userno)
    '''后台查看用户1 的关联用户，有用户2'''
def test_union_join_010():
    user4 = rwyaml.get_yaml_data('interface_data', 'union.yml')['user4']['userno']
    user5 = rwyaml.get_yaml_data('interface_data', 'union.yml')['user5']['userno']
    user4_token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user4']['token']



def test_union_join_user4():
    '''验证用户4 成为用户2的推广用户以后，无法成为用户3 的推广用户'''

    user3_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user3']['userno']
    r = union.union_user(user3_no)

    total_pre = r.json()['data']['total']

    '''获取用户3的token'''
    user3_token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user3']['token']
    '''用户3 加入推广计划'''
    union.union_join(user3_token)

    '''获取用户3 的推广链接'''
    r = union.union_list_1(user3_token)

    h5_url = r.json()['data']['data'][0]['h5_url']

    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    rwyaml.set_keyvalue('interface_data', 'union.yml', 'user3', 'inv', inv)
    print(inv)
    '''获取用户4 的手机号码'''
    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')['user4']['phone']
    user.get_msg(phone)
    '''获取用户的信息，
    更新到 union.yml 上'''

    '''用户4 快捷登陆'''
    # userinfo = user.quick_login_union(inv, phone)
    userinfo = user.quick_login_union(inv, phone)
    print(userinfo)

    user4_token = userinfo.json()['data']['token']

    user4_userno = userinfo.json()['data']['user']['userno']
    '''保存用户3 的基本信息'''
    rwyaml.set_data('interface_data', 'union.yml', 'user4', user4_token, user4_userno)
    '''后台查看用户1 的关联用户，有用户2'''
    # user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_user(user3_no)

    total = r.json()['data']['total']

    assert total == total_pre + 1
def test_union_join_user5_001():
    '''验证用户5 通过用户3的inv 加入推广计划，只成为用户4的下级用户，不会成为用户2及用户1的下级用户'''
    '''验证用户4的下级用户，第一个用户 userno 为用户5的userno'''
    user4_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user4']['userno']
    '''获取用户4 的关联用户列表的第一个关联用户id'''
    user_info = union.union_user(user4_no).json()
    print(user_info)
    user4_union_userno = str(user_info['data']['data'][0]['userno'])
    user5_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user5']['userno']
    assert user4_union_userno == user5_no
def test_union_join_user5_002():
    '''验证用户5 通过用户3的inv 加入推广计划，只成为用户4的下级用户，不会成为用户2及用户1的下级用户'''
    '''验证用户4的下级用户，第一个用户 userno 为用户5的userno'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user4']['userno']
    '''获取用户4 的关联用户列表的第一个关联用户id'''
    user_info = union.union_user(user1_no).json()

    user4_union_userno = str(user_info['data']['data'][0]['userno'])
    user5_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user5']['userno']
    assert user4_union_userno != user5_no