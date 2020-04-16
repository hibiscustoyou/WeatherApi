# -*- coding: utf-8 -*-
"""
Created on 2020/1/21 19:56
Author  : zxt
File    : tran_headers.py
Software: PyCharm
"""


import json


def headers2dict(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in header_raw.split("\n"))


def dict2headers(header_dict):
    header_str = json.dumps(header_dict)
    return header_str.replace('{', '').replace('}', '').replace(', "', '\n').replace('"', '')


def str_format(s):
    return s.replace(' ', '').replace(';', ';\n')


if __name__ == '__main__':
    header_raw = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Host: www.weather.com.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53"""
    print(headers2dict(header_raw.strip()))

    header_dict = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8', 'content-length': '177', 'content-type': 'application/x-www-form-urlencoded', 'cookie': 'BAIDUID=0CA950A25601430FADEC2453A8327673:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1579616598; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%5D; __yjsv5_shitong=1.0_7_694715a07b489985eb4e38e052fa80967bb2_300_1579620185472_120.239.15.85_87aa9f8a; yjs_js_security_passport=2846de05a20b2cb005b506eae3fc944bb28dd5f5_1579620186_js; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1579626405; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1579626405; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1579626405', 'origin': 'https://fanyi.baidu.com', 'referer': 'https://fanyi.baidu.com/', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36', 'x-requested-with': 'XMLHttpRequest'}
    # print(dict2headers(header_dict))

    s = """
cookie: BAIDUID=B43BA21EC07B317C28DD96FB3DDF5603:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1579616598; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%5D; __yjsv5_shitong=1.0_7_694715a07b489985eb4e38e052fa80967bb2_300_1579620185472_120.239.15.85_87aa9f8a; yjs_js_security_passport=2846de05a20b2cb005b506eae3fc944bb28dd5f5_1579620186_js; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1579621545; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1579621545; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1579621545
"""
    # print(str_format(s))
