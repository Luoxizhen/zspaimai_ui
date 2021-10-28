import time
import json
from interface_base import union, user, finance, goods, order
from utils import rwyaml
from interface_test.user_test import add_pwd
import pytest

def updata_user_token(userinfo):
    '''所有用户登陆，获取token'''
    phone = get_userinfo(userinfo, 'phone')
    token = user.get_token(phone)
    set_userinfo(userinfo, 'token', token)
def get_userinfo(user,key):
    userinfo = rwyaml.get_yaml_data('interface_data', 'union.yml')[user][key]
    return userinfo
def set_userinfo(user, key, keyvalue):
    rwyaml.set_keyvalue('interface_data', 'union.yml', user, key, keyvalue)
def get_user_id(user):
    user_no = get_userinfo(user, 'userno')
    user_id = int(user_no) - 192800
    return user_id
def union_join(user1, user2):
    '''该函数提供用户关联的基本操作'''
    token = get_userinfo(user1, 'token')
    union.union_join(token)#用户1 加入推广计划，增加用户是否已加入推广计划，未加入时，执行加入操作
    r = union.union_list_user(1)# 获取用户1的推广链接
    '''获取最新的推广素材链接'''
    i = r.json()['data']['total']
    print("推广素材总数： {}".format(i))
    h5_url = ''
    if i < 11:
        j = i-1
        h5_url = r.json()['data']['data'][j]['h5_url']

    else:
        k = int(i/10) + 1
        r = union.union_list_user(k)
        j = int(i - 10 * (k-1)-1)
        h5_url = r.json()['data']['data'][j]['h5_url']
    '''从h5_url 中提取 inv 信息:http://home.online.zspaimai.cn/?inv=VEVVL1FyODVDVlZYWGVTazg2S0JCZHVpMk9KZmhkeCtycHN1Z0FjWmdiZz0='''
    inv = h5_url.replace('http://home.online.zspaimai.cn/?inv=', '')
    set_userinfo(user1, 'inv', inv)
    phone2 = get_userinfo(user2, 'phone')# 获取用户2 的手机号码
    user.get_msg(phone2) # 获取验证码
    userinfo = user.quick_login_union(inv, phone2) #用户2快捷登陆，成为用户1的成员
    user2_token = userinfo.json()['data']['token']
    user2_userno = userinfo.json()['data']['user']['userno']
    '''保存用户2 的基本信息'''
    set_userinfo(user2, 'userno', user2_userno)
    set_userinfo(user2, 'token', user2_token)
@pytest.fixture(scope='class',name= 'add_user')
def add_user():
    '''给关联用户测试提供准备工作，更新interface_data.union.yml 中的用户手机号码，使用全新手机号码进行关联'''
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
def add_union():
    '''根据 union.yml 中的 newname 创建一个推广计划，在newname +1 后保存推广计划名称 '''
    union_name = get_userinfo('union', 'newname')
    set_userinfo('union', 'name', union_name)
    union_info = {'name': union_name}
    union.union_add(**union_info).json()
    union_name_1 = union_name[0:7]
    union_name_2 = union_name[7:11]
    union_newname = union_name_1 + str(int(union_name_2) + 1)
    set_userinfo('union', 'newname', union_newname) # 保存推广计划新名称


