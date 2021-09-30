#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: client 入口
@Date: 2019-03-11 14:42:52
@LastEditTime: 2019-06-05 15:05:04
"""
import platform
import os
import base64
import json
from .base_driver.app import App
from .base_driver.connection import Connection
from .base_driver.minium_object import MiniumObject
from ..framework.miniconfig import MiniConfig
from ..framework.exception import *

LOG_FORMATTER = "%(levelname)-5.5s %(asctime)s %(filename)-10s %(funcName)-15s %(lineno)-3d %(message)s"

MAC_DEVTOOL_PATH = "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"
WINDOWS_DEVTOOL_PATH = "cli"
TEST_PORT = 9420
UPLOAD_URL = "https://stream.weixin.qq.com/weapp/UploadFile"

# source_path是存放资源文件的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(os.path.dirname(cur_path), "wx_resources")
if not os.path.exists(resource_path):
    os.mkdir(resource_path)


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


class WXMinium(MiniumObject):
    """
    自动化入口
    """

    def __init__(self, conf: MiniConfig = None, uri="ws://localhost"):
        """
        初始化
        :param uri: WebSocket 地址
        :param conf: 配置
        """
        super().__init__()
        if not conf:
            conf = MiniConfig()
        elif isinstance(conf, dict):
            conf = MiniConfig(conf)
        self.conf = conf
        self.version = build_version()
        self.logger.info(self.version)
        self.start_cmd = ""
        self.app = None
        self.connection = None
        test_port = (
            str(conf.test_port) if conf.get("test_port", None) else str(TEST_PORT)
        )
        self.uri = uri + ":" + test_port
        self.test_port = test_port
        self.open_id = conf.get("account_info", {}).get("open_id", None)
        self.ticket = conf.get("account_info", {}).get("ticket", None)
        self.project_path = conf.get("project_path", None)
        self.is_remote = False

        if conf.get("dev_tool_path", None):
            self.dev_tool_path = conf.dev_tool_path
        elif "Darwin" in platform.platform() or "macOS" in platform.platform():
            self.dev_tool_path = MAC_DEVTOOL_PATH
        elif "Windows" in platform.platform():
            self.dev_tool_path = WINDOWS_DEVTOOL_PATH
        else:
            self.logger.warning("Dev tool doesn't support current OS yet")
        self._is_windows = "Windows" in platform.platform()

        self.launch_dev_tool()

        if conf.get("platform", None) != "ide":
            path = self.enable_remote_debug(
                use_push=conf.get("use_push", True),
                connect_timeout=conf.get("remote_connect_timeout", 180),
            )
            self.qr_code = path

    def _dev_cli(self, cmd):
        if not self.dev_tool_path or not os.path.exists(self.dev_tool_path):
            raise MiniConfigError("dev_tool_path: %s not exists" % self.dev_tool_path)
        if self._is_windows:
            cmd_template = '"%s"  %s'
        else:
            cmd_template = "%s %s"
        return self._do_shell(cmd_template % (self.dev_tool_path, cmd))

    def launch_dev_tool(self):
        # start dev tool with minium model
        self.logger.info("Starting dev tool and launch MiniProgram project ...")

        if self.project_path:
            if not os.path.exists(self.project_path):
                raise MiniConfigError("project_path: %s not exists" % self.project_path)
            if not os.path.isdir(self.project_path):
                raise MiniConfigError(
                    "project_path: %s is not directory" % self.project_path
                )

            self.start_cmd = "auto --project %s --auto-port %s" % (
                self.project_path,
                self.test_port,
            )
            if self.open_id:
                self.start_cmd += f" --auto-account {self.open_id}"
            elif self.ticket:
                self.start_cmd += f" --test-ticket {self.ticket}"
            status = self._dev_cli(self.start_cmd)
            # wait ide init
            if self._is_windows:
                # windows更卡
                time.sleep(10)
            else:
                time.sleep(5)
            if status[-1] == "" or "Port %s is in use" % self.test_port in "".join(
                status
            ):
                try:
                    self.connect_dev_tool()
                    return
                except (MiniConnectError, MiniLaunchError) as e:
                    self.logger.error(f"{str(e)}, restart now...")
                    if self.connection:
                        self.connection.send("Tool.close")
                    elif "--auto-account" not in self.start_cmd:
                        self._dev_cli(f"close --project {self.project_path}")
                    else:
                        raise MiniLaunchError(
                            "In the case with multi-account mode and no connection with dev tool,"
                            " the only things I can do is abandon this session"
                        )
                    time.sleep(5)
                    self.logger.info("Starting dev tool again...")
                    status = self._dev_cli(self.start_cmd)
                    if status[-1] == "":
                        raise MiniLaunchError(
                            "Please check MiniProgram project config, "
                            "some error lead to Dev tool can not open project successfully"
                        )
                    else:
                        self.logger.info("Restart success")
                        time.sleep(5)
        else:
            self.logger.warning(
                "Can not find project_path in config, that means you must open dev tool by automation way first"
            )
            status = ["auto"]
        if "auto" in status[-1]:
            try:
                self.connect_dev_tool()
            except MiniConnectError as e:
                self.logger.warning(
                    "Please ensure your local address like 127.0.0.1 or localhost is not pass by proxy"
                )
                self.logger.warning(
                    "Please ensure the version of base lib in dev tool is upper than 2.7.5"
                )
                self.logger.warning(
                    "Try to set a bigger number into request_time in config"
                )
                raise e
            except MiniLaunchError as e:
                self.logger.error(f"{str(e)}, restart now...")
                self.connection.send("Tool.close")
                time.sleep(5)
                self.logger.info("Starting dev tool again...")
                self._dev_cli(self.start_cmd)
                self.connect_dev_tool()
        else:
            raise MiniLaunchError(
                "Open project in automation mode fail! Please ensure you have permission of project and have not "
                "environ error "
            )
            # self.launch_dev_tool_with_login()

    def connect_dev_tool(self):
        i = 3
        while i:
            try:
                self.logger.info("Trying to connect Dev tool ...")
                connection = Connection(
                    self.uri, timeout=self.conf.get("request_timeout")
                )
                self.connection = connection
                self.app = App(connection, self.conf.get("auto_relaunch"))
            except Exception as e:
                self.logger.exception(e)
                i -= 1
                if i == 0:
                    raise MiniConnectError(
                        "three times try to connect Dev tool has all fail ..."
                    )
                continue
            else:
                break
        return True

    def launch_dev_tool_with_login(self):
        # start dev tool with minium model
        cmd_start = "-l --login-qr-output terminal --auto --auto %s --auto-port %s" % (
            self.project_path,
            self.test_port,
        )
        status = self._dev_cli(cmd_start)
        if "Open project with automation enabled success " in status[-1]:
            connection = Connection(self.uri)
            self.app = App(connection)
            self.connection = connection
        else:
            self.logger.error(
                "Open project in automation mode fail! make sure project path is right"
            )
            exit(-1)

    def get_app_config(self):
        """
        获取 app 的配置
        :return: object
        """
        return (
            self.evaluate("function () {return __wxConfig}", sync=True)
            .get("result", {"result": {}})
            .get("result", None)
        )

    def get_system_info(self):
        """
        获取系统信息
        :return:
        """
        return (
            self.app.call_wx_method("getSystemInfoSync")
            .get("result", {"result": {}})
            .get("result", None)
        )

    def enable_remote_debug(self, use_push=True, path=None, connect_timeout=180):
        self.reset_remote_debug()
        time.sleep(2)
        if use_push:
            retry_times = 3
            while retry_times > 0:
                try:
                    self.logger.info(
                        f"Enable remote debug, for the {4 - retry_times}th times"
                    )
                    self.connection.send(
                        "Tool.enableRemoteDebug",
                        params={"auto": True},
                        max_timeout=connect_timeout,
                    )
                    self.is_remote = True
                except Exception as e:
                    retry_times -= 1
                    self.logger.error("enable remote debug fail ...")
                    self.logger.error(e)
                    if retry_times == 0:
                        self.logger.error(
                            "Enable remote debug has been fail three times. Please check your network or proxy "
                            "effective or not "
                        )
                        raise
                    continue
                else:
                    retry_times -= 1
                    rtn = self.connection.wait_for(
                        method="App.initialized", max_timeout=connect_timeout
                    )
                    if retry_times == 0 and rtn is False:
                        self.logger.error(
                            "Wait for APP initialized has been fail three times. Please check your phone's current "
                            "foreground APP is WeChat or not, and check miniProgram has been open or not "
                        )
                        raise MiniLaunchError("Launch APP Error")
                    if rtn is True:
                        break
                    else:
                        self.app.exit()

            return None
        if path is None:
            path = os.path.join(resource_path, "debug_qrcode.jpg")
        qr_data = self.connection.send(
            "Tool.enableRemoteDebug", max_timeout=connect_timeout
        ).result.qrCode
        with open(path, "wb") as qr_img:
            qr_img.write(base64.b64decode(qr_data))

        return path

    def reset_remote_debug(self):
        """
        重置远程调试，解决真机调试二维码扫码界面报-50003 等常见错误
        :return:
        """
        return self.connection.send("Tool.resetRemoteDebug")

    def clear_auth(self):
        """
        清除用户授权信息. 公共库 2.9.4 开始生效
        :return:
        """
        if self.conf.mock_native_modal and self.conf.platform == "ide": # 对授权弹窗MOCK了，需要清除MOCK信息
            self.evaluate("""function() {global.mini_auth_setting = {}}""")
        self.connection.send("Tool.clearAuth")

    def get_test_accounts(self):
        """
        获取已登录的真机账号
        :return: list [{openid, nickName}]
        """
        return self.connection.send("Tool.getTestAccounts").result.accounts

    def shutdown(self):
        """
        关闭 Driver
        :return: status
        """
        try:
            if self.is_remote:
                self.logger.info("MiniProgram closing")
                self.app.exit()
            self.logger.info("Project window closing")
            # if self.project_path:
            #     self._dev_cli(f"close --project {self.project_path}")
            # else:
            self.connection.send("Tool.close")
            time.sleep(5)
        except (MiniTimeoutError, MiniAppError) as e:
            self.logger.exception(f"Shutdown Excrption:{e}")


if __name__ == "__main__":

    mini = WXMinium()
