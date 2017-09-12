#!usr/bin/python
# -*- coding:utf-8 -*-

import sys

from common.ApkBase import ApkInfo
from model.Teststeps import *

sys.path.append('..')
from common.BaseTestCase import *


class test_longpress(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_longpress_0(self):
        print "美颜"

    def test_longpress_1(self):
        time.sleep(5)
        self.tester.back_to_feed()
        print "返回feed"

    # 主动skip case
    def test_longpress_2(self):
        time.sleep(1)
        self.skipTest("hahha")

    # 主动fail case
    def test_longpress_3(self):
        time.sleep(1)
        self.fail("manual")

    def test_longpress_4(self):
        time.sleep(1)
        print "End 4 ~~~~~"

    def tearDown(self):
        pass

    # 请reset到feed页面
    @classmethod
    def tearDownClass(cls):
        pass
