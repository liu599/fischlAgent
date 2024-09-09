# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from framework.inori_utils.utils import ConfigLoader

api_conf = ConfigLoader()
api_conf.read('api.conf', '请拷贝api.default.conf为api.conf并按照需求配置')

azure_model_config = {
    "model_name": api_conf.get("llm_azure", "model_name"),
    "api_version": api_conf.get("llm_azure", "api_version"),
    "api_endpoint": api_conf.get("llm_azure", "api_endpoint"),
    "api_key": api_conf.get("llm_azure", "api_key"),
}

gpt_model_config = {
    "model_name": api_conf.get("llm_gpt4", "model_name"),
    "api_key": api_conf.get("llm_gpt4", "openai_api_key"),
    "user_name": api_conf.get("llm_gpt4", "user_name"),
}