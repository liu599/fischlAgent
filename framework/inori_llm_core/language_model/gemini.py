# -*- coding: utf-8 -*-
# @Time        : 2024/6/26
# @Author      : liuboyuan
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from workflow.language_model.base import BaseLanguageModel
from workflow.prompt import ProjectChatTemplate
from langchain_core.messages import HumanMessage, SystemMessage


class GeminiModel(BaseLanguageModel):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        os.environ["GOOGLE_API_KEY"] = api_key
        self.client = ChatGoogleGenerativeAI(model="gemini-pro")

    def langchain_request(self, human_prompt, system_prompt="", **kwargs) -> str:
        try:
            return self.client.invoke(human_prompt).content
        except Exception as e:
            return f"发生了错误：{e}"


if __name__ == "__main__":
    api_key = "AIzaSyBX6EvxYGCxMwk49fM9LTEKxatbgyhSt_E"
    model = GeminiModel(api_key)
    res = model.langchain_request(human_prompt="你是什么模型啊")