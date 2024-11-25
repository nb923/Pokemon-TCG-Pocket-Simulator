from example_function_for_test import add

def test_addition():
    assert add(1, 1) == 2

def test_addition_negative():
    assert add(1, -1) == 0