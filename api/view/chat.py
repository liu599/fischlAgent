# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields
from framework.inori_llm_core.chat.chat import llm_chat

chat_api_namespace = Namespace("大模型对话测试", description='测试, 接口定义')

@chat_api_namespace.route("")
class ChatView(BaseView):
    def get(self):
        pass

    chat_payload = api.model('Chat请求', {
        'model': fields.String(description='支持gpt35和azure(gpt4)', example='azure', required=True),
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
        else:
            return self.response_raw(
                code=Codes.PARAMS_CHECK_FAILED.code,
                msg=Codes.PARAMS_CHECK_FAILED.desc,
                data=None
            )

