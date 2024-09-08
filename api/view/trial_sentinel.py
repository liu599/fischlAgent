# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields

chat_api_namespace = Namespace("队列测试", description='队列测试, 接口定义')

@chat_api_namespace.route("")
class LLMChatView(BaseView):

    @chat_api_namespace.doc()
    def get(self):
        """
        调用Agent

        :param: current, limit
        :return: data, pager
        """
        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data=None
        )

    chat_payload = api.model('测试任务请求2', {
        'username': fields.Arbitrary(description='开发中的测试接口'),
        'password': fields.Arbitrary(description='开发中的测试接口'),
    })

    @chat_api_namespace.doc(body=chat_payload)
    def post(self):
        """
        创建测试任务

        :body: task_payload
        :return: task_id
        """
        un = self.request.form.get('username')
        pwd = self.request.form.get('password')
        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data={
                "username": un,
                "password": pwd
            }
        )