#!/usr/bin/env python3
# Created by xiazeng on 2019-05-31
import sys
import os.path
import argparse
# import unittest
import logging.handlers
import json
import glob
import fnmatch
import copy
import time
import websocket
import threading

from .minisuite import MiniSuite
from .session import Session
from multiprocessing import Queue
from minium import build_version
from minium.framework import case_inspect
from minium.framework import minitest
from minium.framework import miniconfig
from minium.framework import miniresult
from minium.miniprogram.wx_minium import WXMinium
from minium.framework.exception import *
from minium.framework.libs import unittest
unittest.TestLoader.suiteClass = unittest.TestSuite

logger = logging.getLogger()
g_case_list = []
FILENAME_SUMMARY = "summary.json"
is_connected = False
test_response = None

def run_tests(tests, mini_suite):
    result = miniresult.MiniResult(mini_suite=mini_suite)
    tests.run(result)
    result.print_shot_msg()
    return result


def load_from_suite(case_path, json_path):
    """
    从json文件或者 json 字符串中获取用例筛选规则，并加载用例
    :param case_path: 用例存放的路径
    :param json_path:
    :return:
    """
    if isinstance(json_path, (str, bytes)) and os.path.exists(json_path):
        mini_suite = MiniSuite(json_path)
    elif isinstance(json_path, dict):
        mini_suite = MiniSuite()
        mini_suite.suite_json = json_path
    elif isinstance(json_path, str):
        try:
            suite_dict = json.loads(json_path)
            mini_suite = MiniSuite()
            mini_suite.suite_json = suite_dict
        except MiniParamsError as e:
            raise Exception(
                f"Suite param not file neither dict or formatted json string: {e}"
            )
    else:
        raise Exception("Suite param not file neither dict or formatted json string")
    tests = None
    logger.debug("==========Scan Cases from suite===========")
    for pkg_cases in mini_suite.pkg_list:
        tests = unittest.TestSuite()
        pkg = pkg_cases["pkg"]
        case_list = pkg_cases["case_list"]
        for case_suite_info in case_list:
            if isinstance(case_suite_info, str):
                case_name = case_suite_info
            else:
                case_name = case_suite_info["name"]
            module_case_info_list = case_inspect.load_module(case_path, pkg)
            for module_name, module_info in module_case_info_list.items():
                logger.debug(f"- {module_name}")
                for case_info in module_info["case_list"]:
                    if fnmatch.fnmatch(case_info["name"], case_name):
                        logger.debug(f"  |--{case_info['name']}")
                        case = load_from_case_name(module_name, case_info["name"])
                        tests.addTests(case)
        g_case_list.append(tests)
    return tests, mini_suite


def load_from_module(module):
    """
    通过包名加载该 package 下所有用例
    :param module:
    :return:
    """
    logger.debug(f"Loading module: {module}")
    loader = unittest.TestLoader()
    test_module = case_inspect.import_module(module)
    tests = loader.loadTestsFromModule(test_module)
    logger.debug(f"put module[{module}] into queue")
    g_case_list.append(tests)
    return tests


def load_single_case(module, case_name):
    """
    加载单条 case
    :param module:
    :param case_name:
    :return:
    """
    tests = load_from_case_name(module, case_name)
    g_case_list.append(tests)
    return tests


def load_from_case_name(module, case_name):
    """
    通过包名和用例名加载用例
    :param module:
    :param case_name:
    :return:
    """
    logger.debug(f"Loading Case: {module}.{case_name}")
    loader = unittest.TestLoader()
    test_class = case_inspect.find_test_class(module, case_name)
    if test_class:
        tests = loader.loadTestsFromName(case_name, test_class)
        logger.debug(f"put case[{case_name}] into queue")
        return tests
    else:
        raise AssertionError(
            "can't not find testcase %s in module %s" % (case_name, module)
        )


