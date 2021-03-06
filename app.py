# -*- coding: utf-8 -*-
"""
Created on 2020/4/12 16:47
Author  : zxt
File    : app.py
Software: PyCharm
"""
import json
import os

import pymysql
from flask import Flask, request, g
from WeatherCrawler.weather import Weather


app = Flask(__name__)

with open(os.path.abspath(os.path.join(os.path.abspath(__file__), "../config.json")), 'r') as f:
    data = json.load(f)
    db = data["DB"]
    port = data["port"]
conn = pymysql.connect(
    host=db['host'], user=db['user'], password=db['password'], database=db['database'], charset=db['charset']
)
cur = conn.cursor()


@app.route('/weather', methods=['get'])
def get_weather():
    district = request.args['district'].lower()
    data_type = request.args['data_type'].lower()
    try:
        sql = f'select town from towns where code = {int(district)}'
        cur.execute(sql)
        district = cur.fetchone()[0]
    except:
        pass
    weather = Weather().get_weather(district, t=data_type)
    print(weather)
    if not weather['status']:
        weather.update({'msg': 'success'})
        return weather
    return weather


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
