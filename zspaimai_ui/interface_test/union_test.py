import time

from interface_base import union, user

from utils import rwyaml
import pytest
# @pytest.fixture(scope="module")
def user_login1():
    '''所有用户登陆，获取token'''
    for i in range(1, 6):
        testuser = "user" + str(i)
        print(testuser)
        phone = rwyaml.get_yaml_data('interface_data', 'union.yml')[testuser]['phone']
        user.get_msg(phone)
        userinfo = user.quick_login(phone).json()
        token = userinfo['data']['token']
        userno = userinfo['data']['user']['userno']
        rwyaml.set_data('interface_data', 'union.yml', testuser, token, userno)

    user1_token = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['token']
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    rwyaml.set_data('interface_data', 'union.yml', 'user1', user1_token, user1_no)
def get_userinfo(user,key):
    userinfo = rwyaml.get_yaml_data('interface_data', 'union.yml')[user][key]
    return userinfo
def set_userinfo(user, key, keyvalue):
    rwyaml.set_keyvalue('interface_data', 'union.yml', user, key, keyvalue)

def union_join(user1, user2):
    '''该函数提供用户关联的基本操作'''
    token = get_userinfo(user1, 'token')
    union.union_join(token)#用户1 加入推广计划，增加用户是否已加入推广计划，未加入时，执行加入操作

    r = union.union_list_1(token)# 获取用户1的推广链接
    print(r.json())
    '''获取最新的推广素材链接'''
    i = r.json()['data']['total']
    h5_url = ''
    if (i<11):
        j = i-1
        h5_url = r.json()['data']['data'][j]['h5_url']
    else:
        k = i/10 + 1
        r = union.union_lise_2(token, k)
        j = i - 10(k-1) -1
        h5_url = r.json()['data']['data'][j]['h5_url']


    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    rwyaml.set_keyvalue('interface_data', 'union.yml', user1, 'inv', inv)#保存用户1的inv 信息

    phone2 = rwyaml.get_yaml_data('interface_data', 'union.yml')[user2]['phone']# 获取用户2 的手机号码
    user.get_msg(phone2) # 获取验证码
    userinfo = user.quick_login_union(inv, phone2) #用户2快捷登陆，成为用户1的成员
    user2_token = userinfo.json()['data']['token']
    user2_userno = userinfo.json()['data']['user']['userno']
    '''保存用户2 的基本信息'''
    rwyaml.set_keyvalue('interface_data', 'union.yml', user2, 'userno', user2_userno)
    rwyaml.set_keyvalue('interface_data', 'union.yml', user2, 'token', user2_token)


def test_add_union():
    '''验证后台添加推广计划成功'''
    r = union.union_add('推广素材')
    status = r.json()['status']
    union_id = r.json()['data']
    union.union_del(union_id)
    assert status == 200

def user_login(usernum):
    phone = rwyaml.get_yaml_data('interface_data', 'union.yml')[usernum]['phone']
    user.get_msg(phone)
    r = user.quick_login(phone)
    token = r.json()['data']['token']
    userno = r.json()['data']['user']['userno']
    rwyaml.set_keyvalue('interface_data', 'union.yml', usernum, 'token', token)
    rwyaml.set_keyvalue('interface_data', 'union.yml', usernum, 'userno', userno)
    return token
@pytest.fixture(scope='class', name='union_user_login')
def test_user_login():
    user_login('user1')
@pytest.fixture(scope='class', name='union_user_join')
def test_user_join():
    user_token = get_userinfo('user1', 'token')
    union.union_join(user_token)

'''后台基本功能验证'''
@pytest.mark.skip(reason="no way of currently testing this")
class test_union_edit():
    def test_add_union_001(self):
        '''验证后台添加推广计划后，推广计划列表增加一条数据'''
        union_total_pre = union.union_list().json()['data']['total']
        r = union.union_add('推广素材')
        union_id = r.json()['data']
        union_total = union.union_list().json()['data']['total']
        union.union_del(union_id)
        assert union_total == union_total_pre + 1

    def test_add_union_002(self):
        '''验证后台添加推广计划后，pc 端可以看见该推广计划'''
        token = user_login('user1')
        union_total_pre = union.union_list_1(token).json()['data']['total']
        r = union.union_add('推广素材')
        union_id = r.json()['data']
        union_total = union.union_list_1(token).json()['data']['total']
        union.union_del(union_id)
        assert union_total == union_total_pre + 1

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_add_union_003(self):
        '''验证后台添加推广计划后，小程序 端可以看见该推广计划'''
        status = union.union_add('推广素材')
        assert status == 200

    def test_union_del(self):
        '''验证后台删除推广活动功能'''
        union_id = union.union_add('推广素材').json()['data']
        r = union.union_del(union_id)
        status = r.json()['status']
        assert status == 200

    def test_union_del_001(self):
        '''验证后台删除推广活动后，后台列表-1条记录'''
        union_id = union.union_add('推广素材').json()['data']
        r = union.union_list()
        union_total_pre = r.json()['data']['total']
        union.union_del(union_id)
        union_total = union.union_list().json()['data']['total']
        union.union_del(union_id)
        assert union_total == union_total_pre - 1

    def test_union_del_002(self):
        '''验证后台删除推广活动后，pc-1条记录'''
        union_id = union.union_add('推广素材').json()['data']
        token = user_login('user1')
        r = union.union_list_1(token)
        union_total_pre = r.json()['data']['total']
        union.union_del(union_id)
        union_total = union.union_list_1(token).json()['data']['total']
        union.union_del(union_id)
        assert union_total == union_total_pre - 1

    def test_act_edit(self):
        '''验证后台上架、下架推广计划'''
        union_id = union.union_add('推广素材').json()['data']
        act_value = 2
        status = union.union_act_edit(union_id, act_value).json()['status']
        union.union_del(union_id)
        assert status == 200

    def test_act_edit_002(self):
        '''验证后台下架推广计划后pc 端无法查看到该活动'''
        union_id = union.union_add('推广素材').json()['data']
        token = user_login('user1')
        union_total_pre = union.union_list_1(token).json()['data']['total']
        act_value = 2
        union.union_act_edit(union_id, act_value)
        union_total = union.union_list_1(token).json()['data']['total']
        union.union_del(union_id)
        assert union_total_pre == union_total + 1

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_act_edit_003(self):
        '''验证后下架推广计划后，小程序 端无法查看到该活动'''
        union_id = union.union_add('推广素材').json()['data']
        token = user_login('user1')
        union_total_pre = union.union_list_1(token).json()['data']['total']
        act_value = 2
        union.union_act_edit(union_id, act_value)
        union_total = union.union_list_1(token).json()['data']['total']
        union.union_del(union_id)
        assert union_total_pre == union_total + 1

    def test_union_list(self):
        '''验证后台获取推广活动列表功能'''
        r = union.union_list()
        assert r.json()['status'] == 200

    def test_get_user_info(self):
        '''验证后台获取推广用户'''
        file_data = rwyaml.get_yaml_data('interface_data', 'union.yml')
        userno = file_data['user1']['userno']
        r = union.union_user_info(userno)
        status = r.json()['status']
        assert status == 200

    @pytest.mark.skip(reason='')
    def test_set_user_role(self):
        '''验证后台设置推广用户的角色功能，先检查用户的角色，再设置为另一个角色'''

        userno = get_userinfo('user1', 'userno')

        if (union.union_index(userno).json()['data']['total'] == 0):
            union.union_join(userno)
        user_role_pre = union.union_index(userno).json()['data']['data'][0]['role']

        if (user_role_pre == 10):
            union.union_set_role(20)
            user_role = 20

        elif (user_role_pre == 20):
            union.union_set_role(10)
            user_role = 10

        user_role_real = union.union_index(userno).json()['data']['data'][0]['role']
        assert user_role_real == user_role_pre

    def test_search_user(self):
        '''验证后台搜索推广用户列表功能：根据用户编号搜索'''
        userno = get_userinfo('user1', 'userno')
        r = union.union_index(userno)
        assert r.json()['status'] == 200

    def test_get_union_user(self):
        '''验证后台查询某一个用户的关联用户列表详情'''
        userno = get_userinfo('user1', 'userno')
        r = union.union_user(userno)
        print(r)
        status = r.json()['status']
        assert status == 200

    def test_get_union_order(self):
        '''验证后台查询某一个用户的关联订单列表详情'''
        userno = get_userinfo('user1', 'userno')
        r = union.union_order(userno)
        status = r.json()['status']
        assert status == 200

    def test_get_union_commi(self):
        '''验证后台查询某一个用户的推广值明细详情'''
        userno = get_userinfo('user1', 'userno')
        r = union.union_commi(userno)
        status = r.json()['status']
        assert status == 200


