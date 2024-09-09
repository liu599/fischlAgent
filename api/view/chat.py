# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import json

from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields
from framework.inori_llm_core.chat.chat import llm_chat
from framework.inori_llm_core.chat.multiple_chain import multiple_chain_chat_sample

chat_api_namespace = Namespace("大模型对话测试", description='测试, 接口定义')
multi_chat_api_namespace = Namespace("多个大模型对话测试", description="测试, 接口定义")

@chat_api_namespace.route("")
class ChatView(BaseView):

    chat_payload = api.model('单个Chat请求', {
        'model': fields.String(description='支持gpt4和azure', example='azure', required=True),
        'content': fields.String(description='对话内容', required=True),
        'system': fields.String(description='可选, 系统提示词'),
    })

    @chat_api_namespace.doc(body=chat_payload)
    def post(self):
        params = self.request.json
        q = params["q"]
        if "model" in params and params["model"] == "azure":
            chat_message_body = llm_chat("azure", self.azure_model_config, "{input}", "", {
                "input": q
            })
            return self.response_raw(
                code=Codes.SUCCESS.code,
                msg=Codes.SUCCESS.desc,
                data=chat_message_body
            )
        elif "model" in params and params["model"] == "gpt4":
            chat_message_body = llm_chat("gpt4", self.gpt_model_config, "{input}", "", {
                "input": q
            })
            return self.response_raw(
                code=Codes.SUCCESS.code,
                msg=Codes.SUCCESS.desc,
                data=chat_message_body
            )
        else:
            return self.response_raw(
                code=Codes.PARAMS_CHECK_FAILED.code,
                msg=Codes.PARAMS_CHECK_FAILED.desc,
                data=None
            )


@multi_chat_api_namespace.route("")
class MultiChatView(BaseView):
    multi_chat_payload = api.model('多个Chat请求', {
        'content': fields.String(description='对话内容, 是一个json字符串, 默认要有input, 但是可以根据humanTemplate配置', required=True),
        'systemTemplate': fields.String(description='可选, 系统提示词'),
        'humanTemplate': fields.Raw(description='用户提示词模板, 必须含有{input}字段')
    })

    @multi_chat_api_namespace.doc(body=multi_chat_payload)
    def post(self):
        params = self.request.json
        human_template = params["humanTemplate"]
        system_prompt = params["systemTemplate"]
        chat_message_body = multiple_chain_chat_sample(
            chat_message=json.loads(params["content"]),
            models=[
                {
                    "model_name": "azure",
                    "model_config": self.azure_model_config,
                },
                {
                    "model_name": "gpt4",
                    "model_config": self.gpt_model_config,
                },
            ],
            human_template=human_template,
            system_prompt=system_prompt,
        )
        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data=chat_message_body
        )

