# -*- coding: utf-8 -*-
# @Time        : 2024/4/18
# @Author      : liuboyuan
import urllib3
import json
from urllib.parse import urlencode
import time
from framework.inori_utils.log_utils import LOG


def http_get(url, params=None):
    timeout = urllib3.Timeout(connect=2.0, read=3.0)
    http = urllib3.PoolManager(num_pools=1, timeout=timeout)
    print(url)
    if params is None:
        resp = http.request('GET', url)
        print(resp)
    else:
        resp = http.request("GET", f"{url}?{urlencode(params)}")
    res = json.loads(resp.data.decode('utf-8'))
    if not isinstance(res, dict):
        res = json.loads(res)

    return resp.status, res


def http_post(url, body=None):
    if body is None:
        body = {}
    http = urllib3.PoolManager()
    resp = http.request("POST", url,
                        headers={'Content-Type': 'application/json'},
                        body=json.dumps(body))
    res = json.loads(resp.data.decode('utf-8'))
    if not isinstance(res, dict):
        print('reloads')
        res = json.loads(res)
    return resp.status, res


def retry_decorator(max_retries=3, delay=1, condition=False):
    """
    重试装饰器。如果被装饰的函数返回False，则会自动重试指定次数。

    :param condition: 在何种情况下执行这个重试装饰器
    :param max_retries: 重试的最大次数，默认为3次。
    :param delay: 每次重试之间的延迟时间（秒），默认为1秒。
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                result = func(*args, **kwargs)
                if result is not condition:
                    return result
                LOG.error(f"Function returned condition {condition}, retrying ({retries + 1}/{max_retries})...")
                retries += 1
                time.sleep(delay)  # 等待一段时间后重试
            LOG.error(f"Failed after {max_retries} retries.")
            return False  # 最大重试次数后仍然失败，返回False

        return wrapper

    return decorator
