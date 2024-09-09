# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from flask_restx import Api
from api.view.file import file_api_namespace
from api.view.trial_sentinel import agent_api_namespace
from api.view.chat import (
    chat_api_namespace,
    multi_chat_api_namespace,
)
from logger import s_log

route_map = {
    'agent_chat': agent_api_namespace,
    'chat_api': chat_api_namespace,
    'multi_chat': multi_chat_api_namespace,
    'file': file_api_namespace,
}


def init_app_router(api: Api, prefix: str):
    """
    初始化应用程序路由。

    :param api: Flask-RESTPlus或其他API对象实例
    :param prefix: API前缀字符串
    """
    # 遍历全局route_map，注册每个命名空间
    for path_suffix, namespace in route_map.items():
        full_path = f'{prefix}/{path_suffix}'
        api.add_namespace(namespace, full_path)
    s_log.info('注册所有路由 registered routers')
