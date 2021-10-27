from interface_base import user
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