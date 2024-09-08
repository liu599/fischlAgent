# -*- coding: utf-8 -*-
# @Time        : 2024/3/27
# @Author      : liuboyuan


from enum import unique
from api.constants.base_enum import EnumBase


@unique
class Codes(EnumBase):
    """API状态枚举值"""
    # 20000～30000 预留系统状态
    SUCCESS = (20000, '操作成功')
    FAILURE = (20001, '操作失败')
    LOGOUT = (20002, '退出登陆成功')
    TOKEN_INVALID = (20003, 'token失效')
    INVALID_PARAMS = (20010, '无效参数')
    PARAMS_CHECK_FAILED = (20011, '参数检查失败')

    # 30001～40000 预留业务状态
    NO_DATA = (30001, '未查询到数据')