@pytest.mark.usefixtures('add_user')
class TestUnionUser(object):
    '''验证正常情况下，业务员所关联的下级用户的所有下级用户都是该业务员的下级用户'''
    # @pytest.mark.skip(reason = '')
    def test_union_join_user1(self):
        user_login('user1')
        token = get_userinfo('user1', 'token')
        r = union.union_join(token)
        userno = get_userinfo('user1', 'userno')
        union.union_set_role(userno, 20)
        assert r.json()["status"] == 200

    def test_union_join_user2_001(self):
        '''验证用户2通过用户1的推广链接加入推广计划'''
        '''先创建一个推广计划： '''
        union_name = get_userinfo('union', 'newname')
        print(union_name)
        set_userinfo('union', 'name', union_name)
        union.union_add(union_name).json()
        union_name_1 = union_name[0:7]

        union_name_2 = union_name[7:11]
        union_newname = union_name_1 + str(int(union_name_2) + 1)
        set_userinfo('union', 'newname', union_newname)

        '''重新保存推广计划'''

        user1_no = get_userinfo('user1', 'userno')
        print(user1_no)
        total_pre = union.union_user(user1_no).json()['data']['total']
        print('用户2加入前用户数')
        print(total_pre)
        union_join('user1', 'user2')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1


    def test_union_join_user3_001(self):
        '''验证用户3 加入推广计划以后，用户3 通过用户2的 inv 加入推广计划，用户3 会成为用户2 的推广用户'''

        '''用户3 为加入用户2 的推广计划前，用户2的推广用户数量：'''
        user2_no = get_userinfo('user2', 'userno')
        total_pre = union.union_user(user2_no).json()['data']['total']
        union_join('user2', 'user3')
        total = union.union_user(user2_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user4_001(self):
        '''验证用户4 通过用户2的推广链接加入推广计划， 用户4 成为业务员： 用户1 的推广成员'''
        user1_no = get_userinfo('user1', 'userno')
        total_pre = union.union_user(user1_no).json()['data']['total']
        union_join('user2', 'user4')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user5_001(self):
        '''验证用户5 通过用户3的推广链接加入推广计划， 用户5成为用户3 的推广成员'''
        user3_no = get_userinfo('user3', 'userno')
        total_pre = union.union_user(user3_no).json()['data']['total']
        union_join('user3', 'user5')
        total = union.union_user(user3_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user6_001(self):
        '''验证用户6 通过用户4的推广链接加入推广计划， 用户6 不会成为用户1 的推广成员'''
        user1_no = get_userinfo('user1', 'userno')
        total_pre = union.union_user(user1_no).json()['data']['total']
        union_join('user3', 'user6')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1

class TestUnionOrder(object):
    '''验证在TestUnionUser 推广用户关联成功后，推广订单的关联'''
class TestUnionCommi(object):
    '''验证在TestUnionUser 推广用户关联成功后，推广订单的关联'''
@pytest.mark.skip(reason='')
def test_union_join():
    user_token = get_userinfo('user1', 'token')
    r = union.union_join(user_token)
    assert r.json()['status'] == 200
@pytest.mark.skip(reason= '')
def test_union_join_001():
    '''验证已加入推广计划的用户重复加入推广计划的提示信息'''
    token = user_login('user1')
    r = union.union_join(token)
    status = r.json()['data']['msg']
    msg = "该用户已加入推广计划"
    assert status == msg

def test_union_user_1():
    '''验证从pc 查看用户自己的关联用户'''
    token = user_login('user1')
    r = union.union_user_1(token)
    status = r.json()['status']
    assert status == 200
def test_union_order_1():
    '''验证从pc 查看用户自己的关联订单'''
    token = user_login('user1')
    r = union.union_order_1(token)
    status = r.json()['status']
    assert status == 200

def test_union_commi_1():
    '''验证从pc 查看用户自己的推广值'''
    token = user_login('user1')
    r = union.union_commi_1(token)
    status = r.json()['status']
    assert status == 200

def test_union_list_1():
    '''验证从pc 查看用户自己的推广值'''
    token = user_login('user1')
    r = union.union_list_1(token)
    status = r.json()['status']
    assert status == 200








@pytest.mark.skip(reason="已经执行过")
def test_union_join_user2_001():
    '''验证用户1 的第一个关联用户编号为 用户2的编号  信息准确信'''
    user1_no = get_userinfo('user1', 'userno')
    r = union.union_user(user1_no)
    user2_no = get_userinfo('user2', 'userno')
    union_user2_no = str(r.json()['data']['data'][0]['userno'])
    assert union_user2_no == user2_no

@pytest.mark.skip(reason= '')
def test_union_join_user2_002():
    '''验证用户1 的第一个关联用户编号为 用户2的 inv 信息准确信'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']
    r = union.union_user(user1_no)
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    union_user2_no = str(r.json()['data']['data'][0]['userno'])
    assert union_user2_no == user2_no

@pytest.mark.skip(reason='')
def test_union_join_user2_003():
    '''验证用户2 在推广用户列表中'''
    user2_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user2']['userno']
    r = union.union_index(user2_no)
    total = r.json()['data']['total']
    # union_user2_no = r.json()['data']['data'][0]['userno']
    # union_user2_inv = r.json()['data']['data'][0]['inv']
    assert total == 1

@pytest.mark.skip(reason="涉及订单支付，订单接口完成后实现")
def test_union_join_user2_004():
    '''验证用户2完成订单支付后，从后台查看用户1的推广订单，生成两笔订单，一步是业务奖励，一笔是推广奖励'''
    user1_no = rwyaml.get_yaml_data('interface_data', 'union.yml')['user1']['userno']

    total_pre = union.union_order(user1_no)
    '''用户2 完成一笔订单支付'''
    pass
@pytest.mark.skip(reason="用户未登陆时发送链接给新用户登陆的用例后续实现")
def test_union_join_user3():
    '''验证用户3 在用户2 未加入推广计划之前，通过用户2的 inv 加入推广计划，用户3 不会成为用户2 的推广用户'''

    '''用户3 为加入用户2 的推广计划前，用户2的推广用户数量：'''
    user2_no = get_userinfo('user2', 'userno')
    r = union.union_user(user2_no)

    total_pre = r.json()['data']['total']

    '''获取用户2的token'''
    token = get_userinfo('user2', 'token')

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
@pytest.fixture(scope='class',name= 'add_user')
def add_user():
    user_phone = get_userinfo('user', 'phone')#13622288516
    ph1 = user_phone[0:8]
    ph2 = user_phone[8:]
    for i in range(1, 7):
        user_str = 'user' + str(i)
        if (i!=1):
            ph2 = str(int(ph2) + 1)
        phone = ph1 + ph2
        set_userinfo(user_str, 'phone', phone)
        set_userinfo(user_str, 'inv', '')
        set_userinfo(user_str, 'userno', '')
        set_userinfo(user_str, 'token', '')
    ph2 = str(int(ph2)+1)
    last_phone = ph1 + ph2
    set_userinfo('user', 'phone', last_phone)



