#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
from model import Tester

class HuaWeiG9PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(HuaWeiG9PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    # 开始预处理流程
    def pre_process(self):
        Log.logger.info(u"设备：%s 开始预处理流程..." % self.tester.device.devicename)
        driver = self.tester.driver
        try:
            if driver.is_app_installed('com.nice.main'):
                Log.logger.info(u"设备：%s 卸载老的nice包" % self.tester.device.devicename)
                driver.remove_app('com.nice.main')

            if self.tester.is_element_exist('android:id/button1',30):
                self.tester.find_element_by_id_and_tap('android:id/button1')

            Log.logger.info(u"设备：%s 开始安装测试的nice包" % self.tester.device.devicename)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info(u"设备：%s 启动成功" % self.tester.device.devicename)
            self.login_process()
            Log.logger.info(u"设备：%s 登录成功" % self.tester.device.devicename)
            self.login_success_process()
            self.get_permission_process()
            time.sleep(3)
            self.tester.clean_mp4_file()  # 预处理时清除sd的mp4文件
            Log.logger.info(u"设备：%s 预处理成功，开始执行测试用例" % self.tester.device.devicename)
        except  Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        return True

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            if self.tester.is_element_exist('com.android.packageinstaller:id/decide_to_continue',10) == True:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/decide_to_continue')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/goinstall')
            elif self.tester.is_element_exist('com.android.packageinstaller:id/ok_button',10) == True:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/ok_button')
            else :
                print 'error!'
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            # 该流程包括点击login按钮到达登录页面，并登录
        finally:
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

            # 获取定位权限
            self.tester.find_element_by_id_and_tap('com.huawei.systemmanager:id/btn_allow')

    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
        try:
            # 新老注册流程的登录按钮使用的是同一个resource_id，对登录按钮不用做特殊判断
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)

            self.tester.press_keycode(4)

            time.sleep(1)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            time.sleep(1)
            self.tester.screenshot(u"登录成功")
        except Exception, e:
            raise

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            #授权sd卡
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            #授权位置信息
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            #授权通讯录
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

            time.sleep(5)
            if self.tester.is_element_exist('com.android.packageinstaller:id/permission_allow_button'):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            time.sleep(5)
            if self.tester.is_element_exist('com.nice.main:id/btn_know'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_know')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')


            # 切换到拍摄tab
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            time.sleep(1)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)