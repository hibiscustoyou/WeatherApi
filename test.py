# -*- coding: utf-8 -*-
"""
Created on 2020/4/11 1:31
Author  : zxt
File    : test.py
Software: PyCharm
"""

import requests
import os
from locust import HttpLocust, TaskSet, task, between
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings


disable_warnings(InsecureRequestWarning)


class WeatherApiTest(TaskSet):

    @task(1)
    def get_api(self):
        # req = self.client.get(
        #     'http://111.230.151.193:5001/weather?district=雷岭镇&data_type=all',
        # )
        url = 'http://111.230.151.193:5001/weather?district=雷岭镇&data_type=all'
        res = requests.get(url)
        data = res.json()
        if res.status_code == 200:
            print('success', data)
        else:
            print('error')


class WebUser(HttpLocust):
    task_set = WeatherApiTest
    wait_time = between(3, 6)


def get_api():
    url = 'http://111.230.151.193:5001/weather?district=雷岭镇&data_type=all'
    res = requests.get(url)
    data = res.json()
    print()


# if __name__ == '__main__':
#     os.system('locust -f test.py --host=http://111.230.151.193:5001')
