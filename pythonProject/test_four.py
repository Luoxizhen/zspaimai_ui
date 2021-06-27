import pytest
@pytest.mark.smoke
@pytest.mark.exit
def test_001():
    assert 1==2
@pytest.mark.smoke
def test_002():
    assert 1==1
@pytest.mark.login
def test_003():
    assert 1==1
@pytest.mark.logout
def test_004():
    assert 1==1