# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields

from framework.inori_plugin_manager.plugin_manager import PluginManager

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
        'repo': fields.String(description='repo name', example='repo:langchain-ai/langchain', required=True),
    })

    @chat_api_namespace.doc(body=chat_payload)
    def post(self):
        """
        调用Github Agent并存储

        :body: task_payload
        :return: task_id
        """
        params = self.request.json
        repo = params['repo']
        local_folder = self.api_config.get('data', 'local_folder')
        token = self.api_config.get('github', 'token')
        pm = PluginManager("./api/plugins/agent")
        print(pm.get_plugin_list())
        plugin = pm.get_plugin("api.plugins.agent.githubdatafetcher")
        plugin.configure(token=token, output_dir=local_folder)
        plugin.set_query_params(
            {"q": repo}
        )
        plugin.run()
        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data={
                "repo": repo,
            }
        )