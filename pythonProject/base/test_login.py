import pytest
import requests
from requests import request
def get_token():
    data = {"phone":"15622145010","pwd":"123456"}
    r = request(method="post", url='http://api.online.zspaimai.cn/user/user/login', data=data)
    return r.json()['data']['token']
def write(bookID):
    with open('addrID','w') as f:
        f.write(bookID)
def read():
    with open('addrID','r') as f:
        return f.read()
pytest.mark.skip
def test_login():
    data = {"phone":"15622145010","pwd":"123456"}
    r = request(method="post",url='http://api.online.zspaimai.cn/user/user/login',data=data)
    print(r.text)
    print(r.json()['data']['token'])
    assert r.status_code == 200
    assert r.json()['status']==200

def test_addAddr():
    data = {"id":"",
        "name":"罗小姐",
        "phone":"15622145011",
        "address":"岐山村",
        "zipcode":"",
        "province":19,
        "city":308,
        "county":3153,
        "is_default":1}
    token1 = get_token()
    headers = {'token':get_token()}
    r = request(method='post',url= 'http://api.online.zspaimai.cn/user/addr/add',data=data,headers=headers)
    print(r.text)
def test_getAddrList():
    headers = {'token': get_token()}
    r = request(method='get', url='http://api.online.zspaimai.cn/user/addr/list',  headers=headers)
    write(r.json()['data'][0]['id'])
    
def test_deleteAddr():
    addrId = read()
    headers = {'token': get_token()}
    data = {'id': addrId}
    r = request(method='get', url='http://api.online.zspaimai.cn/user/addr/del', headers=headers,json=data)
    print(r.json())