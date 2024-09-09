# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
from typing import Dict

from framework.inori_llm_core.language_model.azure_model import AzureModel
from framework.inori_llm_core.language_model.gpt4_model import Gpt4Model


def llm_chat(model_name: str, model_config: Dict, human_template: str, system_prompt: str, chat_message: Dict) -> Dict:
    language_model = None
    if model_name == 'azure':
        language_model = AzureModel(**model_config)
    if model_name == 'gpt4':
        language_model = Gpt4Model(**model_config)
    if language_model is None:
        raise ValueError("Language model not support")

    cf = {
        "human_prompt": human_template,  # {input}
        "message": chat_message,  # 对应需要 {"input": "我的问题"}
        "system_prompt": system_prompt,  # 系统提示词
    }
    content, metadata, run_id = language_model.langchain_request(**cf)

    if 'token_usage' in metadata:
        token_usage = metadata['token_usage']['total_tokens']
    else:
        token_usage = -1

    return {
        "content": content,
        "metadata": metadata,
        "run_id": run_id,
        "total_tokens": token_usage
    }