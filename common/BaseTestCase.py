#!usr/bin/python
# -*- coding:utf-8 -*-

import unittest
import time
import os
import traceback
from Log import *


class BaseTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', tester=None):
        super(BaseTestCase, self).__init__(methodName)
        self.tester = tester

    @staticmethod
    def parametrize(testcase_klass, tester=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, tester=tester))
        return suite
