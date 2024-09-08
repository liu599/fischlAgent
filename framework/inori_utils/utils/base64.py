# -*- coding: utf-8 -*-
# @Time        : 2024/4/23
# @Author      : liuboyuan

import base64


def base64_encoder(char: str, length=4) -> str:
    binary_data = char.encode()
    padded = binary_data + b'\x00' * (3 - (len(binary_data) % 3))  # 添加填充以确保能被3整除
    encoded = base64.b64encode(padded)[:length].decode().replace('/', '-')  # 使用'-'替换'/'
    return encoded


def base64_decoder(encoded: str) -> str:
    decoded_binary = base64.b64decode(encoded.replace('-', '/'))  # 使用'/'替换'-'
    decoded_text = decoded_binary.rstrip(b'\x00').decode()
    return decoded_text


def encode_base64(text: str) -> str:
    return "".join(base64_encoder(char) for char in text).strip()


def decode_base64(text: str) -> str:
    return "".join(base64_decoder(encoded) for encoded in text).strip()


def image_to_base64(image_path):
    """
    将图片文件转换为Base64编码字符串。

    :param image_path: 图片文件的路径
    :return: Base64编码的字符串
    """
    with open(image_path, "rb") as image_file:
        # 读取图片的二进制数据
        encoded_string = base64.b64encode(image_file.read())
        # 将二进制数据转换为字符串并移除换行符（如果有的话）
        return encoded_string.decode('utf-8')


def encode_credentials(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials
