#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: client 入口
@Date: 2019-03-11 14:42:52
@LastEditTime: 2019-06-05 15:05:04
"""
import os
import json
from .app import App
from .connection import Connection
from .minium_object import MiniumObject

LOG_FORMATTER = "%(levelname)-5.5s %(asctime)s %(filename)-10s %(funcName)-15s %(lineno)-3d %(message)s"

MAC_DEVTOOL_PATH = "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"
WINDOWS_DEVTOOL_PATH = "cli"
TEST_PORT = 9420
UPLOAD_URL = "https://stream.weixin.qq.com/weapp/UploadFile"


class LogLevel(object):
    INFO = 20
    DEBUG_SEND = 12
    METHOD_TRACE = 11
    DEBUG = 9


def build_version():
    config_path = os.path.join(os.path.dirname(__file__), "version.json")
    if not os.path.exists(config_path):
        return {}
    else:
        with open(config_path, "rb") as f:
            version = json.load(f)
            return version


class Minium(MiniumObject):
    """
    自动化入口
    """

    app: App
    connection: Connection

    def __init__(self, conf=None, uri="ws://localhost"):
        ...

    def launch_dev_tool(self):
        ...

    def connect_dev_tool(self):
        ...

    def launch_dev_tool_with_login(self):
        ...

    def get_app_json(self):
        ...

    def get_system_info(self):
        ...

    def enable_remote_debug(self, use_push=True, path=None, connect_timeout=None):
        ...

    def reset_remote_debug(self):
        ...

    def clear_auth(self):
        ...

    def shutdown(self):
        ...
