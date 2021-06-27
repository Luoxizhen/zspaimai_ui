def test_001():
    assert 1==2


class Test_login(object):
    def test_login_001(self):
        assert 1==1
    def add(self):
        assert 2==3
def add(a,b):
    return a+b
def test_add():
    try:

        assert add(1,'1')==2
    except Exception as e:
        print(e.args[0])

def test_smoke_001():
    assert 1==2
def test_smoke_002():
    assert 1==1