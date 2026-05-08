import ctypes
import os

# Build the absolute path to the shared library
# We look for libfib.so by default (since you mentioned WSL/Ubuntu)
# but we add a fallback for Windows (.dll) just in case.
lib_path_so = os.path.join(os.path.dirname(__file__), 'libfib.so')
lib_path_dll = os.path.join(os.path.dirname(__file__), 'fib.dll')

if os.path.exists(lib_path_so):
    fib_lib = ctypes.CDLL(lib_path_so)
elif os.path.exists(lib_path_dll):
    fib_lib = ctypes.CDLL(lib_path_dll)
else:
    raise FileNotFoundError("Could not find the shared library. Please ensure you compiled it.")

# Define the argument types and return type for the C function
fib_lib.CFib.argtypes = [ctypes.c_int]
fib_lib.CFib.restype = ctypes.c_int

def fib(n):
    """
    Wrapper function that calls the C CFib function.
    ctypes handles the conversion between Python int and C int 
    automatically because we defined argtypes and restype above.
    """
    return fib_lib.CFib(n)
