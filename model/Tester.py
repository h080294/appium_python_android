#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import random
import subprocess
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import *
import time
import platform
import tempfile
import shutil
import math
import operator
from PIL import Image
from common.DataProvider import DataProvider
from common.PublicMethod import *
import traceback

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Tester(object):
    def __init__(self, driver):
        self._driver = driver
        self._user = None
        self._device = None
        self._logger = None
        self.action = TouchAction(self._driver)
        self._screenshot_path = ""
        self.device_width = self._driver.get_window_size()['width']
        self.device_height = self._driver.get_window_size()['height']

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def screenshot_path(self):
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, value):
        self._screenshot_path = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def show_relationship(self):
        self.logger.info(u"设备与登陆号码对应关系%s ----- %s" % (self.device.devicename, self.user.mobile))

    def swipe_screen(self, startx, starty, endx, endy, duration=500):
        self.logger.info(u"设备：%s swipe from point x:%s y:%s to x:%s y:%s"
                         % (self.device.devicename, startx, starty, endx, endy))
        self.driver.swipe(startx, starty, endx, endy, duration=500)

    def tap_screen(self, x, y):
        self.logger.info(u"设备：%s tap screen point at x:%s y:%s" % (self.device.devicename,x,y))
        self.action.tap(None, x, y).perform()

    def get_screen_center(self):
        x=self.device_width / 2
        y=self.device_height / 2

        y1 = 10

        self.swipe_screen(x,y,x,y1)

    def tap_screen_center(self):
        x = self.device_width/2
        y = self.device_height/2
        self.logger.info(u"设备：%s tap center of the screen point at x:%s y:%s" % (self.device.devicename, x, y))
        self.action.tap(None, x, y).perform()

    def long_press_screen(self, eleid, duration):
        el = self.driver.find_element_by_id(eleid)
        time.sleep(1)
        self.logger.info(u"设备：%s 长按控件 %s %s 毫秒" % (self.device.devicename, eleid, duration))
        self.action.long_press(el).wait(duration).release().perform()

    def screenshot(self, name):
        path = "%s/%s.png" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info(u"设备：%s screen shot at path:%s" % (self.device.devicename, path))

    def screenshot2(self, name):
        path = "%s/%s.jpg" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info(u"设备：%s screen shot at path:%s" % (self.device.devicename, path))

    def start_screen_record(self, name):
        """开始录制屏幕操作
        完成操作之后，要执行stop_screen_record()方法
        系统默认最长180秒，请在180秒内完成所有操作

        :Args:
         - name - 要保存的文件的名字，支持中文
        :Usage:
            self.tester.strat_screen_record(u'录制视频测试')
        """
        start_record = "adb -s %s shell screenrecord /sdcard/DCIM/%s.mp4" % (self.device.deviceid, name)
        self.logger.info(u"设备：%s screen record started" % self.device.devicename)
        subprocess.Popen(start_record, shell=True)

    def stop_screen_record(self, name):
        """结束录制屏幕操作
        注意！！！！！
        参数的name值一定要和strat_screen_record() 中的name值一致

        :Args:
         - name - 与 strat_screen_record()中传递的name一致
        :Usage:
            self.tester.strat_screen_record(u'录制视频测试')
            Your code here
            self.tester.stop_screen_record(u'录制视频测试')
        """
        self.logger.info(u"设备：%s screen record is stopping" % self.device.devicename)
        keyword = 'screenrecord'
        cmd_pid = "ps -e| grep adb |awk '{if($6=/%s/ && $8=/%s/)print $1}'" % (self.device.deviceid, keyword)
        pid = os.popen(cmd_pid).read()
        kill_pid = "kill -9 %s" % pid
        subprocess.Popen(kill_pid, shell=True)
        time.sleep(3)
        cmd_file = "adb -s %s shell ls /sdcard/DCIM/ |grep %s" % (self.device.deviceid, name)
        name = os.popen(cmd_file).read().strip('\r\n')
        path = "%s/%s" % (self.screenshot_path, name)
        cmd_pull = "adb -s %s pull /sdcard/DCIM/%s %s" % (self.device.deviceid, name, self.screenshot_path)
        subprocess.Popen(cmd_pull, shell=True)

    def clean_mp4_file(self):
        clean_cmd = "adb -s %s shell rm /sdcard/DCIM/*.mp4" % self.device.deviceid
        self.logger.info(u"设备：%s 清理sd卡录制的mp4文件" % self.device.devicename)
        subprocess.Popen(clean_cmd, shell=True)

        print 'clean done'

    def find_element_by_id(self,eleid,timeout=120):
        self.logger.info(u"设备：%s start find :%s" % (self.device.devicename, eleid))
        try:
            element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
            return element
        except Exception,e:
            self.logger.info(u"设备：%s 出现异常!" % self.device.devicename)
            traceback.print_exc()
            return None

    def find_element_by_id_and_tap(self, eleid,timeout=120,taptimes=1):
        self.logger.info(u"设备：%s start tap :%s" % (self.device.devicename, eleid))
        try:
            element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
            if element != None:
                if taptimes == 1:
                    self.action.tap(element).perform()
                    self.logger.info(u"设备：%s tap success :%s " % (self.device.devicename, eleid))
                elif taptimes > 1:
                    for x in range(taptimes):
                        self.action.tap(element).perform()
                        self.logger.info(u"设备：%s tap success :%s " % (self.device.devicename, eleid))
        except TimeoutException,e:
            self.logger.info(u"设备：%s 出现异常!" % self.device.devicename)
            traceback.print_exc()

    def find_element_by_uiautomator(self, uiselector, timeout=200):
        self.logger.info(u"设备：%s start find element uiselector:%s" % (self.device.devicename, uiselector))
        element = self.wait_element_uiautormator_display(self.driver, uiselector, uiselector, timeout)
        return element

    def find_element_by_uiautomator_and_tap(self, uiselector, timeout=200):
        self.logger.info(u"设备：%s start tap element uiselector:%s" % (self.device.devicename, uiselector))
        element = self.wait_element_uiautormator_display(self.driver, uiselector, uiselector, timeout)
        if element != None:
            self.action.tap(element).perform()
            self.logger.info(u"设备：%s tap success :%s " % (self.device.devicename, uiselector))

    def find_element_by_id_and_send_keys(self, eleid, text, timeout=200):
        self.logger.info(u"设备：%s start send_key %s to element id:%s" % (self.device.devicename, text, eleid))
        element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
        if element != None:
            element.send_keys(text)
            self.logger.info(u"设备：%s send_key text:%s to element id:%s success "
                             % (self.device.devicename, text, eleid))

    def find_element_by_class_name_and_tap(self, class_name, timeout=200):
        self.logger.info(u"设备：%s start tap element class name:%s" % (self.device.devicename, class_name))
        element = self.wait_element_id_display(self.driver, class_name, class_name, timeout)
        if element != None:
            self.action.tap(element).perform()
            self.logger.info(u"设备：%s tap element id:%s success" % (self.device.devicename, class_name))

    def wait_element_id_display(self, driver, idstr, msg, timeout=200):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, idstr)), msg)
        except TimeoutException, e:
            raise

    def wait_element_uiautormator_display(self, driver, uiselector, msg, timeout=200):
        try:
            return WebDriverWait(driver, timeout).until(lambda dr: dr.find_element_by_android_uiautomator(uiselector))
        except TimeoutException, e:
           raise

    def find_element_by_xpath_and_tap(self, xpath):
        self.logger.info(u"设备：%s find by xpath:%s" % (self.device.devicename, xpath))
        element = self.driver.find_element_by_xpath(xpath)
        self.action.tap(element).perform()

    def wait_element(self, eleid, timeout=200):
        self.logger.info(u"设备：%s wait element: %s" % (self.device.devicename, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            self.logger.info(u"设备：%s element id have displayed:%s" % (self.device.devicename, eleid))
        else:
            self.logger.info(u"设备：%s Timeout: wait element %s" % (self.device.devicename, eleid))

    def press_keycode(self, keycode, metastate=None):
        """发送keycode到设备中。仅限Android设备
        更多关于keycode请参考
        http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - 要发送的keycode值
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.press_keycode(24)
        """
        self.logger.info(u"设备：%s [action]按系统按键(keycode='%s')"
                         % (self.device.devicename, keycode))
        self.driver.press_keycode(keycode)

    # 目前系统的keycode按键长按只有500ms，暂时并不符合需求
    def long_press_keycode(self, keycode, metastate=None):
        """发送长按keycode事件到设备中。仅限Android设备
        Android only.

        :Args:
         - keycode - 要发送的keycode值
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.long_press_keycode(24)
        """
        self.logger.info(u"设备：%s [action]长按系统按键(keycode='%s')"
                         % (self.device.devicename, keycode))
        self.driver.long_press_keycode(keycode)

    def swipe_left(self, duration=None):
        """Perform a swipe left full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_left()
        """
        self.logger.info(u"设备：%s [action]向左滑动屏幕 " % self.device.devicename)
        startx = self.device_width - 10
        starty = self.device_height/2
        endx = 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy)

    def fast_swipe_left(self):
        """快速左滑
        :Args:
            - None
        :Usage:
            self.tester.fast_swipe_left()
        """
        self.logger.info(u"设备：%s [action]向左滑动屏幕 " % self.device.devicename)
        startx = self.device_width - 10
        starty = self.device_height/2
        endx = 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy, duration=200)

    def swipe_right(self, duration=None):
        """Perform a swipe right full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_right()
        """
        self.logger.info(u"设备：%s [action]向右滑动屏幕 " % self.device.devicename)
        startx = 10
        starty = self.device_height/2
        endx = self.device_width - 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy)

    def fast_swipe_right(self):
        """快速右滑
        :Args:
            - None
        :Usage:
            self.tester.fast_swipe_right()
        """
        self.logger.info(u"设备：%s [action]向右滑动屏幕 " % self.device.devicename)
        startx = 10
        starty = self.device_height/2
        endx = self.device_width - 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy, duration=200)
        time.sleep(2)

    def swipe_down(self, duration=None):
        """Perform a swipe down full screen width
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(u"设备：%s [action]向上滑动屏幕 " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height/3
        endx = self.device_width/2
        endy = 10
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def swipe_down_refresh(self):
        startx = self.device_width / 2
        starty = self.device_height / 3
        endx = self.device_width / 2
        endy = self.device_height
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def fast_swipe_down(self):
        """快速上滑
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(u"设备：%s [action]向上滑动屏幕 " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height/2
        endx = startx
        endy = starty-300
        self.driver.swipe(startx, starty,endx, endy, duration=150)

    def fast_swipe_up(self):
        """快速上滑
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(u"设备：%s [action]向下滑动屏幕 " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height/2
        endx = startx
        endy = starty + 300
        self.driver.swipe(startx, starty,endx, endy, duration=150)

    def random_swipe_horizontal(self):
        direction = self.random_choice(("right", "left"))
        if direction == "right":
            self.fast_swipe_left()
        else:
            self.fast_swipe_right()

    def pull_to_refresh_page(self, duration=None):
        """下拉刷新页面,当前页面非顶部的时候禁用
        :Args:
            - None
        :Usage:
            self.tester.pull_to_refresh_page()
        """
        self.logger.info(u"设备：%s [action]下拉刷新页面  " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height/3
        endx = self.device_width/2
        endy = self.device_height - 10
        self.driver.swipe(startx, starty, endx, endy, duration=100)
        time.sleep(2)

    def pull_to_refresh_page2(self,duration=None):
        #拖拉距离大了，直播卡片页面会有上滑动作，为了不影响其他页面，重新写一个
        self.logger.info(u"设备：%s [action]下拉刷新直播卡片  " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height/7
        endx = self.device_width/2
        endy = self.device_height/3
        self.driver.swipe(startx, starty, endx, endy, duration=10000)
        time.sleep(2)

    def is_element_exist(self, element, timeout=1):
        """判断元素是否存在，存在返回True，不存在返回No
        增加timeout超时等待，默认为1次，可通过传的参数覆盖

        :Args:
            - element - 要查找的元素
        :Usage:
            self.tester.is_element_exist('com.nice.main:id/beauty_auto')  # 美颜按钮
        """
        # self.logger.info(u"设备：%s 查找控件 %s" % (self.device.devicename, element))
        count = 0
        while count < timeout:
            source = self.driver.page_source
            if element in source:
                # self.logger.info(u"设备：%s 找到控件: %s" % (self.device.devicename, element))
                return True
            else:
                count += 1
                time.sleep(1)
        # self.logger.info(u"设备：%s 未找到控件: %s" % (self.device.devicename, element))
        return False

    def get_center_coor_and_tap(self, element):
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']
        x = x + width / 2
        y = y + height / 2
        time.sleep(1)
        self.tap_screen(x, y)

    def get_center_loction(self, element):
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']
        x = x + width / 2
        y = y + height / 2
        return x, y

    def is_autotest_exit(self):
        """初始话设备时，判断是否存在autotest测试图片
        :Usage:
            self.pull_file_to_device  # 美颜按钮
        """
        cmd = "adb -s %s shell ls /sdcard/DCIM/ | grep autotest" % self.device.deviceid
        result = "autotest"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output.strip('\r\n') == result:
            self.logger.info(u"设备：%s SD中存在测试图片 " % self.device.deviceid)
            return True
        else:
            self.logger.info(u"设备：%s SD中不存在测试图片 " % self.device.deviceid)
            return False

    def is_auto_video_exit(self):
        """初始话设备时，判断是否存在autotest测试图片
        :Usage:
            self.pull_file_to_device  # 美颜按钮
        """
        cmd = "adb -s %s shell ls /sdcard/DCIM/ | grep auto_video" % self.device.deviceid
        result = "auto_video"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output.strip('\r\n') == result:
            self.logger.info(u"设备：%s SD中存在测试视频 " % self.device.deviceid)
            return True
        else:
            self.logger.info(u"设备：%s SD中不存在测试视频 " % self.device.deviceid)
            return False

    def random_choice(self, string):
        return random.choice(string)

    # 判断手机本地是否有autotest图库
    def pic_data_prepare(self):
        #Log.logger.info(u"设备：%s 检查文件开始" % self.tester.device.devicename)
        if self.is_autotest_exit():
            time.sleep(1)
        else:
            #Log.logger.info(u"设备：%s 写入测试文件" % self.tester.device.devicename)
            self.pull_pic_file_to_device()
            time.sleep(10)
            self.refresh_test_pic()

    #判断本地是否有auto_video视频
    def video_data_prepare(self):
        # Log.logger.info(u"设备：%s 检查文件开始" % self.tester.device.devicename)
        if self.is_auto_video_exit():
            time.sleep(1)
        else:
            # Log.logger.info(u"设备：%s 写入测试文件" % self.tester.device.devicename)
            self.pull_video_file_to_device()
            time.sleep(10)
            self.refresh_test_video()

    def pull_pic_file_to_device(self):
        """初始话设备时，拷贝图片进入设备
        :Usage:
            self.pull_pic_file_to_device
        """
        path = os.getcwd()+'/res/autotest'
        cmd = "adb -s %s push %s /sdcard/DCIM/" % (self.device.deviceid, path)
        subprocess.Popen(cmd, shell=True)
        time.sleep(5)

    def pull_video_file_to_device(self):
        """初始话设备时，拷贝短视频进入设备
        :Usage:
            self.pull_file_to_device  video_
        """
        path = os.getcwd()+'/res/auto_video'
        cmd = "adb -s %s push %s /sdcard/DCIM/" % (self.device.deviceid, path)
        subprocess.Popen(cmd, shell=True)
        time.sleep(5)

    def refresh_test_pic(self):
        """初始话设备时，刷新系统图库，使autotest文件可见
        :Usage:
            self.tester.refresh_test_pic()
        """
        img_src = os.getcwd()+'/res/autotest'
        path = get_file_name_from_path(img_src, 'jpg')
        for i in range(len(path)):
            cmd = "adb -s %s shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/autotest/%s.jpg" % (self.device.deviceid, path[i])
            subprocess.Popen(cmd, shell=True)
            i += 1

    def refresh_test_video(self):
        """初始话设备时，刷新系统图库，使auto_video文件可见
        :Usage:
            self.tester.refresh_test_pic()
        """
        img_src = os.getcwd() + '/res/auto_video'
        path = get_file_name_from_path(img_src, 'mp4')
        for i in range(len(path)):
            cmd = "adb -s %s shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/auto_video/%s.mp4" % (
            self.device.deviceid, path[i])
            subprocess.Popen(cmd, shell=True)
            i += 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~常用处理方法~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def back_to_feed(self):
        """用户case结束后回到Feed首页
        :Usage:
            self.tester.back_to_feed()
        """
        if self.is_element_exist('com.nice.main:id/btnTabSubscription'):
            time.sleep(1)
        else:
            self.driver.close_app()
            self.logger.info(u"设备：%s close app " % self.device.devicename)
            time.sleep(5)
            self.driver.launch_app()
            self.logger.info(u"设备：%s restart app " % self.device.devicename)
            time.sleep(10)

    def clear_pub_story(self):
        """删除已经发布的story，防止影响其他case的验证
        :Usage:
            self.tester.clear_pub_story()
        """
        if not self.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
            self.back_to_feed()

        # 进入我的故事u
        if self.is_element_exist('我的故事'):
            self.find_element_by_xpath_and_tap(
                 '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
        else:
            self.logger.info(u"设备：%s 不存在我的故事 " % self.device.devicename)

        # 删除已经发布的故事
        while self.is_element_exist(u'上传失败') == True:
            try:
                self.driver.find_element_by_id('com.nice.main:id/img_share').click()
                self.driver.find_element_by_android_uiautomator('text("放弃上传")').click()
            except:
                self.logger.info(u"设备：%s 没有点击到story menu " % self.device.devicename)

        while self.is_element_exist('com.nice.main:id/more_share') == True:
            try:
                self.driver.find_element_by_id('com.nice.main:id/more_share').click()
                self.driver.find_element_by_android_uiautomator('text("删除")').click()
                self.driver.find_element_by_id('com.nice.main:id/btn_ok').click()
            except:
                self.logger.info(u"设备：%s 没有点击到story menu " % self.device.devicename)

    def get_verify_code(self):
        """获取当前手机号的短信验证码
        :Usage:
            self.tester.get_verify_code()
        """
        getverifycode = os.getcwd() + '/getverifycode.sh'
        sinput = "sh %s %s" % (getverifycode, self.user.mobile)
        myproc = subprocess.Popen(sinput, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        strout = myproc.stdout.read().decode("utf-8")
        code = strout.strip()
        self.logger.info(u"设备：%s 登陆验证码为:%s " % (self.device.devicename, code))
        if not code:
            print "get vertifycode failed！！！"
        return code

    def longin_with_verifycode(self):
        """处理登陆流程中的短信验证码环节
        :Usage:
            self.tester.longin_with_verifycode()
        """
        if self.is_element_exist('com.nice.main:id/btn_phone_verify', timeout=5):
            self.logger.info(u"设备：%s 需要短信验证才能登陆" % self.device.devicename)
            self.find_element_by_id_and_tap('com.nice.main:id/btn_phone_verify')
            time.sleep(2)
            code = self.get_verify_code()
            self.find_element_by_id_and_send_keys('com.nice.main:id/verification_code', code)
            time.sleep(2)
            if self.is_element_exist('com.nice.main:id/titlebar_action_btn'):
                self.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
        else:
            self.logger.info(u"设备：%s 不需要短信验证登陆" % self.device.devicename)

    #截取指定区域的图片并存储到指定文件夹中
    def get_screent_shot_target_size(self,start_x, start_y, end_x, end_y,dirPath,imageName,form='png'):
        # 自定义截取范围
        # 先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        # 将截屏文件复制到指定目录下
        #dirPath 在调用方法之前需要自己定义图片的存储位置,imageName给截的图命名
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))

        print '截图成功'

    #通过指定元素截取图片相似度对比
    def get_screen_element_and_compare(self,eleid,image_path,percent=0):
        #在使用该方法时，需要先定义image_path,即定义存放目标图片的绝对路径
        #目标图片存放在res/image_compare文件夹下
        #percent为相似度，默认为0，表示相似度100%

        # 先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)
        # 获取元素所占区域
        location = eleid.location
        size = eleid.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        # 截取元素对应的图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        # 加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
        else:
            raise Exception("%s is not exist" % image_path)

        #对比截图和本地图片
        histogram1 = Image.open(TEMP_FILE).histogram()
        histogram2 = load.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, \
                                                         histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            print '相似度匹配设定的百分比'
            return True
        else:
            print '相似度不匹配设定的百分比'
            return False

    #通过指定size区域截取图片相似度对比
    def get_screen_target_size_and_compare(self,start_x, start_y, end_x, end_y,image_path,percent=0):
        # 在使用该方法时，需要先定义image_path,即定义存放目标图片的绝对路径
        # 目标图片存放在res/image_compare文件夹下
        # percent为相似度，默认为0，表示相似度100%

        # 自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        # 加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
        else:
            raise Exception("%s is not exist" % image_path)

        # 对比截图和本地图片
        histogram1 = Image.open(TEMP_FILE).histogram()
        histogram2 = load.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, \
                                                         histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            print '相似度匹配设定的百分比'
            return True
        else:
            print '相似度不匹配设定的百分比'
            return False

    def inputInt(self, strings):
        # print("传的参数" + str(strings))
        myDict = {'0': '7', '1': '8', '2': '9', '3': '10', '4': '11',
                  '5': '12', '6': '13', '7': '14', '8': '15', '9': '16'}
        for i in range(len(strings)):
            i = strings[i]
            # print('字符串中的值' + str(i))
            keywords = myDict[i]
            # print('字符串转化后的值' + str(keywords))
            self.driver.press_keycode(keywords)

    def set_input_method(self):
        true_value = "com.google.android.inputmethod.pinyin/.PinyinIME"
        package_name = "com.google.android.inputmethod.pinyin"
        command0 = 'adb -s %s shell ime list -s | grep %s' % (self.device.deviceid, true_value)
        command1 = 'adb -s %s shell settings get secure default_input_method | grep %s' % (self.device.deviceid, true_value)
        command2 = 'adb -s %s shell ime set %s' % (self.device.deviceid, true_value)
        install_akp = "adb -s %s install -r %s" % (self.device.deviceid, DataProvider.inputmethod)
        p = os.popen(command0)
        outstr = p.read()
        if outstr != true_value:
            subprocess.call(install_akp, shell=True)
        p1 = os.popen(command1)
        outstr = p1.read()
        if outstr != true_value:
            subprocess.call(command2, shell=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~常用case步骤~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def pub_nice_pic(self):

        self.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
        self.is_element_exist("nice")

        # 点击相册选择
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_center_title')

        # 切换到autotest相册
        time.sleep(3)
        while self.is_element_exist(u'autotest')==False:
            self.swipe_down()
            time.sleep(1)

        self.find_element_by_uiautomator_and_tap(
            'new UiSelector().resourceId(\"com.nice.main:id/txt_name\").textContains(\"autotest\")')

        # 选择9张图片
        time.sleep(3)
        for i in range(9):
            time.sleep(2)
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().resourceId(\"com.nice.main:id/select_textview_container\").index(1)')

        # 点击下一步到达编辑页面
        time.sleep(3)
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_next')

        # 获取图片Container的中心坐标并点击弹出标签页面
        time.sleep(10)
        if self.is_element_exist('com.nice.main:id/btn_panel_crop'):
            time.sleep(2)
            self.tap_screen_center()

        # 添加标签autotest
        time.sleep(1)
        self.find_element_by_id_and_send_keys('com.nice.main:id/txt_search', 'autotest')
        self.find_element_by_uiautomator_and_tap(
            'new UiSelector().resourceId(\"com.nice.main:id/tv_tag_name\").index(0)')

        # 点击下一步到达预览页面
        self.find_element_by_id_and_tap('com.nice.main:id/title_next_btn')

        # 添加
        self.find_element_by_id_and_send_keys('com.nice.main:id/publish_content_text', '123456')

        # 点击发布按钮
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_next_btn')
        time.sleep(10)
        self.back_to_feed()
        print "pub_nine_pic finished"

    def find_pub_nice_pic(self):
        text = "123456"
        for i in range(20):
            if self.is_element_exist(text):
                self.driver.find_element_by_android_uiautomator('text("123456")')
                self.logger.info(u"设备: %s 找到发图标记: %s " % (self.device.devicename, text))
                return True
            else:
                self.swipe_down()
                i += 1
        self.logger.info(u"设备: %s 未找到发图标记: %s " % (self.device.devicename, text))
        return False

    def enter_myprofile(self):
        self.back_to_feed()
        self.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
        self.find_element_by_id_and_tap('com.nice.main:id/layout_profile_base_container')
        if self.is_element_exist("com.nice.main:id/profile_edit", timeout=10):
            self.logger.info(u"设备: %s 成功进入个人页" % self.device.devicename)
        else:
            self.logger.info(u"设备: %s 进入个人页失败" % self.device.devicename)

    def enter_live_from_disc_page(self):
        self.back_to_feed()
        self.driver.find_element_by_id('com.nice.main:id/btnTabExplore').click()
        if self.is_element_exist('com.nice.main:id/recommend_live_rv', timeout=10):
            time.sleep(5)
            self.find_element_by_xpath_and_tap('//android.widget.RelativeLayout[3]')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/bg_live_card')
        time.sleep(5)
        self.find_element_by_id_and_tap('com.nice.main:id/img_pic')
        if self.is_element_exist('com.nice.main:id/btn_exit', timeout=5):
            return True
        elif self.is_element_exist('com.nice.main:id/exit_btn', timeout=5):
            return True
        else:
            return False

    def calculate_elementcenter_and_tap(self,element):
        self.ele = self.driver.find_element_by_id(element)
        x = self.ele.location['x']
        y = self.ele.location['y']
        width = self.ele.size['width']
        height = self.ele.size['height']
        x1 = x + width / 2
        y1 = y + height / 2
        time.sleep(1)
        self.tap_screen(x1, y1)

    def enter_hot_live_list(self):
        self.back_to_feed()
        self.driver.find_element_by_id('com.nice.main:id/btnTabExplore').click()
        if self.is_element_exist('com.nice.main:id/recommend_live_rv', timeout=10):
            time.sleep(5)
            self.find_element_by_xpath_and_tap('//android.widget.RelativeLayout[3]')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/bg_live_card')
        time.sleep(5)

    def find_mutil_pic_profile(self):
        if self.is_element_exist('9'):
            return True
        else:
            for i in range(20):
                self.swipe_down()
                if self.is_element_exist('9'):
                    self.logger.info(u"设备: %s 找到9图" % self.device.devicename)
                    return True
                else:
                    i += 1
            self.logger.info(u"设备: %s 找到9图" % self.device.devicename)
            return False

    def exit_from_watch_live(self):
        """
        从观看的直播中退出
        """
        if self.is_element_exist('com.nice.main:id/btn_exit', timeout=5):
            self.find_element_by_id_and_tap('com.nice.main:id/btn_exit')
            if self.is_element_exist('com.nice.main:id/btn_exit'):
                self.find_element_by_id_and_tap('com.nice.main:id/btn_exit')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/exit_btn')

    def enter_story_pub_page(self):
        """从feed页进入story拍摄页面，并处理引导、提示等逻辑
        :Usage:
            self.tester.clear_pub_story()
        """
        # 确认在feed首页
        self.back_to_feed()

        # Feed页滑动打开story拍摄页面
        self.swipe_right()

        # 处理第一次进入story的引导或者弹窗
        if self.is_element_exist(u'您的手机暂时不支持故事功能'):
            self.logger.info(u"设备：%s 不支持故事功能 " % self.device.devicename)
            self.screenshot(u"不支持故事功能 ")
            self.find_element_by_id_and_tap('com.nice.main:id/btn_ok')
            self.back_to_feed()
            return False
        else:
            time.sleep(2)
            self.tap_screen_center()
            return True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end常用case步骤~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ monkey~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 定义一个类变量，用于创建monkey结果文件夹
    monkey_result_path = ""
    monkey_log = os.getcwd()+'/Monkey_log'

    @classmethod
    def is_exit_monkeyresultfile(cls):
        if os.path.exists(cls.monkey_log):
            print 'monkey结果文件夹已存在'
        else:
            print 'monkey结果文件夹不存在，自动创建'
            os.mkdir(cls.monkey_log)

    @classmethod
    def create_monkey_result(cls):
        cls.monkey_result_path=os.getcwd()+'/Monkey_log/%s' % get_format_currenttime()
        os.mkdir(cls.monkey_result_path)

    #throttle_set : 设定执行的时间间隔,单位为毫秒
    #seed_set : 设定seed值，seed值相同则跑的monkey序列相同
    #perform_times : monkey的执行次数
    #--pct-motion 30 --pct-trackball 30 --pct-touch 10 --pct-appswitch 10
    def run_monkey(self,seed_set,perform_times):
        self.monkey_log = self.monkey_result_path
        cmd = "adb -s %s shell monkey -p com.nice.main -v -v --throttle 200 -s %s --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes %s >%s/%s.log" % (self.device.deviceid,seed_set,perform_times,self.monkey_log,self.device.devicename)
        subprocess.call(cmd, shell=True)

    # 定义列表，该列表用于存放设备生成的log文件名
    lis = []

    #读取当前结果文件夹下的所有文件，并将每个文件的文件名加入到列表中
    @classmethod
    def open_filelist(self):
        self.pathDir = os.listdir(self.monkey_result_path)
        for allDir in self.pathDir:
            child = os.path.join('%s/%s' %  (self.monkey_result_path,allDir))
            self.lis.append(child)

    anr = 0
    crash = 0
    monkey_total_result = ''

    @classmethod
    def read_log(self):
        #创建统计crash和anr结果的文件,并写入标题头
        monkey_total_result = self.monkey_result_path + "/Summary.txt"
        print '文件名字为：%s ' % monkey_total_result

        init=open(monkey_total_result, 'a+')
        init_log=u'---------本次monkey测试结果统计--------\n'
        init.writelines(init_log)
        init.close()

        # 读取每个设备的log文件
        for currentlis in self.lis:
            crashfile = open(currentlis,'rb')

            # 以可写入的方式打开统计结果文件
            monkey_result = open(monkey_total_result, 'a+')
            # 设备信息
            result_string = u'文件: %s 的crash和anr统计信息 \n' % currentlis
            monkey_result.writelines(result_string)

            # 循环读取log文件中的每一行
            for s in crashfile.readlines():
                if 'CRASH: com.nice.main' in s:   #统计Crash出现的次数
                    self.crash=self.crash+1
                    crash_line=u'Crash日志:\n %s \n' % s
                    monkey_result.writelines(crash_line)
                if 'ANR in com.nice.main' in s:   #统计ANR出现的次数
                    self.anr = self.anr + 1
                    anr_line=u'ANR日志:\n %s \n'% s
                    monkey_result.writelines(anr_line)
            crashfile.close()

            #crash个数
            crash_string=u'crash个数统计: %s \n' % self.crash
            monkey_result.writelines(crash_string)
            #anr个数
            anr_string=u'anr个数统计: %s \n' % self.anr
            monkey_result.writelines(anr_string)
            #自动换行
            enter='\n'
            monkey_result.writelines(enter)
            #关闭文件
            monkey_result.close()
            #该文件遍历之后将crash和anr的变量清0
            self.crash = 0
            self.anr=0
        self.lis.append(monkey_total_result)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ monkey~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





