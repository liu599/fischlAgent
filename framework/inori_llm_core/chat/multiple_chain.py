# -*- coding: utf-8 -*-
# @Time        : 2024/9/9
# @Author      : liuboyuan
# @Description :
from operator import itemgetter
from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from framework.inori_llm_core.language_model.azure_model import AzureModel
from framework.inori_llm_core.language_model.gpt4_model import Gpt4Model
from langchain.callbacks.tracers import ConsoleCallbackHandler
# https://stackoverflow.com/questions/77625508/how-to-activate-verbosity-in-langchain
# from langchain.globals import set_debug
#
# set_debug(True)


def multiple_chain_chat_sample(chat_message: Dict, models: List, human_template: str = "生成关于以下内容的论点: {input}", system_prompt: str = "给出批评后生成最终评论") -> str:
    clients = []
    for model in models:
        client = None
        if model['model_name'] == 'azure':
            client = AzureModel(**model['model_config'])
        if model['model_name'] == 'gpt4':
            client = Gpt4Model(**model['model_config'])
        if client is None:
            raise Exception("No supported client found")
        clients.append(client)
    planner = (
        ChatPromptTemplate.from_template(human_template)
        | clients[0].client
        | StrOutputParser()
        | {"base_response": RunnablePassthrough()}
    )
    arguments_for = (
        ChatPromptTemplate.from_template("列出关于 {base_response} 正确或有利的方向, 严格按照要求不要给出其他观点")
        | clients[0].client
        | StrOutputParser()
    )
    arguments_against = (
        ChatPromptTemplate.from_template("列出关于 {base_response} 反面或不利的方向, 严格按照要求不要给出其他观点")
        | clients[0].client
        | StrOutputParser()
    )

    final_responder = (
        ChatPromptTemplate.from_messages([
                ("ai", "{original_response}"),
                ("human", "正面观点：\n{results_1}\n反面观点：\n{results_2}\n"),
                ("system", system_prompt),
        ])
        | clients[0].client
        | StrOutputParser()
    )
    #
    chain = (
        planner
        | {
            "results_1": arguments_for,
            "results_2": arguments_against,
            "original_response": itemgetter("base_response"),
        }
        | final_responder
    )

    return chain.invoke(chat_message, config={'callbacks': [ConsoleCallbackHandler()]})