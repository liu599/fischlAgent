# -*- coding: utf-8 -*-
# @Time        : 2024/7/8
# @Author      : liuboyuan
from typing import Type
import loguru


def log_error_and_raise(error_message: str, log_handler: loguru.logger,
                        exception_class: str | Type[BaseException] = 'general'):
    if exception_class == 'general':
        log_handler.error(f"General Error Message: {error_message}")
        raise Exception(error_message)
    log_handler.error(f"Error Type: {exception_class} Error Message: {error_message}")
    raise exception_class(error_message)
