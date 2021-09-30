#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import os.path
import json
import logging
import yaml

logger = logging.getLogger()


default_config = {
    "platform": "ide",
    "app": "wx",
    "debug_mode": "debug",
    "close_ide": False,         # 是否关闭IDE
    "assert_capture": True,
    "auto_relaunch": True,
    "device_desire": {},
    "account_info": {},
    "report_usage": True,
    "remote_connect_timeout": 180,  # 远程连接超时
    "request_timeout": 60,      # 请求超时
    "use_push": True,
    "full_reset": False,
    "outputs": None,
    "enable_app_log": False,
    "enable_network_panel": False,
    "project_path": None,
    "dev_tool_path": None,
    "test_port": 9420,
    "mock_native_modal": {},    # 仅在IDE生效, mock所有会有原生弹窗的接口
    "mock_request": [],         #  mock request接口，item结构为{rule: {}, success or fail}, 同app.mock_request参数
}


def get_log_level(debug_mode):
    return {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "warn": logging.WARNING,
        "error": logging.ERROR,
    }.get(debug_mode, logging.INFO)


class MiniConfig(dict):
    def __init__(self, from_dict=None):
        for k, v in default_config.items():
            setattr(self, k, v)
        if from_dict is None:
            self.is_default_config = True
        else:
            self.is_default_config = False
            for k, v in from_dict.items():
                setattr(self, k, v)
        super(MiniConfig, self).__init__(self.__dict__)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def from_file(cls, filename):
        logger.info("load config from %s", filename)
        _, ext = os.path.splitext(filename)
        f = open(filename, "rb")
        if ext == ".json":
            json_dict = json.load(f)
        elif ext == ".yml" or ext == ".yaml":
            json_dict = yaml.load(f)
        else:
            raise RuntimeError(f"unknown extension {ext} for {filename}")
        f.close()
        if isinstance(json_dict, list):
            config_list = list()
            for c in json_dict:
                config_list.append(MiniConfig(c))
            return config_list
        return MiniConfig(json_dict)


if __name__ == "__main__":
    a = MiniConfig({"outputs": "xxxx"})
    print(a.outputs)
    print(a.sss)
