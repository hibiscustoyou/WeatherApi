# -*- coding: utf-8 -*-
"""
Created on 2020/4/11 17:23
Author  : zxt
File    : cnzz.py
Software: PyCharm
"""

import time
import random
from utils.HexConvert import dec2hex


def fa():

    def __a():
        _k = []
        _d = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/80.0.3987.163 Safari/537.36"
        _n = 0

        def __c(w, v):
            _y = 0
            for r in range(len(v)):
                _y |= _k[r] << 8 * r
            return w ^ _y

        for i in _d:
            _k.insert(0, ord(i) & 255)
            _n = __c(_n, _k)
            if len(_k) >= 4:
                _n = __c(_n, _k)
                _k = []

        if len(_k):
            _n = __c(_n, _k)

        return dec2hex(_n)

    def __b():
        ts = int(time.time() * 1000)
        d = 0
        while ts == int(time.time() * 1000):
            d += 1
        return dec2hex(ts) + dec2hex(d)

    r = dec2hex(random.random()).replace('.', '')

    return f"{__b()}-{r}-{__a()}-{dec2hex(864*1536)}-{__b()}"


if __name__ == '__main__':
    print(fa())
