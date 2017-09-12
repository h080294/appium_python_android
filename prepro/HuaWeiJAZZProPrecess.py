#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
from model import Tester
from prepro.HuaWeiG9PreProcess import *
from prepro.HUAWEIMT7PreProcess import *

class HuaWeiJAZZProPrecess(HuaWeiG9PreProcess):

    def __init__(self,tester):
        super(HuaWeiJAZZProPrecess, self).__init__(tester)
