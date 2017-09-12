#usr/bin/python
#-*- coding:utf-8 -*-

from appium import webdriver
import MonkeyResultEmail
import share
from common.DeviceManager import *
from common.PreProManager import *
from common.TestCaseManager import *
from common.TheTestResult import *
import MonkeyResultWiki
import traceback


class RunTestManager(object):

    def __init__(self, mode):
        self.count_testcases = 0
        self.task_id = int(time.time())
        self.logger = Log.logger
        self.mode = mode

    def start_run(self):
        try:
            self.logger.debug('Start run %s...' % self.mode)
            if self.mode == "autotest":
                TheTestResult.create_result_folder()

            if self.mode == "monkey":
                Tester.is_exit_monkeyresultfile()
                Tester.create_monkey_result()

            Log.logger.info(u"开始执行任务...")
            self.start_run_test()

            if self.mode == "autotest":
                Log.logger.debug(u'开始生成测试报告...')
                TheTestResult.generate_html_testresult()

            if self.mode == "monkey":
                #读取本次monkey结果文件夹下的所有log
                Tester.open_filelist()
                Tester.read_log()
                time.sleep(10)
                MonkeyResultWiki.login_and_post("参数")
                MonkeyResultEmail.run()

            Log.logger.info(u"完成测试并退出所有Driver")
            # DriverManager.quit_all_driver()
            self.stop_run()
        except Exception, e:
            traceback.print_exc()
            self.stop_run()

    def stop_run(self):
        share.set_if_run(False)

    def run(self, tester):
        try:
            DataProvider.starttime[tester.device.deviceid] = get_format_currenttime()
            tester.show_relationship()
            # 开始设备预处理流程
            if PreProManager(tester).device().pre_process():
                if self.mode == "monkey":
                    Log.logger.info(u"设备：%s ---开始执行monkey---" % tester.device.devicename)
                    suite = TestCaseManager(tester).monkey_android()
                    Log.logger.info(u"设备：%s ---monkey执行结束---" % tester.device.devicename)

                elif self.mode == "autotest":
                    tester.clean_mp4_file()  #清理sd卡DCIM文件夹中的mp4文件
                    Log.logger.info(u"设备：%s ---开始执行autotest---" % tester.device.devicename)
                    tester.pic_data_prepare()  #判断手机是否有autotest图库
                    tester.video_data_prepare()  # 判断手机是否有auto_video视频
                    Log.logger.info(u"设备：%s 开始Load测试用例..." % tester.device.devicename)
                    suite = TestCaseManager(tester).compatibility_testsuite()
                    #suite = TestCaseManager(tester).signal_case_suit(test_show_pub_video)
                    Log.logger.info(u"设备：%s 测试用例Load完成" % tester.device.devicename)
                    Log.logger.info(u"设备：%s 开始执行测试用例..." % tester.device.devicename)
                    unittest.TextTestRunner(verbosity=2, resultclass=TheTestResult).run(suite)
                    Log.logger.info(u"设备：%s 测试用例执行完成" % tester.device.devicename)
            else:
                Log.logger.info(u"设备：%s 预处理流程失败，终止相应任务" % tester.device.devicename)

            DataProvider.stoptime[tester.device.deviceid] = get_format_currenttime()

        except Exception,e:
            Log.logger.info(u"设备：%s 出现异常" % tester.device.devicename)
            traceback.print_exc()

    def init_tester_data(self, device, which_user):
        try:
            desired_caps = {}
            desired_caps['platformName'] = device.platformname
            desired_caps['platformVersion'] = device.platformversion
            desired_caps['deviceName'] = device.devicename
            desired_caps['unicodeKeyboard'] = "true"
            desired_caps['resetKeyboard'] = 'true'
            desired_caps['autoLaunch'] = "false"
            desired_caps['appPackage'] = 'com.nice.main'
            desired_caps['appActivity'] = 'com.nice.main.activities.MainActivity_'
            desired_caps['udid'] = device.deviceid
            desired_caps['newCommandTimeout'] = "3000"
            desired_caps['unicodeKeyboard'] = True
            desired_caps['resetKeyboard'] = True
            url = "http://%s:%s/wd/hub" % (device.server, device.serverport)
            driver = webdriver.Remote(url, desired_caps)

            if self.mode=="autotest":
                # 创建每个设备的截图文件夹
                folderpath = '%s/%s' % (TheTestResult.testresultpath, device.devicename)
                os.mkdir(folderpath)

            testerobject = Tester(driver)
            testerobject.device = device
            testerobject.user = DataProvider.users[which_user]
            testerobject.logger = Log.logger
            if self.mode=="autotest":
                testerobject.screenshot_path = folderpath

            DriverManager.drivers[device.deviceid] = driver
            return testerobject
        except Exception,e:
            Log.logger.info(u"设备：%s 出现异常" % device.devicename)
            traceback.print_exc()

    def start_run_test(self):
        which_user = 0
        threads = []
        for deviceid, device in DeviceManager.serverdevices.iteritems():
            testerobject = self.init_tester_data(device, which_user)
            DataProvider.testers[device.deviceid] = testerobject
            try:
                thread = threading.Thread(target=self.run, args=(testerobject,))
                thread.start()
                which_user = which_user + 1
                threads.append(thread)
            except Exception, e:
                traceback.print_exc()
                DataProvider.testers[deviceid].driver.quit()

        for thread in threads:
            thread.join()