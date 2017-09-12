#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *

class ChuiZi_YQ607PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(ChuiZi_YQ607PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 安装app并处理GPS弹窗" % self.tester.device.devicename)

            #启动app
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

            #获取位置信息
            time.sleep(5)
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            # 该流程包括点击login按钮到达登录页面，并登录

    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
        try:
            # 新老注册流程的登录按钮使用的是同一个resource_id，对登录按钮不用做特殊判断
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/password')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            time.sleep(1)
            self.tester.screenshot(u"登录成功")
        except Exception, e:
            raise
    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            element = self.tester.find_element_by_id("android:id/button1")
            if element != None:
                self.action.tap(element).perform()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)

            #打开取景窗
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            time.sleep(3)
            # 权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)