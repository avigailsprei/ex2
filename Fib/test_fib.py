from fib_module import fib

def test_fib_zero():
    """Test the base case n=0"""
    assert fib(0) == 0

def test_fib_one():
    """Test the base case n=1"""
    assert fib(1) == 1

def test_fib_ten():
    """Test a larger calculation for n=10"""
    assert fib(10) == 55
