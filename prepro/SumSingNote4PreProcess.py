#!usr/bin/python
# -*- coding:utf-8 -*-

from SumSingNote3PreProcess import *

#处理过程跟三星note3一样，所以直接继承三星note3处理类
class SumSingNote4PreProcess (SumSingNote3PreProcess):

    def __init__(self,tester):
        super(SumSingNote4PreProcess, self).__init__(tester)

    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
        try:
            # 新老注册流程的登录按钮使用的是同一个resource_id，对登录按钮不用做特殊判断
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            time.sleep(3)
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)

            time.sleep(3)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/password')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
            time.sleep(3)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            while self.tester.is_element_exist(u'手机号位数不对'):
                self.tester.find_element_by_id('com.nice.main:id/phone_number')

        except Exception,e:
            raise