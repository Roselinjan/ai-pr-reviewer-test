from main import add, get_api_key, multiply


def test_add():
    assert add(2,3) == 5

def test_multiply():
    assert multiply(2,3) == 6

def test_get_api_key():
    assert get_api_key() == "sk-1234567890"