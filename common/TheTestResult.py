#!usr/bin/python
# -*- coding:utf-8 -*-
import re
import sys

from common.ApkBase import ApkInfo

reload(sys)
sys.setdefaultencoding('utf-8')
import unittest
from pyh import *
import collections
from datetime import datetime
import traceback
from DriverManager import *
from DataProvider import *


class TheTestResult(unittest.TestResult):

    detailresults = {} #{"5HUC9S6599999999":{},"":{}}
    totalresults = {}
    device = {}
    testresultpath = ""
    filecss = ""
    filejs = ""

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        unittest.TestResult.__init__(self, stream=None, descriptions=None, verbosity=None)
        self.logger = Log.logger
        self._testcasedict = collections.OrderedDict()
        self.if_write_starttime = False

    def startTest(self, test):
        self.tester = test.tester
        self.deviceid = self.tester.device.deviceid
        testcase_starttime = get_format_currenttime()
        self.logger.debug(u'设备：%s Start Run %s' % (self.tester.device.devicename, test))
        print test.id()

        #初始化每个设备总结果的数据结构
        if self.__class__.totalresults.has_key(self.deviceid):
            pass
        else:
            self.__class__.totalresults[self.deviceid] = collections.OrderedDict()
            self.__class__.totalresults[self.deviceid]['totalrun'] = 0
            self.__class__.totalresults[self.deviceid]['startime'] = 0
            self.__class__.totalresults[self.deviceid]['stoptime'] = 0
            self.__class__.totalresults[self.deviceid]['errortestcase'] = 0
            self.__class__.totalresults[self.deviceid]['failtestcase'] = 0
            self.__class__.totalresults[self.deviceid]['skiptestcase'] = 0
            self.__class__.totalresults[self.deviceid]['successtestcase'] = 0

        #总用例数
        self.__class__.totalresults[self.deviceid]['totalrun'] = self.__class__.totalresults[self.deviceid]['totalrun'] + 1

        #开始时间
        if self.if_write_starttime:
            pass
        else:
            self.__class__.totalresults[self.deviceid]['starttime'] = testcase_starttime
            self.if_write_starttime = True

        #每个设备的详细执行结果
        self._testcasedict[test] = collections.OrderedDict()
        if self.__class__.detailresults.has_key(self.deviceid):
            pass
        else:
            self.__class__.device[self.deviceid] = self.tester.device
            self.__class__.detailresults[self.deviceid] = self._testcasedict
        self.__class__.detailresults[self.deviceid][test]['startime'] = testcase_starttime


    def stopTest(self, test):
        testcase_stoptime = get_format_currenttime()
        self.logger.debug(u'设备：%s Stop Run %s' % (self.tester.device.devicename, test))
        self.__class__.detailresults[self.deviceid][test]['stoptime'] = testcase_stoptime
        testcase_consumingtime = self.__class__.get_time_consuming(self.__class__.detailresults[self.deviceid][test]['startime']
        , self.__class__.detailresults[self.deviceid][test]['stoptime'])
        self.__class__.detailresults[self.deviceid][test]['consumingtime'] = testcase_consumingtime
        self.__class__.totalresults[self.deviceid]['stoptime'] = testcase_stoptime


    def startTestRun(self):
        # self.logger.debug('测试开始...')
        pass

    def stopTestRun(self):
        # self.logger.debug('测试完成...')
        pass

    def addError(self, test, err):
        info = '************      - %s -!(Error)    ***************' % self.tester.device.devicename
        self.logger.warning(info)
        #traceback.print_tb(err[2])
        traceback.print_exc()
        info = 'Error device:%s Run TestCase %s, Error info:%s' % (self.tester.device.devicename, test, traceback.format_exception(err[0], err[1], err[2]))
        self.logger.error(info)
        info = '************************************************'
        self.logger.warning(info)

        # 错误截图
        mytest = str(test)
        simplename = clean_brackets_from_str(mytest).replace(' ', '')
        myscr = "Error_%s" % simplename
        self.tester.screenshot2(myscr)

        # 错误日志
        list = traceback.format_exception(err[0], err[1], err[2])
        list_err = []  # 列表包含要输出的错误日志信息
        list_err.append(list[-1])
        list_err.append(list[2])

        if self.__class__.totalresults.has_key(self.deviceid):
            self.__class__.totalresults[self.deviceid]['errortestcase'] = self.__class__.totalresults[self.deviceid]['errortestcase'] + 1
        else:
            self.__class__.totalresults[self.deviceid]['errortestcase'] = 0

        try:
            self.__class__.detailresults[self.deviceid][test]['result'] = 'Error'
            self.__class__.detailresults[self.deviceid][test]['reason'] = list_err
        except Exception, e:
            info = Exception, ":", e
            self.logger.error(info)

    def addFailure(self, test, err):
        info = '************      - %s -!(Fail)    ***************' % self.tester.device.devicename
        self.logger.warning(info)
        info = 'Fail device:%s Run TestCase %s, Fail info:%s' % (self.tester.device.devicename, test, err[1].message)
        self.logger.warning(info)
        info = '***********************************************'
        self.logger.warning(info)

        # 失败截图
        mytest = str(test)
        simplename = clean_brackets_from_str(mytest).replace(' ', '')
        myscr = "Failure_%s" % simplename
        self.tester.screenshot2(myscr)

        # 失败日志
        list = traceback.format_exception(err[0], err[1], err[2])
        list_fail = []  # 列表包含要输出的错误日志信息
        list_fail.append(list[-1])
        list_fail.append(list[2])

        self.__class__.totalresults[self.deviceid]['failtestcase'] = self.__class__.totalresults[self.deviceid]['failtestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Fail'
        self.__class__.detailresults[self.deviceid][test]['reason'] = list_fail

    def addSuccess(self, test):
        self.__class__.totalresults[self.deviceid]['successtestcase'] = self.__class__.totalresults[self.deviceid]['successtestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Success'
        self.__class__.detailresults[self.deviceid][test]['reason'] = u'无'

    def addSkip(self, test, reason):
        info = '→_→Skip Run TestCase %s, Skip reason:%s' % (test ,reason)
        self.logger.debug(info)
        self.__class__.totalresults[self.deviceid]['skiptestcase'] = self.__class__.totalresults[self.deviceid]['skiptestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Skip'
        self.__class__.detailresults[self.deviceid][test]['reason'] = reason

    @classmethod
    def get_time_consuming(cls, starttime, endtime):
        starttime = datetime.datetime.strptime(starttime, "%Y_%m_%d_%H:%M:%S")
        endtime = datetime.datetime.strptime(endtime, "%Y_%m_%d_%H:%M:%S")
        timeconsuming = endtime - starttime

        if timeconsuming.seconds <= 0:
            timestr = '<1秒'
        else:
            timestr = '%s 秒' % timeconsuming.seconds
        return timestr

    @classmethod
    def create_result_folder(cls):
        cls.testresultpath = os.getcwd()+'/testresult/%s' % get_format_currenttime()
        os.mkdir(cls.testresultpath)

    # css文件路径
    filecss = os.getcwd()+'/testresult/result.css'
    # js文件路径
    filejs = os.getcwd()+'/testresult/result.js'
    # js文件路径
    sorttablejs = os.getcwd()+'/testresult/sorttable.js'

    @classmethod
    def generate_html_testresult(cls):
        page = PyH('测试报告')
        result_title = "nice Auto Test Report"

        # 增加css样式及js脚本
        page.addCSS(cls.filecss)
        page.addJS(cls.filejs)
        page.addJS(cls.sorttablejs)
        homediv = page << div(id='nice_report', cl='nice_header_passed')
        reporttitle = homediv << div(result_title, id='title')

        # 获取apk信息
        apk_name = ApkInfo().get_apk_pkg()
        apk_version_name = ApkInfo().get_apk_version_name()
        apk_version_code = ApkInfo().get_apk_version_code()

        # 展示apk相关信息
        reportsummary = homediv << div(id='summary')
        reportsummary << p(apk_name)
        reportsummary << p(apk_version_code)
        reportsummary << p(apk_version_name)

        tabdiv = page << div(id="Tab1")
        menuboxdiv = tabdiv << div(cl="Menubox")
        contentdiv = tabdiv << div(cl="Contentbox")

        tabul = menuboxdiv << ul()
        index = 1
        size = len(cls.detailresults)
        for deviceid, testresult in cls.detailresults.iteritems():
            tabstr = "setTab('one',%s, %s)" % (index, size)
            liid = "one%s" % index
            if index == 1:
                tabul << li(cls.device[deviceid].devicename, id=liid, onmouseover=tabstr, cl="hover")
            else:
                tabul << li(cls.device[deviceid].devicename, id=liid, onmouseover=tabstr)

            content_div_id = "con_one_%s" % index
            if index == 1:
                detaildiv = contentdiv << div(id=content_div_id, cl="hover")
            else:
                detaildiv = contentdiv << div(id=content_div_id, style="display:none")

            totaldiv = detaildiv << div(id='Total')
            totallabel = totaldiv << p('设备总结果:',align="left")
            totalresulttable = totaldiv << table(cl='totalResult', border="1", cellpadding="15")
            # totalresulttable.attributes['class'] = 'totalResult'
            result_title_tr = totalresulttable << tr()
            result_value_tr = totalresulttable << tr()
            ordertitle = collections.OrderedDict()
            timeconsuming = cls.get_time_consuming(cls.totalresults[deviceid]['starttime'], cls.totalresults[deviceid]['stoptime'])
            ordertitle[u'开始时间'] = DataProvider.starttime[deviceid]
            try:
                ordertitle[u'结束时间'] = DataProvider.stoptime[deviceid]
            except:
                ordertitle[u'结束时间'] = ordertitle[u'开始时间']
                Log.logger.debug('%s stoptime: connect error, use default time instead' % cls.device[deviceid].devicename)

            ordertitle[u'总耗时'] = timeconsuming
            ordertitle[u'总用例数'] = cls.totalresults[deviceid]['totalrun']
            ordertitle[u'成功用例数'] = cls.totalresults[deviceid]['successtestcase']
            ordertitle[u'失败用例数'] = cls.totalresults[deviceid]['failtestcase']
            ordertitle[u'错误用例数'] = cls.totalresults[deviceid]['errortestcase']
            ordertitle[u'跳过用例数'] = cls.totalresults[deviceid]['skiptestcase']

            for title, value in ordertitle.iteritems():
                result_title_tr << td(title)
                temp = result_value_tr << td(value)
                temp.attributes['class'] = title

            detaillabel = detaildiv << p('详细执行结果:',align="left")
            detail_table_title = (u'测试用例', u'开始时间', u'结束时间', u'耗时', u'测试结果', u'原因')
            detailresulttable = detaildiv << table(cl='sortable', width="100%", border="1", cellpadding="2", cellspacing="1", style="table-layout:fixed")
            detail_title_tr = detailresulttable << tr()
            for title in detail_table_title:
                detail_title_tr << td(title)
            for key, values in cls.detailresults[deviceid].iteritems():
                testcasetr = detailresulttable << tr()
                mykey = str(key)
                final_key = clean_brackets_from_str(mykey)
                testcasetr << td(final_key, align='left',width="100%",style="word-break:break-all")
                testcasetr << td(values['startime'])
                testcasetr << td(values['stoptime'])
                testcasetr << td(values['consumingtime'])
                try:
                    testcasetr << td(values['result'])
                except:
                    testcasetr << td('device connect error')
                    Log.logger.debug('%s result: device connect error, use default values instead' % cls.device[deviceid].devicename)
                try:
                    testcasetr << td(values['reason'], width="100%", style="word-break:break-all")
                except:
                    testcasetr << td('session error')
                    Log.logger.debug('%s reason: device connect error, use default values instead' % cls.device[deviceid].devicename)

            # 截图展示
            # 创建新div标签，并赋予id
            screencaplable = detaildiv << div(id='screencap')

            # 添加说明
            screencapdiv = detaildiv << p('截图验证:', align="left")

            # 获取截图文件名及绝对路径
            screecap_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].devicename)
            screencap_table_title = get_file_name_from_path(screecap_path, 'png')
            screencap_img_src = get_fullfile_from_path(screecap_path, 'png')

            # 创建table
            screencapresulttable = screencapdiv << table(width="auto", border="1", cellpadding="2", cellspacing="1",
                                               style="table-layout:fixed")

            # 描述'title'
            screencap_title_tr = screencapresulttable << tr()
            # 描述'内容'
            screencap = screencapresulttable << tr()

            # 循环写入截图名及对应截图
            for title in screencap_table_title:
                screencap_title_tr << td(title)
            for path in screencap_img_src:
                screencap << td("<img src=%s alt=%s width='170' height='300'> " % (path, title))

            # 视频展示
            # 创建新div标签，并赋予id
            screenrecordlable = detaildiv << div(id='screenrecord')
            screenrecorddiv = detaildiv << p('视频验证:', align="left")

            # 获取视频名字及绝对路径
            screerecord_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].devicename)
            screenrecord_table_title = get_file_name_from_path(screerecord_path, 'mp4')
            screenrecord_video_src = get_fullfile_from_path(screerecord_path, 'mp4')

            # 创建table
            screenrecordresulttable = screenrecorddiv << table(width="auto", border="1", cellpadding="2", cellspacing="1",
                                               style="table-layout:fixed")
            # 描述'title'
            screenrecord_title_tr = screenrecordresulttable << tr()
            # 描述'内容'
            screenrecord = screenrecordresulttable << tr()

            # 循环写入截图名及对应截图
            for title_video in screenrecord_table_title:
                screenrecord_title_tr << td(title_video)
            for path_video in screenrecord_video_src:
                screenrecord << td("<video width='240' height='320' controls='controls'> "
                                "<source src=%s type='video/mp4' /></video>" % path_video)

            # 添加错误截图信息
            errorlable = detaildiv << div(id='errorrecord')
            errordiv = detaildiv << p('错误截图:', align="left")

            error_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].devicename)
            error_table_title = get_file_name_from_path(error_path, 'jpg')
            error_src = get_fullfile_from_path(screerecord_path, 'jpg')

            # 创建table
            errorresulttable = errordiv << table(width="auto", border="1", cellpadding="2",
                                                               cellspacing="1",
                                                               style="table-layout:fixed")

            error_title = errorresulttable << tr()
            error_valus = errorresulttable << tr()

            # 循环写入截图名及对应截图
            for title_error in error_table_title:
                error_title << td(title_error)
            for path_error in error_src:
                error_valus << td("<img src=%s alt=%s width='170' height='300'> " % (path_error, title))


            # 循环添加各个设备的tab
            index = index + 1

        #生成测试结果Html文件
        htmltestresultfile = '%s/%s.html' % (cls.testresultpath, get_format_currenttime())
        try:
            page.printOut(htmltestresultfile)
        except IOError:
            Log.logger.error('file %s not exist' % htmltestresultfile)
            DriverManager.quit_all_driver()

        else:
            Log.logger.debug(u'测试报告创建成功，路径:%s' % htmltestresultfile)


if __name__ == '__main__':
    TheTestResult().generate_html_testresult()