def test_add_union():
    '''验证后台添加推广计划成功'''
    # for i in range (1,10):
    #     name = "推广素材-" + str(i)
    #     r = union.union_add(name)
    r = union.union_add("add_union_test")
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
class TestUnionEdit():
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
    #@pytest.mark.skip(reason='')
    def test_union_join_user1(self):
        phone = get_userinfo('user1', 'phone')
        user.get_msg(phone)
        r = user.quick_login(phone)
        token = r.json()['data']['token']
        userno = r.json()['data']['user']['userno']
        set_userinfo('user1', 'token', token)
        set_userinfo('user1', 'userno', userno)#用户登陆并保存信息
        user.update_token(token)
        r = union.union_join()#用户加入推广计划
        union.set_union_role(userno, 20)# 设置用户为业务员
        assert r.json()['status'] == 200

    def test_union_join_user2(self):
        '''验证用户2通过用户1的推广链接加入推广计划'''
        add_union()
        user1_no = get_userinfo('user1', 'userno')
        total_pre = union.union_user(user1_no).json()['data']['total']
        union_join('user1', 'user2')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user3(self):
        '''验证用户3 加入推广计划以后，用户3 通过用户2的 inv 加入推广计划，用户3 会成为用户2 的推广用户'''

        '''用户3 为加入用户2 的推广计划前，用户2的推广用户数量：'''
        user2_no = get_userinfo('user2', 'userno')
        total_pre = union.union_user(user2_no).json()['data']['total']
        union_join('user2', 'user3')
        total = union.union_user(user2_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user4(self):
        '''验证用户4 通过用户2的推广链接加入推广计划， 用户4 成为业务员： 用户1 的推广成员'''
        user1_no = get_userinfo('user1', 'userno')
        total_pre = union.union_user(user1_no).json()['data']['total']
        union_join('user2', 'user4')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user5(self):
        '''验证用户5 通过用户3的推广链接加入推广计划， 用户5成为用户3 的推广成员'''
        user3_no = get_userinfo('user3', 'userno')
        total_pre = union.union_user(user3_no).json()['data']['total']
        union_join('user3', 'user5')
        total = union.union_user(user3_no).json()['data']['total']
        assert total == total_pre + 1

    def test_union_join_user6(self):
        '''验证用户6 通过用户4的推广链接加入推广计划， 用户6 会成为用户1 的推广成员'''
        user1_no = get_userinfo('user1', 'userno')
        total_pre = union.union_user(user1_no).json()['data']['total']
        union_join('user3', 'user6')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == total_pre + 1
    def test_union_join_user7(self):
        '''验证用户1 的推广用户数量为5'''
        user1_no = get_userinfo('user1', 'userno')
        total = union.union_user(user1_no).json()['data']['total']
        assert total == 5

class TestUnionIndex(object):
    '''在用户关联成功以后，检查各个上级用户的额度
        新用户加入用户的推广计划后，该用户可获得额度奖励 2000'''
    def test_union_index_001(self):
        '''验证业务员：用户1 的额度奖励 - 推荐一个新用户： 用户2 '''
        userno = get_userinfo('user1', 'userno')
        quota = union.union_index(userno).json()['data']['data'][0]['quota']
        assert quota == '2000.00'
    def test_union_index_002(self):
        '''验证用户2 的额度奖励 - 推荐2新用户： 用户3、 用户4'''
        userno = get_userinfo('user2', 'userno')
        quota = union.union_index(userno).json()['data']['data'][0]['quota']
        assert quota == '4000.00'
    def test_union_index_003(self):
        '''验证用户3 的额度奖励 - 推荐2新用户： 用户5、 用户6'''
        userno = get_userinfo('user3', 'userno')
        quota = union.union_index(userno).json()['data']['data'][0]['quota']
        assert quota == '4000.00'
class TestUnionOrder(object):
    '''在用户关联成功以后， 各用户下的推广用户完成订单支付以后，用户的推广订单列表中显示下级用户的成交订单
    业务员的下级用户成交的订单，在业务员的推广订单列表中，显示两条记录，
    其中一条记录计算业务提成：订单的拍品成交价总额 * 业务员佣金比例，
    一条记录计算推广值：订单的拍品成交总额 * 推广素材的推广值返点'''
    # 1、在途佣金计算方式更改为，用户收货7天，不允许退货退款后，开始计算
    # 2、佣金计算方式更改为，支付时间30天后，在途佣金才确认到账，允许提现到余额
    def test_set_pwd_addr(self):
        '''用户完成订单支付前先设置支付密码'''
        for i in range(2,7):
        #for i in (5,):
            user_info ='user'+ str(i)
            phone = get_userinfo(user_info, 'phone')
            token = get_userinfo(user_info, 'token')
            r1 = add_pwd(token, phone) #设置支付密码
            r2 = user.add_addr()

    # def test_union_order_000(self):
    #     '''验证用户4 增加收货地址'''
    #     for i in (2, 6):
    #         user_info = 'user' + st r(i)
    #         token = get_userinfo(user_info, 'token')
    #         user.add_addr(token)

    def test_union_order_001(self):
        '''验证用户2完成一笔订单支付'''
        order_info = {'good_names': ['关联拍品1'], "user": "user2"}
        r = add_union_order(**order_info)
        assert r.json()['status'] == 200
    def test_union_order_002(self):
        '''验证用户2完成一笔订单支付'''
        order_info = {'good_names': ['关联拍品2', '关联拍品3'], "user": "user2"}
        r = add_union_order(**order_info)


        assert r.json()['status'] == 200

    def test_union_order_003(self):
        '''验证用户2完成一笔订单支付：2个拍品'''
        order_info = {'good_names': ['关联拍品4', '关联拍品5'], "user": "user2"}
        r = add_union_order(**order_info)
        assert r.json()['status'] == 200
    def test_union_order_004(self):
        '''验证用户6完成订单支付：1个拍品'''
        order_info = {'good_names': ['关联拍品6'], "user": "user6"}
        r = add_union_order(**order_info)
        assert r.json()['status'] == 200
    def test_union_order_005(self):
        '''验证用户6完成订单支付：2个拍品'''
        order_info = {'good_names': ['关联拍品7', '关联拍品8'], "user": "user6"}
        r = add_union_order(**order_info)
        assert r.json()['status'] == 200
    def test_union_order_006(self):
        '''验证用户6完成订单支付：1个拍品'''
        order_info = {'good_names': ['关联拍品9', '关联拍品10'], "user": "user6"}
        r = add_union_order(**order_info)
        assert r.json()['status'] == 200
    def test_union_order_007(self):
        '''验证用户6的第二个订单部分退款'''
        #order.confirm_order() #后台确认订单
        good_id = order.refund_goods(1477).json()['data'][0]['goods_id']
        goods_id = '['+str(good_id)+']'
        refund_info = {"order_id":1477,
            "refund_money":"1100",
            "goods_id":goods_id}
        r = order.refund(**refund_info)
        assert r.json()['status'] == 200
    def test_union_order_008(self):
        '''验证用户6的第二个订单部分退款'''
        #order.confirm_order(1478) #后台确认订单
        good_id = order.refund_goods(1478).json()['data'][0]['goods_id']
        goods_id = '['+str(good_id)+']'
        refund_info = {"order_id":1478,
            "refund_money":"1100",
            "goods_id":goods_id}
        order.refund(**refund_info)
    def test_union_order_009(self):
        '''验证用户六提货'''
        for order_ids in (1476,1477,1478):
            order.take_delivery(order_ids)





    def test_union_order_011(self):
        '''验证用户4 完成订单'''
        order_info = {'good_names': ['关联拍品20','关联拍品21','关联拍品22'], "user": "user4", "express":2}
        r = add_union_order(**order_info)
        print (r.json())
        assert r.json()['status'] == 200


    def test_union_order_012(self):
        '''验证用户4 完成订单'''
        # user_phone = get_userinfo('user4', 'phone')
        # token = user.get_token_quick(user_phone)
        # set_userinfo('user4', 'token', token)
        delivery_info = {
            "user_addr_id": 193,
            "goods": "[{\"goods_id\":2452,\"buy_number\":1}]"
        }

        express_fee = order.calculate_freight(**delivery_info).json()['data']['freight']
        express_fee = round(float(express_fee))
        order_info = {'goods_ids': '["2452"]', 'total': 1100, 'addr_id': 193, 'express_fee': express_fee}

        r = order.add_order(**order_info)

        print (r.json())
        assert r.json()['status'] == 200


    def test_update_token_013(self):
        user_phone = get_userinfo('user4', 'phone')
        token = user.get_token_quick(user_phone)
        set_userinfo('user4', 'token', token)
        user.update_token(token)


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


# def add_union_order_1(**order_info):
#     '''验证用户完成订单支付'''
#     order_info_list = ['good_name', 'user']
#     order_info_real = {'good_name': "关联订单", "user": "user2"}
#     for key in order_info:
#         if key in order_info_list:
#             order_info_real[key] = order_info[key]
#     begin_time = round(time.time())
#     end_time = begin_time + 20
#     good_info = {"begin_time": begin_time, "end_time": end_time, "name": order_info_real['good_name'], "price": 1000}
#     print(good_info)
#     good_id = goods.goods_add(**good_info).json()['data'] #添加拍品，获取新添加拍品的id
#     print(good_id)
#     time.sleep(2)
#     token = get_userinfo(order_info_real['user'], 'token')
#     user_id = get_user_id(order_info_real['user'])
#     recharge_info = {'money': '10000', 'user_id': user_id}
#     finance.recharge(**recharge_info)  #后台给用户充值
#     goods.bidding(good_id, 1000, token) #用户竞买拍品
#     time.sleep(20)
#     #user_phone = get_userinfo(order_info_real['user'], 'phone')
#     #add_pwd(user_phone) #设置支付密码
#     order_info = {"goods_ids": "["+str(good_id)+"]", "total":1100, "appointment":"2021-10-26"}#用户支付订单
#     r = order.add_order(token,**order_info)
#     print (r.json())
#     return r
# def add_union_order_2(**order_info):
#     '''验证用户完成订单支付'''
#     order_info_list = ['good_name', 'user']
#     order_info_real = {'good_name': ['关联拍品1', '关联拍品2'], "user": "user2"}
#     good_ids = [1,2]
#     for key in order_info:
#         if key in order_info_list:
#             order_info_real[key] = order_info[key]
#     for i in (0,1):
#         begin_time = round(time.time())
#         end_time = begin_time + 10
#         good_info = {"begin_time": begin_time, "end_time": end_time, "name": order_info_real['good_name'][i], "price": 1000}
#         good_ids[i] = goods.goods_add(**good_info).json()['data'] #添加拍品，获取新添加拍品的id
#         time.sleep(2)
#         token = get_userinfo(order_info_real['user'], 'token')
#
#         user_id = get_user_id(order_info_real['user'])
#         recharge_info = {'money': '10000', 'userid': user_id}
#         finance.recharge(**recharge_info)  # 后台给用户充值
#         goods.bidding(good_ids[i], 1000, token) #用户竞买拍品
#         time.sleep(10)
#         user_phone = get_userinfo(order_info_real['user'], 'phone')
#     #add_pwd(user_phone) #设置支付密码
#     token = get_userinfo(order_info_real['user'], 'token')
#     order_info = {"goods_ids": "["+str(good_ids[0])+','+str(good_ids[1])+"]", "total": 2200, "appointment":"2021-10-26"}#用户支付订单
#     r = order.add_order(token,**order_info)
#     return r
def add_union_order(**order_info):
    '''验证用户完成订单支付'''
    order_info_list = ['good_names', 'user','express']
    order_info_real = {'good_names': ['关联拍品1', '关联拍品2'], "user": "user2", 'express':0}
    good_ids = []
    goods_infos = []
    for key in order_info:
        if key in order_info_list:
            order_info_real[key] = order_info[key]
    token = get_userinfo(order_info_real['user'], 'token')
    for goodname in order_info_real['good_names']:
        begin_time = round(time.time())
        end_time = begin_time + 10
        good_info = {"begin_time": begin_time, "end_time": end_time, "name": goodname, "price": 1000}
        good_id = goods.goods_add(**good_info).json()['data'] #添加拍品，获取新添加拍品的id
        good_ids.append(good_id)
        goods_infos.append({"goods_id": int(good_id), "buy_number": 1})
        time.sleep(2)
        user_id = get_user_id(order_info_real['user'])
        recharge_info = {'money': '10000', 'user_id': user_id}
        finance.recharge(**recharge_info)  # 后台给用户充值
        bid_info = {"goods_id": good_id, "price": 1000 }
        r = goods.bidding(token,**bid_info) #用户竞买拍品
        time.sleep(10)
    # "["+str(good_ids[0])+','+str(good_ids[1])+"]"

    id = "["
    goods_info = "["
    for i in range(len(good_ids)):
        if i < len(good_ids)-1:
            id = id + good_ids[i] + ","
            goods_info = goods_info + json.dumps(goods_infos[i]) + ","
        else:
            id = id + good_ids[i] + "]"
            goods_info = goods_info + json.dumps(goods_infos[i]) + "]"
    total = 1100 * len(good_ids)
    addr_id = user.addr_list(token).json()['data'][0]['id']
    print(goods)


    delivery_info = {
        "user_addr_id": addr_id,
        "goods": goods_info
    }
    r = order.calculate_freight(**delivery_info).json()
    express_fee = round(float(r['data']['freight']))

    if order_info_real['express'] == 0: #上门自提
        date = time.strftime('%Y-%m-%d', time.localtime())  # "appointment": "2021-10-26"
        order_info = {"goods_ids": id, "total": total, "appointment": date}  # 用户支付订单
    else: #货到付款
        order_info = {"goods_ids": id, "total": total, "addr_id": addr_id, 'express_fee': express_fee}#用户支付订单

    r = order.add_order(**order_info)
    order_id = r.json()['data']['reId']
    order.confirm_order(order_id)
    return r

def test_dd():
    date = time.strftime('%Y-%m-%d', time.localtime())
    print(date)
    assert 1==2
