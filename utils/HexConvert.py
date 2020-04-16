# -*- coding: utf-8 -*-
"""
Created on 2020/4/11 1:47
Author  : zxt
File    : HexConvert.py
Software: PyCharm
"""


def bin2qua(num):
    # todo
    return num


def bin2oct(num):
    # todo
    return num


def bin2dec(num):
    num = str(float(num))
    i, f = num.split(".")

    def __int2dec(i):
        return int(i, 2)

    def __float2dec(f):
        d = 0
        for idx, val in enumerate(f):
            d += 2 ** (-idx - 1) * int(val)
        return d

    return __int2dec(i) + __float2dec(f)


def bin2hex(num):
    num = str(num)
    if '.' in num:
        i, f = num.split(".")
    else:
        i, f = num, ''

    def __int2hex(i):
        return hex(int(i, 2))[2:]

    def __float2hex(f):
        f += ("0" * (4 - len(f) % 4)) if len(f) % 4 else ""
        return hex(int(f, 2))[2:] if f else ''

    return __int2hex(i) + ('.' + __float2hex(f) if __float2hex(f) else '')


def dec2bin(num):
    def __int2bin(i):
        return bin(i)[2:]

    def __float2bin(f):
        bins = []
        while f and len(bins) <= 52:
            f *= 2
            bins.append(1 if f >= 1. else 0)
            f -= int(f)
        return "".join([str(i) for i in bins])

    return __int2bin(int(num)) + ("." + __float2bin(num - int(num)) if __float2bin(num - int(num)) else '')


def dec2qua(num):
    # todo
    return num


def dec2oct(num):
    # todo
    return num


def dec2hex(num):
    return bin2hex(dec2bin(num))


if __name__ == '__main__':
    print(dec2bin(864*1536))
    print(bin2hex(101000100000000000000))