def main():
    # bug: 在 fork 模式下Python 会出现 crash
    # crashed on child side of fork pre-exec
    # Invalid dylib load. Clients should not load the unversioned libcrypto dylib as it does not have a stable ABI.
    import multiprocessing

    multiprocessing.set_start_method("spawn")
    # 解析参数
    parsers = argparse.ArgumentParser()
    parsers.add_argument(
        "-v", "--version", dest="version", action="store_true", default=False
    )
    parsers.add_argument(
        "-p",
        "--path",
        dest="path",
        type=str,
        help="case directory, default current directory",
        default=None,
    )
    parsers.add_argument(
        "-m",
        "--module",
        dest="module_path",
        type=str,
        help="case package name, usually means a python file name",
    )
    parsers.add_argument(
        "--case",
        dest="case_name",
        type=str,
        default=None,
        help="case name, usually means a function",
    )
    parsers.add_argument(
        "--module_search_path",
        dest="sys_path_list",
        nargs="*",
        help="you can add some custom module into sys path by this param",
    )
    parsers.add_argument(
        "--apk",
        dest="apk",
        action="store_true",
        default=False,
        help="show apk path which may you need to install before running test in android device",
    )
    parsers.add_argument(
        "-s",
        "--suite",
        dest="suite_path",
        type=str,
        default=None,
        help="test suite file, a json format file or just a json string",
    )
    parsers.add_argument(
        "-c", "--config", dest="config", type=str, default=None, help="config file path"
    )
    parsers.add_argument(
        "-g",
        "--generate",
        dest="generate",
        action="store_true",
        default=False,
        help="generate html report",
    )

    parsers.add_argument(
        "--mode",
        dest="run_mode",
        type=str,
        default="fork",
        help="cases run mode, parallel or fork",
    )

    parsers.add_argument(
        "-a",
        "--accounts",
        dest="accounts",
        action="store_true",
        help="get accounts which already login",
    )

    parsers.add_argument(
        "--only-native",
        dest="only_native",
        action="store_true",
        help="Only init native driver",
    )
    
    parsers.add_argument(
        "--test-connection",
        dest="test_connection",
        action="store_true",
        help="test connection between minium and ide",
    )
    
    parsers.add_argument(
        "--test-port",
        dest="test_port",
        type=str,
        default="9420",
        help="test connection port, default: 9420",
    )

    parsers.format_help()

    parser_args = parsers.parse_args()
    version = parser_args.version
    path = parser_args.path
    module = parser_args.module_path
    apk = parser_args.apk
    case_name = parser_args.case_name
    generate_report = parser_args.generate
    suite_path = parser_args.suite_path
    config = parser_args.config
    sys_path_list = parser_args.sys_path_list
    show_accounts = parser_args.accounts
    run_mode = parser_args.run_mode
    only_native = parser_args.only_native
    test_connection = parser_args.test_connection
    test_port = parser_args.test_port

    if show_accounts:
        # 打印已登录的多账号
        print(WXMinium().get_test_accounts())
        exit(0)
        
    if test_connection:
        # 测试ws链接是否正常
        def on_open(ws):
            global is_connected
            print("connection opened")
            is_connected = True
        def on_error(ws, error):
            print("error: %s"%str(error))
            exit(1)
        def on_message(ws, message):
            global test_response
            print("receive: %s"%message)
            message = json.loads(message)
            if message["id"] == "minitest-test-id":
                test_response = message
        def on_close(ws):
            global is_connected
            print("closed")
            is_connected = False
        url = "ws://localhost:{}".format(test_port)
        print("start connect {}".format(url))
        client = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        def run_forever():
            client.run_forever()
        thread = threading.Thread(target=run_forever, args=())
        thread.daemon = True
        thread.start()
        s = time.time()
        while time.time() - s < 10:
            if is_connected:
                print("connect to WebChatTools successfully")
                print("连接开发者工具成功")
                break
            time.sleep(1)
        else:
            print("connect WebChatTools fail, please confirm the test port is open")
            print("连接开发者工具失败，可能的原因有:")
            print("1. 没有打开自动化测试端口，请检查开发者工具的通知栏是否有: 小程序的自动化端口已开启，端口号是 xxxx")
            print("2. 调试基础库版本过低，请选择最新版本")
            exit(1)
        message = json.dumps(
            {"id": "minitest-test-id", "method": "App.callWxMethod", "params": {"method": "getSystemInfoSync", "args": []}}, separators=(",", ":")
        )
        client.send(message)
        s = time.time()
        while time.time() - s < 30:
            if test_response:
                print("response successfully")
                print("收到命令返回")
                break
            time.sleep(1)
        else:
            print("can't receive response, please confirm miniprogram is launch successfully")
            print("未收到命令返回，请确认小程序项目是否正确运行(没有白屏/报错)")
            exit(1)
        client.close()
        exit(0)

    if sys_path_list:
        # 添加 package 寻找路径到 sys.path
        for sys_path in sys_path_list:
            logger.info("insert %s to sys.path", sys_path)
            sys.path.insert(0, sys_path)

    if version:
        # 打印 minium 版本信息
        print(build_version())
        exit(0)

    if apk:
        # 打印 android uiautomator 相关的 apk 包路径
        bin_root = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "native",
            "lib",
            "at",
            "bin",
            "*apk",
        )
        print("please install apk:")
        for filename in glob.glob(bin_root):
            print(f"adb install -r {filename}")
        exit(0)

    if path is None:
        # 用例目录路径
        logger.debug("case directory path not specified, use current path")
        path = os.getcwd()

    if not os.path.exists(path) or not os.path.isdir(path):
        logger.error("case directory: %s not exists" % path)
        parsers.print_help()
        exit(0)

    sys.path.insert(0, path)

    # 提前预加载默认配置，否则处理 suite 的时候logger 参数不生效
    minitest.AssertBase.setUpConfig(default=True)

    # 处理 suite、case、module 参数
    if suite_path:
        load_from_suite(path, suite_path)
    elif module is None:
        # raise RuntimeError("suite_path or pkg is necessary")
        logger.error("suite_path or module_path is necessary at least one")
        parsers.print_help()
        exit(0)
    elif case_name is None:
        load_from_module(module)
    else:
        load_single_case(module, case_name)

    # 处理 config 参数
    if config and not os.path.exists(config):
        # raise RuntimeError("config not exists:%s" % config)
        logger.error("config not exists:%s" % config)
        parsers.print_help()
        exit(0)
    conf_list = []
    if config:
        conf_list = miniconfig.MiniConfig.from_file(config)
        conf_list = [conf_list] if not isinstance(conf_list, list) else conf_list
    else:
        conf_list.append(miniconfig.MiniConfig())

    # 启动 session
    session_list = list()
    q = Queue()
    for tests in g_case_list:
        q.put(tests)
    for c in conf_list:
        new_q = Queue()
        if run_mode == "fork":
            for tests in copy.deepcopy(g_case_list):
                new_q.put(tests)
            q = new_q
        if only_native:
            c.only_native = True
        logger.info(f"start session with {run_mode} mode \n{c}\n")
        s = Session(conf=c, queue=q, generate_report=generate_report)
        s.start()
        session_list.append(s)

    for se in session_list:
        se.join()

    exit(0)


if __name__ == "__main__":
    main()
