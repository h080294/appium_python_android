#!/usr/bin/python
#-*- coding:utf-8 -*-

import SimpleHTTPServer
from Log import Log
import urlparse
import threading
import json
import re
import share
from RunTestManager import *


class HttpServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    run_manager = None

    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_POST(self):
        self.logger = Log.logger
        self.logger.warning("--------- POST ---------")

    def do_GET(self):
        self.logger = Log.logger
        self.logger.warning("--------- GET ---------")
        self.logger.warning(self.path)
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)

        if parsedParams.path == '/run':
            self.run(queryParsed)
        else:
            result_dict = {'code':1001,"data":{"message":"错误的命令"}}
            self.set_response(result_dict)

    def run(self, params):
        if share.get_if_run() == True:
            result_dict = {'code':1002,"data":{"message":"已经有一个任务在执行","taskid":"%s" % share.get_taskid()}}
            self.set_response(result_dict)
            return
        if params.has_key('mode') == False:
            result_dict = {'code':1003,"data":{"message":"缺少mode参数"}}
            self.set_response(result_dict)
            return
        elif params['mode'][0] != "monkey" and params['mode'][0] != 'autotest':
            self.set_response({'code':1004, "data":{"message":"mode参数错误"}})
            return

        try:
            set_run_manager(RunTestManager(params['mode'][0]))
            self.taskid = get_run_manager().task_id
            share.set_taskid(get_run_manager().task_id) #设置全局共享taskid
            share.set_if_run(True)
            thread = threading.Thread(target=get_run_manager().start_run)
            thread.start()
            result_dict = {'code':0,"data":{"taskid fuck":"%s" % self.taskid,"message":"开始执行%s任务" % params['mode']}}
            self.set_response(result_dict)
        except Exception, e:
            traceback.print_exc()
            get_run_manager().stop_run()

    def set_response(self, text, code=200):
        try:
            result = json.dumps(text, ensure_ascii=False)
        except Exception, e:
            traceback.print_exc()
            result = text
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(result)


def get_run_manager():
    return HttpServerHandler.run_manager


def set_run_manager(value):
    HttpServerHandler.run_manager = value