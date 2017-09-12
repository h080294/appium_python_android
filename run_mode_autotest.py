#!usr/bin/python
# -*- coding:utf-8 -*-

import requests

def main():
    url = 'http://127.0.0.1:8886/run?mode=autotest'
    response = requests.get(url)
    resjson = response.json()
    print resjson

if __name__ == '__main__':
    main()



