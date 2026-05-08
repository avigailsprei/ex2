from fib_module import fib
import pytest
import ctypes

def test_fib_zero():
    """Test the base case n=0"""
    assert fib(0) == 0

def test_fib_one():
    """Test the base case n=1"""
    assert fib(1) == 1

def test_fib_ten():
    """Test a larger calculation for n=10"""
    assert fib(10) == 55

def test_fib_negative():
    """Test a negative number edge case"""
    # Standard Fibonacci usually isn't defined for negative numbers in this context,
    # or should follow the mathematical negative sequence. We might expect a ValueError.
    # Let's assert it raises an error or returns the mathematically correct value (e.g. F(-1)=1).
    # We will see what actually happens!
    with pytest.raises(ValueError):
        fib(-1)

def test_fib_wrong_type_float():
    """Test passing a float"""
    # ctypes should catch this based on argtypes
    with pytest.raises(ctypes.ArgumentError):
        fib(3.14)

def test_fib_wrong_type_string():
    """Test passing a string"""
    with pytest.raises(ctypes.ArgumentError):
        fib("hello")
