# -*- coding: utf-8 -*-
# @Time        : 2024/7/5
# @Author      : liuboyuan
from framework.inori_log import Logger

s_log = Logger(
    name='inori',
    log_dir='static',
    debug=True
).logger


def register_logger():
    global s_log
    s_log = Logger(
        name='inori',
        log_dir='static',
        debug=True
    ).logger
