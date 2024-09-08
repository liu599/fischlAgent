#!flask/bin/python
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# CORS
from flask_cors import CORS
# Router
from api.router import init_app_router
# APP及Router description
from api_entry import app, rest_api_description
# encoder
from framework.inori_utils.utils import NumpyEncoder
# log
from logger import s_log

# api中间件
# import api.middleware.modify_mime



app.json = NumpyEncoder(app)
s_log.info("初始化json numpy序列化工具")


CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "PUT", "POST", "OPTIONS", "DELETE", "PATCH"],
    "allowed_headers": [
        "Origin", "Content-Length",
        "Content-Type", "User-Agent",
        "Referrer", "Host", "Token",
        "User", "Authorization", "Uuid", "Auth-Server",
        "X-Requested-With"],
}}, supports_credentials=True)


if os.environ.get('WORKER_ENV') == 'prod':
    # 生产环境路由不需要前缀
    s_log.info('running in production mode')
    init_app_router(rest_api_description, '')
else:
    s_log.info("running in development mode")
    init_app_router(rest_api_description, '/fischl_api/v1')

if __name__ == '__main__':
    # 运行程序
    app.run(host='0.0.0.0', port=5010, debug=False)
