from main import add, multiply, square


def test_add():
    assert add(2,3) == 5

def test_multiply():
    assert multiply(2,3) == 6

def test_square():
    assert square(4) == 16