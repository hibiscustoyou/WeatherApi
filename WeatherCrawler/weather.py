# -*- coding: utf-8 -*-
"""
Created on 2020/4/10 22:28
Author  : zxt
File    : weather.py
Software: PyCharm
"""

import json
import re
import os
import time
import requests
import pymysql
from pyquery import PyQuery as pq
from calendar import weekday

from utils.cnzz import fa


def _week(date):
    weeks = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    y, m, d = date.split('-')
    return weeks[weekday(int(y), int(m), int(d))]


def _replace(kw, rp, val=''):
    if not rp:
        return kw
    for r in rp:
        kw = kw.replace(r, val)
    return kw


class Weather:
    def __init__(self):

        ts = int(time.time())
        today = int(time.strftime('%Y%m%d', time.localtime()))

        with open(os.path.abspath(os.path.join(os.path.abspath(__file__), "../../config.json")), 'r') as f:
            db = json.load(f)["DB"]

        conn = pymysql.connect(
            host=db['host'], user=db['user'], password=db['password'], database=db['database'], charset=db['charset']
        )
        self.cur = conn.cursor()

        self.headers = {
            'Cookie': f'Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b={ts}; '
                      f'cityListCmp=%E5%8C%97%E4%BA%AC-101010100-{today}%7C%E4%B8%8A%E6%B5%B7-101020100-{today + 1}'
                      f'%7C%E5%B9%BF%E5%B7%9E-101280101-{today + 2}%7C%E6%B7%B1%E5%9C%B3-101280601-{today + 3}'
                      f'%2Cdefault%2C{today}; '
                      f'cityListHty=101010100%7C101020100%7C101280101%7C101280601%7C101010300; '
                      f'f_city=%E6%B1%95%E5%A4%B4%7C101280501%7C; '
                      f'UM_distinctid={fa()}; '
                      f'f_city=%E6%B1%95%E5%A4%B4%7C101280501%7C; Wa_lvt_1={ts}; Wa_lpvt_1={ts}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.163 Safari/537.36'
        }

    def search(self, kw):
        url = 'http://toy1.weather.com.cn/search'
        params = {
            'cityname': kw,
            'callback': 'success_jsonpCallback',
            '_': int(time.time() * 1000)
        }
        _headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'toy1.weather.com.cn',
            'Referer': 'http://www.weather.com.cn/'
        }.update(self.headers)
        res = requests.get(url, params=params, headers=_headers)
        code = re.findall(r'(\d+)', res.text[22:50])
        return code[0] if code else ''

    def __now(self, doc):
        now_weather = doc('.cur')('i')
        now = {
            'text': now_weather.attr('title'),
            'icon': f"http://i.tq121.com.cn/i/weather2014/png/blue_40/{now_weather.attr('class').split(' ')[-1]}.png",
            'temp': int(doc('.temp').text()),
            'relative_humidity': 0,
            'wind_class': '',
            'wind_dir': '',
            'uptime': doc('.time span').text().replace('实况', ''),
            'request_time': time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
        }

        p = doc('.todayLeft p')
        now['wind_dir'], now['wind_class'] = p.eq(0)('span').text().split(' ')
        _, now['relative_humidity'] = p.eq(1)('span').text().split(' ')

        return now

    def __location(self, kw):

        location = {
            'province': '',
            'city': '',
            'county': '',
            'town': '',
            'code': ''
        }
        sql = f'SELECT * FROM towns WHERE town like "%{kw}%" or county like "%{kw}%" or city like "%{kw}%"'
        self.cur.execute(sql.replace("(\'", "").replace("\',)", ""))
        data = self.cur.fetchone()
        if data:
            location = dict(zip(('province', 'city', 'county', 'town', 'code'), list(data)[1:]))

        # print(type(location['province']))
        # print(type(location['city']))

        code = str(location['code'])
        if kw in location['city']:
            location['county'] = ''
            location['town'] = ''
            location['code'] = int(code[:4] + '0'*(len(code) - 4))
        elif kw in location['county']:
            location['town'] = ''
            location['code'] = int(code[:6] + '0'*(len(code) - 6))
        else:
            location['code'] = int(code[:8] + '0'*(len(code) - 8))

        return location

    def __forecasts(self, url, headers):
        forecasts = []

        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        doc = pq(res.text)
        cur_month = time.strftime("%Y-%m-", time.localtime())

        weather_info = doc('.weather-info')
        blue_item = doc('.blue-item')
        date_items = doc('.date')

        event_day = re.findall(
            r'event.*\[.*?\]', res.text
        )[0].replace('eventDay = ', '').replace(' ', '').replace('"', '')[1:-1].split(',')
        event_night = re.findall(
            r'event.*\[.*?\]', res.text
        )[1].replace('eventDay = ', '').replace(' ', '').replace('"', '')[1:-1].split(',')

        for i in range(1, date_items.length):
            icons = blue_item.eq(i)('i')
            icon_day, icon_night = [
                f"http://i.tq121.com.cn/i/weather2014/png/blue_40/{icons.eq(idx).attr('class').split(' ')[1]}.png"
                for idx in [0, 1]
            ]

            info = weather_info.eq(i).text().split('转')
            date = cur_month + date_items.eq(i).text().replace('日', '')

            wc = blue_item.eq(i)('.wind-info')
            wc_day, wc_night = wc.text().split('转') if wc.length == 2 else wc.text(), wc.text()
            wind = blue_item.eq(i)('.wind-container .wind-icon')
            wd_day, wd_night = wind.eq(0).attr('title'), wind.eq(1).attr('title')

            week = _week(date)

            forecast = {
                'day': {
                    'text': info[0],
                    'icon': icon_day,
                    'wc': wc_day,
                    'wd': wd_day
                },
                'night': {
                    'text': info[-1],
                    'icon': icon_night,
                    'wc': wc_night,
                    'wd': wd_night
                },
                'highest_temp': int(event_day[i]),
                'lowest_temp': int(event_night[i]),
                'date': date,
                'week': week
            }
            # forecast = {
            #     'text_day': info[0],
            #     'text_night': info[-1],
            #     'highest_temp': int(event_day[i]),
            #     'lowest_temp': int(event_night[i]),
            #     'wc_day': wc_day,
            #     'wd_day': wd_day,
            #     'wc_night': wc_night,
            #     'wd_night': wd_night,
            #     'date': date,
            #     'week': week
            # }
            forecasts.append(forecast)

        return forecasts

    def __weather24h(self, doc):
        hours = []
        for li in doc('#weatherALL li').items():
            hour = {
                'time': li('.time').text(),
                'text': li('i').attr('title'),
                'icon': f"http://i.tq121.com.cn/i/weather2014/png/blue_40/{li('i').attr('class').split(' ')[-1]}.png",
                'temp': int(doc('.temp').text()),
                'wind_class': li('.windL').text(),
                'wind_dir': li('.wind').text()
            }
            hours.append(hour)
        return hours

    def get_weather(self, kw, *, t='all'):
        kw = _replace(kw, ['市', '区', '县', '镇', '村'])
        try:
            weather_code = self.search(kw)
            url = f'http://forecast.weather.com.cn/town/weather1dn/{weather_code}.shtml#input'
            _headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                          'q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'forecast.weather.com.cn',
                'Referer': 'http://www.weather.com.cn/',
                'Upgrade-Insecure-Requests': '1'
            }.update(self.headers)

            weather_detail = {
                'status': 0,
                'result': {
                    'location': {},
                    'now': {}
                }
            }

            res = requests.get(url, headers=_headers)
            res.encoding = 'utf-8'
            doc = pq(res.text)

            weather_detail['result']['location'] = self.__location(kw)
            weather_detail['result']['now'] = self.__now(doc)
            if t == 'now':
                return weather_detail
            elif t == 'all':
                forecasts = self.__forecasts(
                    f'http://forecast.weather.com.cn/town/weathern/{weather_code}.shtml#input',
                    _headers
                )
                weather_detail['result']['forecasts'] = forecasts
                weather_detail['result']['weather24h'] = self.__weather24h(doc)
                return weather_detail
        except Exception as e:
            print(e)
            return {
                'status': 1,
                'msg': '查询失败，请检查您的查询地点是否有误',
            }, []


if __name__ == '__main__':
    weather = Weather()
    print(weather.get_weather("雷岭"))
    # weather.get_weather("潮南")
    # print(weather.get_weather("xxx"))
    # print(_replace('汕头市', ['市', '区', '县', '镇', '村']))
    # print(_replace('潮南区', ['市', '区', '县', '镇', '村']))
    # print(_replace('雷岭镇', ['市', '区', '县', '镇', '村']))
    # print(_replace('东老村', ['市', '区', '县', '镇', '村']))
