#!usr/bin/python
# -*- coding:utf-8 -*-
from  BaseTestCase import *
from model.Device import *


class TestCaseManager(object):

    def __init__(self, tester):
        self.compatibility_suite = unittest.TestSuite()
        self.testcase_class = []
        self.load_case()
        self.tester = tester

    def load_case(self):
        testcase_array = []
        testsuits = unittest.defaultTestLoader.discover('testcase/', pattern='test*.py')
        for testsuite in testsuits:
            for suite in testsuite._tests:
                for test in suite:
                    testcase_array.append(test.__class__)
        self.testcase_class = sorted(set(testcase_array), key=testcase_array.index)

    # 兼容性测试用例
    def compatibility_testsuite(self):
        for testcase in self.testcase_class:
            self.compatibility_suite.addTest(BaseTestCase.parametrize(testcase, tester=self.tester))
        return self.compatibility_suite

    #monkey自动化
    def monkey_android(self):
        self.tester.run_monkey(200,1000)

    # 功能性测试用例
    def functional_testsuite(self):
        pass

    def signal_case_suit(self, test_myclass):
        suite = unittest.TestSuite()
        suite.addTest(BaseTestCase.parametrize(test_myclass, tester=self.tester))
        return suite
