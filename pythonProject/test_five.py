import requests
import pytest
def test_baidu():
    r=requests.get(url="http://www.baidu.com/")
    assert r.status_code==200
def test_taobao():
    r=requests.get(url="http://www.taobao.com/")
    print(r.elapsed.total_seconds())
    assert r.status_code == 200



def test_jd():
    r=requests.get(url="http://www.jd.com/")
    assert r.status_code == 200
def test_sina():
    r=requests.get(url="http://www.sian.com/")
    assert r.status_code == 200