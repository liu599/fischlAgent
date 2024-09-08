# -*- coding: utf-8 -*-
# @Time        : 2024/6/14
# @Author      : liuboyuan
from abc import ABC, abstractmethod
from typing import Any

import loguru

from framework.inori_llm_core.utils_pack.plugin_log import PluginLog


class BaseLanguageModel(ABC):
    """通用模型基础类"""

    def __init__(self, identifier="llm", *args, **kwargs):
        self.identifier = identifier
        if 'log_handler' in kwargs:
            self.logger = kwargs['log_handler'].logger
        else:
            self.logger: loguru.Logger = PluginLog(self.identifier).logger

    @abstractmethod
    def langchain_request(self, *args, **kwargs) -> (str, Any, Any):
        """Langchain调用链基础类"""
        raise NotImplementedError("子类必须实现 langchain_request 方法")
