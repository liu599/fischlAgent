# -*- coding: utf-8 -*-
# @Time        : 2024/5/18
# @Author      : liuboyuan
# @Description :

# used in sd api
def update_nested_key(data, key, new_values):
    """
    递归更新嵌套字典中指定键的值。

    :param data: 需要更新的嵌套字典。
    :param key: 要查找并更新的键名。
    :param new_values: 要添加到列表的新值，可以是单个值或列表。
    :return: 更新后的字典。
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key and isinstance(v, list):
                # 确保new_values是一个列表
                if not isinstance(new_values, list):
                    new_values = [new_values]
                # data[k].extend(new_values)  # 更新列表
                data[k][0].update(new_values[0])
            else:
                update_nested_key(v, key, new_values)  # 递归调用
    elif isinstance(data, list):
        for item in data:
            update_nested_key(item, key, new_values)  # 处理列表中的每个元素
    return data


def update_dict_list(row_item, key, value):
    """
    向指定字典的列表型值中添加一个元素。

    参数:
    row_item (dict): 要更新的字典。
    key (str): 字典中要更新的键名，对应的值应为列表类型。
    value: 要添加到列表中的值。

    异常:
    ValueError: 如果key对应的值不是列表，将抛出此异常。
    """
    # 检查键是否存在且对应的值是列表
    if key in row_item and isinstance(row_item[key], list):
        row_item[key].append(value)
    else:
        raise ValueError(f"键'{key}'不存在或对应的值不是一个列表。")
