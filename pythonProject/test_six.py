import pytest
@pytest.mark.skip(reason ='登陆功能')
def test_log():
    assert 1==2
@pytest.mark.xfail(reason='电话登陆功能')
def test_phonelog():
    assert 2==3
def test_wlog():
    assert '2' in "123"