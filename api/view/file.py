# -*- coding: utf-8 -*-
# @Time        : 2024/5/10
# @Author      : liuboyuan
# @Description :

import os

from api.view.base.view import BaseView
from api.constants.status_code import Codes
from logger import s_log
from api_entry import rest_api_description as api
from flask_restx import Namespace, fields
import uuid

file_api_namespace = Namespace("文件上传", description='文件上传, 接口定义')


@file_api_namespace.route("")
class FileView(BaseView):


    file_payload = api.model('批量创建文件', {
        'file': fields.String(required=True, description='数组, 二进制文件, 为blob类型'),
        'userid': fields.Integer(required=True, min=1, description='user id, 为数字'),
        'keepOriginalName': fields.Boolean(required=False, description='是否在上传中保留原文件名')
    })

    @file_api_namespace.doc(body=file_payload)
    def post(self):
        """
        上传文件

        :body: 批量上传文件
        :return: 文件路径


        """
        files = self.request.files.getlist('file')
        s_log.debug(files)
        if len(files) == 0:
            return self.response_raw(
                code=Codes.PARAMS_CHECK_FAILED.code,
                msg=f'失败原因: 没有提供文件',
                data={
                    "data": []
                }
            )
        userid = self.request.form.get('userid')
        # s_log.debug(self.request)
        force_original_name = self.request.form.get('keepOriginalName', False)
        uploaded_files_info = []

        for file in files:
            if file.filename == '':
                continue

            filename = file.filename
            file_root = os.getcwd()
            _tmp_storage_folder = os.path.join(file_root, 'static', userid)
            if not force_original_name:
                _storage_file_name = f'{str(uuid.uuid4())[:8]}{filename}'
            else:
                _storage_file_name = filename
            if not os.path.exists(_tmp_storage_folder):
                os.makedirs(_tmp_storage_folder)
            _target_storage_file_name = os.path.join(_tmp_storage_folder, _storage_file_name)
            if os.path.exists(_target_storage_file_name):
                os.remove(_target_storage_file_name)
            file.save(_target_storage_file_name)
            uploaded_files_info.append(_storage_file_name)

        return self.response_raw(
            code=Codes.SUCCESS.code,
            msg=Codes.SUCCESS.desc,
            data={
                "reviewPath": f"{self.base_url}/{userid}",
                "files": uploaded_files_info
            }
        )
