# -*- coding: utf-8 -*-
# @Time        : 2024/6/14
# @Author      : liuboyuan
import os
from typing import Any

from langchain_openai import ChatOpenAI
from framework.inori_llm_core.language_model.base import BaseLanguageModel
from framework.inori_llm_core.prompt import ProjectChatTemplate


class Gpt4Model(BaseLanguageModel):
    def __init__(self, api_key: str, user_name: str, model: str = "gpt-4", *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.environ["OPENAI_API_KEY"] = api_key
        self.client = ChatOpenAI(
            model=model,
            temperature=0.7,
            max_tokens=2048
        )

    def langchain_request(self, message: dict, human_prompt="{input}", system_prompt="", **kwargs) -> (str, Any, Any):
        prompt = ProjectChatTemplate(human_prompt, system_prompt, with_history=False).chat_prompt_template
        self.logger.debug(prompt)
        chain = prompt | self.client
        try:
            self.logger.debug(message)
            res = chain.invoke(message)
            self.logger.debug(res)
            return res.content.strip(), res.response_metadata, res.id
        except Exception as e:
            return f"发生了错误：{e}", {}, ""
