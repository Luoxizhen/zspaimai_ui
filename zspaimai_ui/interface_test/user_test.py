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