# -*- coding: utf-8 -*-
# @Time        : 2024/4/6
# @Author      : liuboyuan
# @Description :

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    name: str

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
