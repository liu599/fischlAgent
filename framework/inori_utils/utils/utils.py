from datetime import datetime
import json
import time


def replace_for_unix(f):
    return f.replace("\\", "/")


def timestringstamp() -> str:
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def unixtimestamp() -> int:
    # print("call unix to get timestamp")
    return int(datetime.now().timestamp())


def find_key_for_value(data, target_value):
    for item in data:
        for key, value in item.items():
            if value == target_value:
                return key
    return None


def is_empty_dict(obj):
    return isinstance(obj, dict) and len(obj) == 0


def generate_answer_pairs(N):
    result = []
    for i in range(1, N + 1):
        east_str = f"参考答案{i}"
        west_str = f"答案权重{i}"
        result.append((east_str, west_str))
    return result


def filter_ip(ip):
    ip = ip.replace('.', '-')
    ip = ip.replace(':', '-')
    return ip


def file_writer(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
    f.close()


def flatten(lst):
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])