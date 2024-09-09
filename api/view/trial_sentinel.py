# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import os

from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields

from framework.inori_plugin_manager.plugin_manager import PluginManager

agent_api_namespace = Namespace("Agent测试", description='测试, 接口定义')

@agent_api_namespace.route("")
class LLMAgentView(BaseView):

    @agent_api_namespace.doc()
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

    agent_payload = api.model('AgentPayload', {
        'repo': fields.String(description='repo name', example='repo:langchain-ai/langchain', required=True),
        'days': fields.Integer(description='days', example=5),
    })

    @agent_api_namespace.doc(body=agent_payload)
    def post(self):
        """
        调用Github Agent并存储

        :body: task_payload
        :return: task_id
        """
        params = self.request.json
        repo = params['repo']
        days = params['days']
        local_folder = self.api_config.get('data', 'local_folder')
        token = self.api_config.get('github', 'token')
        pm = PluginManager("./api/plugins/agent")
        print(pm.get_plugin_list())
        plugin = pm.get_plugin("api.plugins.agent.githubdatafetcher")
        plugin.configure(token=token, output_dir=local_folder, days=int(days))
        plugin.set_query_params(repo)
        file_path = plugin.run()
        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data={
                "file_path": f"http://localhost:5010/static/{os.path.basename(file_path)}",
            }
        )