# -*- coding: utf-8 -*-
# @Time        : 2024/6/14
# @Author      : liuboyuan
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def gen_human_template(template):
    human_base_template = """

Current conversation

{history}

Human: """
    ht = human_base_template + template + """{input}
        AI-Reply:
        """
    return HumanMessagePromptTemplate.from_template(ht)


def gen_system_message_template(template):
    return SystemMessagePromptTemplate.from_template(template)


class ProjectChatTemplate:
    def __init__(self, human_message="", system_message="", with_history=True):
        if with_history:
            self.human_message_prompt = gen_human_template(human_message)
            if system_message != "":
                self.system_message_prompt = gen_system_message_template(system_message)
                self.chat_prompt_template = ChatPromptTemplate.from_messages(
                    [self.system_message_prompt, self.human_message_prompt]
                )
            else:
                self.chat_prompt_template = ChatPromptTemplate.from_messages(
                    [self.human_message_prompt]
                )
        else:
            # 构造单次使用的prompt
            if system_message != "":
                self.chat_prompt_template = ChatPromptTemplate.from_messages(
                    [
                        SystemMessagePromptTemplate.from_template(system_message),
                        HumanMessagePromptTemplate.from_template(human_message)
                    ]
                )
            else:
                self.chat_prompt_template = ChatPromptTemplate.from_messages(
                    [
                        HumanMessagePromptTemplate.from_template(human_message)
                    ]
                )
