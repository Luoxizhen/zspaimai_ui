from interface_base import user
import csv
import codecs
from config.conf import cm
import os
from utils import util
import random

def test_logging():
    user.update_token()


def test_add_pwd():
    phone = '13111111248'
    user.get_msg(phone)
    r = user.verify(phone)
    user_code = r.json()['data']['user_code']
    r = user.add_pwd(user_code)
    print(r.json())
    assert r.json()['status'] == 200

def add_pwd(token,phone,pwd=None):
    user.get_msg(token, phone)# 第一步，发送短信验证码
    user_code = user.verify(phone).json()['data']['user_code']#第二步，输入短信验证码
    new_pwd = "246810"if pwd is None else pwd
    r = user.add_pwd(user_code,new_pwd) #第三步，输入新密码
    print(r.json())
    return r


def test_add_pwd_001():
    r = add_pwd('13111111111')
    assert r == 200
def test_list():
    list = []
    info = user.list().json()
    last_page = info['data']['last_page']
    total = info['data']['total']
    for i in range(114,last_page+1):
        list.extend(user.list(page=i).json()['data']['data'])

    file_dir = os.path.join(cm.BASE_DIR, 'interface_data', 'user_list_20220927.csv')
    f = codecs.open(file_dir,'w','utf-8')
    writer = csv.writer(f)
    writer.writerow(list[0].keys())

    for i in list:
        try:
            writer.writerow(i.values())
        except UnicodeEncodeError:
            i["wechat_name"] = ""
            writer.writerow(i.values())

    f.close()

def test_info():
    ids = util.list_nums(user.list,"id")
    file_dir = os.path.join(cm.BASE_DIR, 'interface_data', 'user_info.csv')
    f = codecs.open(file_dir, 'w', 'gbk')
    writer = csv.writer(f)
    user_info = user.info(ids[0]).json()['data']
    user_info.pop('nickname_list')
    user_info.pop('user_bill')
    user_info.pop('user_quota')
    writer.writerow(user_info.keys())

    for i in ids:

        user_info = user.info(i).json()['data']
        if user_info["address"]!=[]:
            user_info.pop('nickname_list')
            user_info.pop('user_bill')
            user_info.pop('user_quota')
            adds = user_info["address"]
            user_info.pop("address")


            for i in range(len(adds)):
                adds_index = "address" + str(i)
                user_info[adds_index] = adds[i]
            try:
                writer.writerow(user_info.values())
            except UnicodeEncodeError:
                user_info["wechat_name"] = ""

                writer.writerow(user_info.values())
    f.close()
def test_login():
    # 13111111255
    user_info ={"phone": "20000000011",
            "pwd": "zs011015"}
    r = user.login(**user_info)
    token = r.json()['data']['token']
    user.update_token(token)
    print(r.json())
    assert r.json()['status'] == 200
def test_login_2():
    r = user.quick_login("13111111297")
    print(r.json())
    token = r.json()['token']
    user.update_token(token)
    print(r.json())
    assert r.json()['status'] == 200
def test_add_nickname():
    f = open("/Users/yuanyuanhe/Desktop/货/昵称.csv",mode="r",encoding="gbk")
    csv_reader = csv.reader(f)
    for i in csv_reader:
        info = {"nickname": i[0], "id": ""}
        r = user.nickname_add(**info)



    assert 200 == 200
def test_list_nickname():
    r = user.nickname_list()
    print(r.json())

    assert r.json()['status'] == 100


def test_set_nickname():
    info = {"id":1022}
    r = user.nickname_set(**info)
    print(r.json())
    assert r.json()['status'] ==100


def test_bid():
    info = {"goods_id":"3840","price":2000}
    r = user.bid(**info)
    print(r.json())
    assert r.json()['status'] == 100
def test_add_nickname_list():
    nick_name = ['桃之夭夭','灼灼其华','叶蓁蓁','从善','去恶','明星有烂','赵敏','蛛儿','周芷若']
    for i in nick_name:
        info = {"nickname": i, "id": ""}
        user.nickname_add(**info)
def test_get_nicknames():
    nicknames = user.nickname_list().json()['data']
    nickname_ids = []
    for i in nicknames:
        nickname_ids.append(i['id'])
    print (nickname_ids)

    assert 1==2
def test_change_nickname_bid():
    nicknames = user.nickname_list().json()['data']
    nickname_ids = []
    f = open("/Users/yuanyuanhe/Desktop/货/出价.csv",mode="r",encoding="gbk")
    reader = csv.reader(f)
    good_ids = []
    prices = []
    for i in reader:
        good_ids.append(i[0])
        prices.append(int(i[2])+100)

    # good_ids = [4078,4079,4080,4081,4082,4083,4084,4085,4086,4087,4088,4089,4090,4091,4092,4093,4094,4095,4096]
    # prices = [500,600,10000,6000,300,100,1000,2000,60,50,100,150,100,10000,2500,300,100,200,200]

    for i in nicknames:
        nickname_ids.append(i['id'])
    for i in range(19):
        info = {"id": nickname_ids[i+1]}
        user.nickname_set(**info)


        bid_info = {"goods_id":str(good_ids[i]),"price":prices[i]}
        r= user.bid(**bid_info)



    assert 1==2

def test_edit_customer_nicknames():
    user_info = {
        "phone": "20000000017",
        "pwd": "zs011015"
    }
    user.user_login(**user_info)
    nicknames = user.nickname_list().json()["data"]
    print(nicknames)
    len_nn = len(nicknames)
    for i in range(len_nn):
        nick_name_id = nicknames[i]["id"]
        r = random.randrange(2)
        print(r)
        if r == 0:
            nickname = util.get_random(8,2)
        else:
            nickname = util.chinese_name()
        nickname_new = {"nickname": nickname,
                        "id": nick_name_id}

        r = user.nickname_edit(**nickname_new)
        if r.json()["status"] == 400 :
            nickname = util.get_random(8, 2)
            nickname_new = {"nickname": nickname,
                            "id": nick_name_id}

            r = user.nickname_edit(**nickname_new)
        # print(r.json())

    assert 1==2
if __name__ == "__main__":
    test_edit_customer_nicknames()