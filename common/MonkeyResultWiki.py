#!/usr/bin/env python
# coding: utf-8

import re
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
from model.Tester import *
from common.PublicMethod import *


def login_and_post(loginPage, requestUrl, user, password):
    try:
        # 设置cookie
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')]
        urllib2.install_opener(opener)

        # 登录
        login_data = {
            "os_username": user,
            "os_password": password,
            "os_cookie": "true",
            "login": "登录",
            "os_destination": ""}
        login_data = urllib.urlencode(login_data)
        req = urllib2.Request(loginPage, login_data)
        conn = urllib2.urlopen(req)


        # 登录成功后打开指定页面
        point_url = urllib2.urlopen(requestUrl).read()
        # print point_url

        soup = BeautifulSoup(
            point_url,  # 文档字符串
            'html.parser',  # 解析器
            from_encoding='utf-8'  # 文档编码
        )
        token = soup.find_all('meta', id ='atlassian-token')
        token_content=token[0].attrs['content']
        print token_content    #获取token值

        draftId = soup.find_all('input', id='draftId')
        draftId_result=draftId[0].attrs['value']
        print draftId_result    #获取draftId

        entityId = soup.find_all('input', id='entityId')
        entityId_result=entityId[0].attrs['value']
        print entityId_result    #获取entityId

        # 读取monkey结果Summary.txt文件中的内容
        for listdir in Tester.lis:
            if 'Summary' in listdir:
                file = open(listdir, 'rb')
                filedata = file.read()
                file.close()

        # 向Android Monkey AutoTest Tracking页面提交form表单数据
        pagedata={
                "atl_token": "%s" % token_content,
                "fromPageId": "8770164",
                "spaceKey": "ANDROID",
                "labelsString":"",
                "titleWritten":"false",
                "linkCreation":"false",
                "title":"%s" % get_format_currenttime(),
                "wysiwygContent":"%s" % filedata,
                "confirm":"Save",
                "parentPageString":"Android Monkey AutoTest Tracking",
                "moveHierarchy": "true",
                "position":"",
                "targetId":"",
                "draftId":"%s" % draftId_result,
                "entityId":"%s" % entityId_result,
                "newSpaceKey":"ANDROID"
        }

        postdata = urllib.urlencode(pagedata)
        Url='http://wiki.niceprivate.com/pages/docreatepage.action'
        req2 = urllib2.Request(url=Url, data=postdata)
        # 查看表单提交后返回内容
        response = urllib2.urlopen(req2)

    except Exception, e:
        print str(e)


if __name__ == '__main__':
    loginUrl = 'xxxxxxx'
    user = 'xxxxxx'
    password = 'xxxxxx'
    requestUrl = 'xxxxxxx'

    # 登录测试
    login_and_post(loginUrl, requestUrl, user, password)


