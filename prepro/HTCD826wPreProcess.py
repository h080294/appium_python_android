#coding=utf-8
from BaseDevicePreProcess import *

class HTCD826wPreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(HTCD826wPreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理安装" % self.tester.device.devicename)

            while self.tester.is_element_exist('com.htc:id/primary')==False:
                time.sleep(1)

            time.sleep(2)
            self.tester.press_keycode(4)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_process(self):
        self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
        self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
        self.tester.find_element_by_id_and_tap('com.nice.main:id/password')
        self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
        self.tester.press_keycode(4)
        self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

    def login_success_process(self):
        Log.logger.info(u"设备：%s 登录成功后，无需处理" % self.tester.device.devicename)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 无需处理" % self.tester.device.devicename)


