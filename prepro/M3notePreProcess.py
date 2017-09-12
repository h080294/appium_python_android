#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *

class M3notePreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(M3notePreProcess, self).__init__(tester)

    #魅族情况太特殊，安装都得继承然后单独处理,弹出的adb安装权限直接阻塞了Server运行
    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)


    def install_process(self):

        Log.logger.info(u"设备：%s 安装app并处理GPS弹窗" % self.tester.device.devicename)
        try:
            #adb
            element = self.tester.find_element_by_id("android:id/button1",20)
            if element != None:
                self.action.tap(element).perform()

            # 启动app
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

            # nice获取手机GPS权限
            element = self.tester.find_element_by_id("android:id/button1",20)
            if element != None:
                self.action.tap(element).perform()

            # nice获取手机识别码权限
            element = self.tester.find_element_by_id("android:id/button1",10)
            if element != None:
                self.action.tap(element).perform()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
        try:
            # 新老注册流程的登录按钮使用的是同一个resource_id，对登录按钮不用做特殊判断

            #先获得注册页面的login按钮对象
            register_login_element = self.tester.find_element_by_id('com.nice.main:id/login')

            #点击登录
            self.action.tap(register_login_element).perform()

            time.sleep(2)

            login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number',2)
            while login_phone_number_element == None:
                self.action.tap(register_login_element).perform()
                time.sleep(2)
                login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number',2)

            #输入账号密码
            login_phone_number_element.send_keys(self.user.mobile)
            login_password = self.tester.find_element_by_id('com.nice.main:id/password')
            self.action.tap(login_password).perform()
            login_password.send_keys(self.user.password)

            #判断直到登录成功
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            time.sleep(5)
            self.tester.screenshot(u"登录成功")
        except Exception,e:
            raise

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            #联系人权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)

            #打开取景窗
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #通讯录权限
            self.tester.find_element_by_id_and_tap('android:id/button1')
            # 录音权限
            time.sleep(2)
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
