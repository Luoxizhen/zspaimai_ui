from interface_base import user
import csv
import codecs
from config.conf import cm
import os
from utils import util

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
    for i in range(last_page):
        list.extend(user.list(page=i).json()['data']['data'])

    file_dir = os.path.join(cm.BASE_DIR, 'interface_data', 'user_list.csv')
    f = codecs.open(file_dir,'w','gbk')
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


