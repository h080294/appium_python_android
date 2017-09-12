#!usr/bin/python
# -*- coding:utf-8 -*-

class DriverManager(object):

    drivers = {}

    #退出所有的Driver
    @classmethod
    def quit_all_driver(cls):
        print cls.drivers
        for deviceid,driver in cls.drivers.iteritems():
            if driver != None:
                print driver
                driver.quit()

    #根据deviceid退出相应的Driver
    @classmethod
    def quit_driver(cls,deviceid):
        if cls.drivers.has_key(deviceid):
            if cls.drivers[deviceid] != None:
                cls.drivers[deviceid].quit()
