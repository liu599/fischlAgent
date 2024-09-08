# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from framework.inori_utils.utils import ConfigLoader

api_conf = ConfigLoader()
api_conf.read('api.conf', '请拷贝api.default.conf')