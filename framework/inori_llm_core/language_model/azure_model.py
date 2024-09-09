# -*- coding: utf-8 -*-
# @Time        : 2024/6/14
# @Author      : liuboyuan
import os
from framework.inori_llm_core.language_model.base import BaseLanguageModel
from langchain_openai import AzureChatOpenAI
from framework.inori_llm_core.prompt import ProjectChatTemplate


class AzureModel(BaseLanguageModel):
    def __init__(self, model_name: str, api_version: str, api_endpoint: str, api_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model_name
        os.environ["AZURE_OPENAI_ENDPOINT"] = api_endpoint
        os.environ["AZURE_OPENAI_API_KEY"] = api_key
        self.client = AzureChatOpenAI(
            model_name=model_name,
            openai_api_version=api_version,
            temperature=0,
            verbose=True
        )

    def langchain_request(self, message: dict, human_prompt="{input}", system_prompt="") -> (str, dict, str):
        prompt = ProjectChatTemplate(human_prompt, system_prompt, with_history=False).chat_prompt_template
        self.logger.debug(prompt)
        chain = prompt | self.client
        try:
            self.logger.debug(message)
            res = chain.invoke(message)
            self.logger.debug(res)
            return res.content.strip(), res.response_metadata, res.id
        except Exception as e:
            return f"发生了错误：{e}", {}, "exception-id-xx"
            # raise Exception(f"发生了未知错误：{e}")
