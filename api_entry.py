# -*- coding: utf-8 -*-
# @Time        : 2024/5/8
# @Author      : liuboyuan

from flask import Flask
from flask_restx import Api


def create_rest_api(application, version, title, description, doc):
    return Api(application, version=version, title=title, description=description, doc=doc)


app = Flask("FischlApi")
rest_api_description = create_rest_api(app,
                                       version="1.0",
                                       title="Fischl Agent API",
                                       description=""
                                                   "Fischl Agent API Documentation",
                                       doc='/'
                                       )
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
# disable Try it Out for all methods
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = []
# enable Try it Out for specific methods
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get", "post"]
