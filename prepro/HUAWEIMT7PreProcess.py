#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
from prepro.HuaWeiG9PreProcess import *

class HUAWEIMT7PreProcess (HuaWeiG9PreProcess):

    def __init__(self, tester):
        super(HUAWEIMT7PreProcess, self).__init__(tester)
