# -*- coding: utf-8 -*-
# @Time        : 2024/7/8
# @Author      : liuboyuan
from framework.inori_log import Logger


def make_logger(identifier, log_dir='static'):
    return Logger(
        name=identifier,
        log_dir=log_dir,
        debug=True
    ).logger


class PluginLog:
    def __init__(self, identifier, log_dir='static'):
        self.logger = make_logger(identifier, log_dir=log_dir)
