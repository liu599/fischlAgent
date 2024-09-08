# -*- coding: utf-8 -*-
# @Time        : 2024/4/6
# @Author      : liuboyuan
# @Description :

from configparser import ConfigParser
from framework.inori_utils.log_utils import LOG
import os.path


class ConfigLoader:
    def __init__(self):
        self.config = ConfigParser()

    def get(self, section, option):
        return self.config.get(section, option)

    def read(self, path, errorMsg):
        if not os.path.exists(path):
            LOG.error(errorMsg)
            exit(1)
        self.config.read(path)
        LOG.info(f'读取config成功 {path}')

