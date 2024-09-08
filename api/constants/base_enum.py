# -*- coding: utf-8 -*-
# @Time        : 2024/3/27
# @Author      : liuboyuan

from enum import Enum


class EnumBase(Enum):
    """枚举基础类"""
    @property
    def code(self):
        return self.value

    @code.getter
    def code(self):
        return self.value[0]

    @property
    def desc(self):
        return self.value

    @desc.getter
    def desc(self):
        return self.value[1]