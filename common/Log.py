#!usr/bin/python
#-*- coding:utf-8 -*-

import logging
import datetime
import os
import sys
from logging.handlers import RotatingFileHandler
from PublicMethod import *


class Log(object):

    logger = None

    @classmethod
    def create_log_file(cls):
        logfile = '%s/%s.log' % (os.path.abspath('./log'),get_format_currenttime())

        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)

        # 文件handler
        filehandle = RotatingFileHandler(logfile, maxBytes=50*1024*1024, backupCount=5, encoding="UTF-8")
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        filehandle.setFormatter(formatter)
        cls.logger.addHandler(filehandle)

        # 屏幕handler
        console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        console.setFormatter(formatter)
        cls.logger.addHandler(console)

if __name__=='__main__':
    Log.create_log_file()
    Log.logger.debug('this is a debug msg')
    Log.logger.info('this is a info msg')
