# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import os
from datetime import datetime
import markdown2
from api.view.base.view import BaseView
from api.constants.status_code import Codes
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields

from framework.inori_llm_core.chat.chat import llm_chat
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
        'dryRun': fields.Integer(description='dry run Feature Flag, only print prompt to LLM', example=1),
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
        file_path, updates = plugin.run()
        system_prompt = ""
        system_prompt_file_path = self.prompts
        with open(system_prompt_file_path, 'r', encoding='utf-8') as file:
            system_prompt = file.read()
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        if 'dryRun' in params:
            print(system_prompt)
            print(file_content)
            print(updates['info']['repo'])
            html_report = markdown2.markdown(file_content)
            with open(f"static/{os.path.basename(file_path)}.html", 'w', encoding='utf-8') as file:
                file.write(html_report)
            return self.response_raw(
                code=Codes.SUCCESS.code,
                msg=Codes.SUCCESS.desc,
                data=None
            )
        else:
            chat_message_body = llm_chat("azure", self.azure_model_config, "{input}", system_prompt, {
                "input": file_content
            })
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{updates['info']['repo']}-{days}-{updates['info']['from']}-{timestamp}.md"
            content = chat_message_body["content"]
            with open(f"static/{filename}", 'w', encoding='utf-8') as file:
                file.write(content)
            with open(f"static/{filename}.html", 'w', encoding='utf-8') as file:
                file.write(markdown2.markdown(content))

            return self.response_raw(
                code=Codes.SUCCESS.code,
                msg=Codes.SUCCESS.desc,
                data={
                    "report_file_path": f"{self.base_url}/static/{os.path.basename(file_path)}",
                    "gpt_report_file_path": f"{self.base_url}/static/{filename}.html",
                    "metadata": chat_message_body["metadata"]
                }
            )