# usr/bin/python
# -*- coding:utf-8 -*-
import Log

class global_var:

    run_mode = 'autotest' #monkey

    if_run = False  # 当时是否有运行的任务

    task_id = 0  # 当前的任务id

def set_run_mode(value):
    global_var.run_mode = value


def get_run_mode():
    return global_var.run_mode


def set_if_run(value):
    global_var.if_run = value


def get_if_run():
    return global_var.if_run


def set_taskid(value):
    global_var.task_id = value


def get_taskid():
    return global_var.task_id

