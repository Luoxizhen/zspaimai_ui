import pytest




#
#



def add(a,b):
    return a+b
# @pytest.mark.parametrize('a,b,expect',[
#     [1,1,2],
#     [2,2,5],
#     [3,3,9]
# ])
data=[
    pytest.param(1,1,2,id='one'),
    pytest.param(2,2,4,id='two'),
    pytest.param(3,3,6,id='three')
]
@pytest.mark.parametrize('a,b,expect',data)
# @pytest.mark.parametrize('data',[
#     {'a':1,'b':1,'expect':2},
#     {'a':1,'b':1,'expect':2},
#     {'a':1,'b':1,'expect':2}
# ])
# def test_add(data):
#     print(data['a'])
#     assert add(data['a'],data['b'])==data['expect']
def test_add(a,b,expect):
    assert add(a, b) == expect
# if __name__='__main__'
#     pytest.main('-s','-v','test_seven.py')
