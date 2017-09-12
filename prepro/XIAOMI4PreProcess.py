#coding=utf-8
from BaseDevicePreProcess import *

class XIAOMI4PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(XIAOMI4PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            time.sleep(3)
            self.tester.find_element_by_id_and_tap('com.miui.securitycenter:id/do_not_ask_checkbox')

            self.tester.find_element_by_id_and_tap('android:id/button2')

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    # def login_process(self):
    #     Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
    #     try:
    #
    #
    #         # self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
    #         time.sleep(10)
    #         self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
    #         self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
    #         self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
    #
    #         time.sleep(3)
    #
    #         self.tester.longin_with_verifycode()
    #         self.tester.screenshot(u"登录成功")
    #     except Exception,e:
    #         raise
    #

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            # 授权通讯录弹框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

            #授权联系人权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

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


            # 摄像头权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

