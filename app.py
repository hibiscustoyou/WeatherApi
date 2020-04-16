# -*- coding: utf-8 -*-
"""
Created on 2020/4/12 16:47
Author  : zxt
File    : app.py
Software: PyCharm
"""


import pymysql
from flask import Flask, request, g
from WeatherCrawler.weather import Weather


app = Flask(__name__)
conn = pymysql.connect(
    host='localhost', user='zxt', password='990127zxtXhh', database='national_divisions', charset='gb2312'
)
cur = conn.cursor()


@app.route('/weather', methods=['get'])
def get_weather():
    district = request.args['district']
    data_type = request.args['data_type']
    try:
        sql = f'select town from towns where code = {int(district)}'
        cur.execute(sql)
        district = cur.fetchone()[0]
    except:
        pass
    weather, forecasts = Weather().get_weather(district)
    print(weather)
    if not weather['status']:
        if data_type == 'all':
            weather.update({'forecasts': forecasts, 'msg': 'success'})
            return weather

        if data_type == 'now' or not data_type:
            weather.update({'msg': 'success'})
            return weather
    return weather


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
