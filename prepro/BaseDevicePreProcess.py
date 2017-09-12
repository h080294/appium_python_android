#!usr/bin/python
# -*- coding:utf-8 -*-

from common.DataProvider import *
from common.Log import *
import threading
import traceback
from common.DriverManager import *
from appium.webdriver.common.touch_action import TouchAction
import time
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from model.Tester import *
import subprocess


class BaseDevicePreProcess(object):

    def __init__(self, tester):
        self.tester = tester
        self.driver = self.tester.driver
        self.action = TouchAction(self.driver)
        self.user = self.tester.user

    # 开始预处理流程
    def pre_process(self):
        Log.logger.info(u"设备：%s 开始预处理流程..." % self.tester.device.devicename)
        driver = self.tester.driver
        try:
            if driver.is_app_installed('com.nice.main'):
                Log.logger.info(u"设备：%s 卸载老的nice包" % self.tester.device.devicename)
                driver.remove_app('com.nice.main')
            Log.logger.info(u"设备：%s 开始安装测试的nice包" % self.tester.device.devicename)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info(u"设备：%s 启动成功" % self.tester.device.devicename)
            self.login_process()
            Log.logger.info(u"设备：%s 登录成功" % self.tester.device.devicename)
            self.login_success_process()
            time.sleep(10)
            self.get_permission_process()
            time.sleep(3)
            self.tester.clean_mp4_file()     #预处理时清除sd的mp4文件
            Log.logger.info(u"设备：%s 预处理成功，开始执行测试用例" % self.tester.device.devicename)
        except  Exception, e:
            Log.logger.info(u"设备：%s 出现异常!" % self.tester.device.devicename)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        return True

    # 安装流程
    def install_app(self):
        self.driver.install_app(DataProvider.niceapk)

    # 版本升级
    def upgrade_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.nicelatestapk)
        subprocess.call(cmd, shell=True)

        time.sleep(5)
        self.driver.launch_app()

        self.tester.start_screen_record(u'直播礼物开屏')
        time.sleep(10)
        self.tester.stop_screen_record(u'直播礼物开屏')

    # 该流程包括处理安装及启动过程中的各种弹窗，一直到可以点击login按钮
    def install_process(self):
        pass

    # 该流程包括点击login按钮到达登录页面，并登录
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
            login_element = self.tester.find_element_by_id('com.nice.main:id/login')
            self.action.tap(login_element).perform()

            time.sleep(2)

            self.tester.screenshot(u"登录成功")
        except Exception,e:
            raise

    # 该流程包括登录成功后，对各种自动弹出对话框进行处理
    def login_success_process(self):
        pass

    # 对所有需要的权限进行处理，例如：相机、录音
    def get_permission_process(self):
        pass

    def check_user_profile_pic(self):
        self.tester.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
        self.tester.find_element_by_id_and_tap('com.nice.main:id/img_profile_avatar')
        time.sleep(3)
        if self.tester.is_element_exist('编辑头像'):
            print '该用户未添加头像'
            self.tester.find_element_by_id_and_tap('com.nice.main:id/img_publish_photo')
            time.sleep(3)
            if self.tester.is_element_exist('com.nice.main:id/image'):
                self.tester.find_element_by_uiautomator_and_tap('new UiSelector().resourceId(\"com.nice.main:id/image\").index(0)')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
                time.sleep(5)  # 上传头像到【我】页面
            else:
                Log.logger.info(u'上传头像失败')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        else:
            print '该用户已添加头像'
            self.tester.find_element_by_id_and_tap('com.nice.main:id/profile_black')

    # 创建autotest文件夹并生成测试图片
    def data_prepare(self):
        Log.logger.info(u"设备：%s 检查文件开始" % self.tester.device.devicename)
        if self.tester.is_autotest_exit():
            time.sleep(1)
        else:
            Log.logger.info(u"设备：%s 写入测试文件" % self.tester.device.devicename)
            self.tester.pull_file_to_device()
            time.sleep(10)
            self.tester.refresh_test_pic()









