# -*- coding: utf-8 -*-
# @Time        : 2024/6/14
# @Author      : liuboyuan
import os
from typing import Any

from langchain_openai import ChatOpenAI
from framework.inori_llm_core.language_model.base import BaseLanguageModel
from framework.inori_llm_core.prompt import ProjectChatTemplate


class Gpt4Model(BaseLanguageModel):
    def __init__(self, api_key: str, model: str = "gpt-4", *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.environ["OPENAI_API_KEY"] = api_key
        self.client = ChatOpenAI(
            model=model,
            temperature=0.7,
            max_tokens=2048,
            top_p=0.7,
            frequency_penalty=0,
            presence_penalty=0.7,
            response_format={
                "type": "text",
            }
        )

    def langchain_request(self, human_prompt, system_prompt="", **kwargs) -> (str, Any, Any):
        prompt = ProjectChatTemplate(human_prompt, system_prompt, with_history=False).chat_prompt_template
        try:
            if system_prompt != "":
                messages = [
                    ("system", system_prompt),
                    ("human", human_prompt),
                ]
            else:
                messages = [
                    ("human", human_prompt),
                ]
            return self.client.invoke(messages).content, {}, ""
        except Exception as e:
            return f"发生了错误：{e}", {}, ""
