# -*- coding: utf-8 -*-
# @Time        : 2024/3/27
# @Author      : liuboyuan
# @Description : 基本输出格式
import sys

from flask import request, jsonify, make_response

# Resource 继承了 MethodView
# from flask.views import MethodView
from logger import s_log
from logger import register_logger
from api.constants.status_code import Codes
from flask_restx import Resource
from api.conf import api_conf, azure_model_config, gpt_model_config


class BaseView(Resource):
    azure_model_config = None
    gpt_model_config = None
    base_url = 'http://localhost:5000'
    api_config = None
    request = None
    prompts = ''

    def __init__(self, *args, **kwargs):
        self.__setattr__('request', request)
        self.__setattr__('api_config', api_conf)
        self.__setattr__('base_url', api_conf.get("server", "url"))
        self.__setattr__('azure_model_config', azure_model_config)
        self.__setattr__('gpt_model_config', gpt_model_config)
        self.__setattr__('prompts', api_conf.get("prompts", "github_prompts"))
        super(BaseView, self).__init__(*args, **kwargs)

    def response_raw(self, code, msg, data):
        return jsonify(
            {
                "code": code,
                "message": msg,
                "data": data
            }
        )

    # 统一错误处理中间件
    def handle_error(self, error, error_type):
        error_msg = str(error)
        error_code = 401
        if hasattr(error, 'code'):
            error_code = error.code
        if error_type == 'ValueError':
            error_code = Codes.PARAMS_CHECK_FAILED.code
            error_msg = f"输入的数值错误 {error_msg}"
        if error_type == 'KeyError':
            error_code = Codes.PARAMS_CHECK_FAILED.code
            error_msg = f"该请求格式不正确, 参数值不支持或缺少参数 {error_msg}"
        if error_type == 'OperationalError':
            error_code = Codes.FAILURE.code
            error_msg = f"数据库连接错误, 请联系管理员解决 {error_msg}"
        if error_type == 'IntegrityError':
            error_code = Codes.FAILURE.code
            error_msg = f"创建请求失败, 已有数据。 {error_msg}"
        # return jsonify(response), getattr(error, 'code', 500)
        return self.response_raw(
            code=error_code,
            msg=error_msg,
            data=''
        )

    def dispatch_request(self, *args, **kwargs):
        # 每次请求时API重新注册logger, 这样logger的地址会保持一致。
        register_logger()
        try:
            return super().dispatch_request(*args, **kwargs)
        except Exception as e:
            # 出错时也需要重置logger地址
            register_logger()
            # 如果在执行视图方法时发生任何异常，调用handle_error方法
            s_log.opt(exception=e).error(f'Error when dispatching - TYPE: [{type(e).__name__}], MESSAGE:  {e}')
            return self.handle_error(e, error_type=type(e).__name__)
