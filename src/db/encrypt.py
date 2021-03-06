# coding=utf-8
from ctypes import *
from os import path

dll_path = path.dirname(__file__) + '/Encrypt.dll'
ENCRYPT_DLL = WinDLL(dll_path)
API_PROTO = WINFUNCTYPE(c_wchar_p, c_wchar_p)
PARAM = (1, 'p', 0),
HAPI = API_PROTO(('HugegisDecode', ENCRYPT_DLL), PARAM)


def decode(str):
    p = c_wchar_p(str)
    return HAPI(p)
