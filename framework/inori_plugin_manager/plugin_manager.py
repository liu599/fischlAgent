# -*- coding: utf-8 -*-
# @Time        : 2024/4/6
# @Author      : liuboyuan
# @Description :


from __future__ import annotations
import importlib
import inspect
import os
import sys
from types import ModuleType
from typing import Optional, Dict, List, Tuple

from .base_plugin import BasePlugin
from inori_log import Logger


def reload_module(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

    # 重新导入模块
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module
    else:
        raise ImportError(f"Module '{module_name}' not found")


class PluginManager:
    plugins: Dict[str: (BasePlugin, ModuleType)] = {}

    def __init__(self, plugin_folder: str, plugin_name='plugin', logger_dir='static'):
        self.plugin_log = Logger(name=plugin_name,
                                 log_dir=logger_dir,
                                 debug=True).logger
        self.load_plugins_from_folder(plugin_folder)


    def test_init(self):
        m = importlib.import_module('test.plugin3')
        print(m)  # module object
        items = inspect.getmembers(m, inspect.isclass)
        print(dict(items))

        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                obj().run()

    def test_update(self):
        new_module = importlib.reload(sys.modules['test.plugin3'])
        print(new_module)

        # 获取模块全部函数
        items = inspect.getmembers(new_module, inspect.isclass)
        print(dict(items))

        for name, obj in inspect.getmembers(new_module):
            if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                obj().run()

    def redirect_log(self, log_dir):
        self.plugin_log = Logger(name='plugin',
                                 log_dir=log_dir,
                                 debug=True).logger

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        return self.plugins.get(name.lower())[0]

    def add_plugin(self, plugin: Tuple[BasePlugin, ModuleType], plugin_name: str):
        name = plugin_name.lower()
        if name in self.plugins:
            print(f'Plugin {name} already registered')
            self.unload_plugin(name)
            # raise ValueError(f"Plugin {name} already exists")
        self.plugins[name] = plugin

    def get_plugin_list(self) -> List[str]:
        return list(self.plugins.keys())

    def register_module(self, module: ModuleType, module_name: str) -> None:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                plugin_instance = obj()
                self.add_plugin((plugin_instance, module), module_name)
                self.plugin_log.info(f"Registered plugin - {module_name}:{name}:{obj}")

    def print_functions(self, module: ModuleType):
        items = inspect.getmembers(module, inspect.isclass)
        print(dict(items))

    def load_plugins_from_folder(self, folder: str):
        # Ensure the folder starts with './' for proper relative path handling
        if not folder.startswith('./'):
            folder = './' + folder

        # Get absolute path from relative path
        folder = os.path.abspath(folder)

        # Extract the root package name from the folder path
        root_package = folder[len(os.getcwd()) + 1:].replace(os.sep, '.')
        self.plugin_log.info(f"Scanning plugins from folder: {root_package}")

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if file.endswith(".py") and file != "__init__.py":
                module_name = f"{root_package}.{file[:-3]}"
                try:
                    if module_name in self.plugins:
                        self.unload_plugin(module_name)
                        self.plugin_log.info(f"Reloading module: {module_name}")
                        module = importlib.reload(sys.modules[module_name])
                        self.register_module(module, module_name)
                    else:
                        self.plugin_log.info(f"Importing new module: {module_name}")
                        module = importlib.import_module(module_name)
                        self.register_module(module, module_name)
                except Exception as e:
                    self.plugin_log.opt(exception=e).error(f"Invalid Python file with grammar error: {e}")
                    continue

            elif os.path.isdir(file_path) and not file.startswith("__"):
                self.load_plugins_from_folder(file_path)

    def unload_plugin(self, name):
        self.plugins.pop(name, None)
        self.plugin_log.info(f"plugin {name} unload")
