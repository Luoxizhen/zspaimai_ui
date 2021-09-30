#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       minium_object.py
Create time:    2019/4/30 21:21
Description:

"""

from .minium_log import MonitorMetaClass
import subprocess
import time
from functools import wraps
import logging

logger = logging.getLogger()


def timeout(duration):
    """
    重试超时装饰器，在超市之前会每隔一秒重试一次
    注意：被修饰的函数必须要有非空返回，这是重试终止的条件！！！
    :param duration: seconds
    :return:
    """

    def spin_until_true(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            timeout = time.time() + duration
            r = func(*args, **kwargs)
            while not r:
                time.sleep(1)
                if timeout < time.time():
                    logger.warning("timeout for %s" % func.__name__)
                    break
                r = func(*args, **kwargs)
            return r

        return wrapper

    return spin_until_true


class MiniumObject(object, metaclass=MonitorMetaClass):
    def __init__(self):
        self.logger = logger
        self.observers = {}
        self.connection = None

    def _do_shell(self, command, print_msg=True):
        """
        执行 shell 语句
        :param command:
        :param print_msg:
        :return:
        """
        self.logger.info("de shell: %s" % command)
        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        lines = []
        for line in iter(p.stdout.readline, b""):
            try:
                line = line.rstrip().decode("utf8")
            except UnicodeDecodeError:
                line = line.rstrip().decode("gbk")
            logger.debug(line)
            lines.append(line)
        return lines

    def call_wx_method(self, method, args=None):
        """
        调用 wx 的方法
        :param method:
        :param args:
        :return:
        """
        return self._call_wx_method(method=method, args=args)

    def mock_wx_method(
        self,
        method,
        functionDeclaration: str = None,
        result=None,
        args=None,
        success=True,
    ):
        """
        mock wx method and return result
        :param self:
        :param method:
        :param functionDeclaration:
        :param result:
        :param args:
        :param success:
        :return:
        """
        self._mock_wx_method(
            method=method,
            functionDeclaration=functionDeclaration,
            result=result,
            args=args,
            success=success,
        )

    def restore_wx_method(self, method):
        """
        恢复被 mock 的方法
        :param method:
        :return:
        """
        self.connection.send("App.mockWxMethod", {"method": method})

    def hook_wx_method(self, method, before=None, after=None):
        """
        hook wx 方法
        :param method: 需要 hook 的方法
        :param before: 在需要 hook 的方法之前调用
        :param after: 在需要 hook 的方法之后调用
        :return:
        """

        def super_before(msg):
            self.logger.debug(f"{method} before hook result: {msg['args']}")
            if before:
                before(msg["args"])

        if before and not callable(before):
            self.logger.error(f"wx.{method} hook before method is non-callable")
            return
        self._expose_function(method + "_" + super_before.__name__, super_before)

        def super_after(msg):
            self.logger.debug(f"wx.{method} after hook result: {msg['args']}")
            if after:
                after(msg["args"])

        if after and not callable(after):
            self.logger.error(f"{method} hook after method is non-callable")
            return
        self._expose_function(method + "_" + super_after.__name__, super_after)

        self.evaluate(
            """function () {
    var origin = wx.%s;
    if(!wx.%s){
        Object.defineProperty(wx, "%s", {
            get() {
                return function (...args) {
                    return origin(...args);
                }
            }
        })
    }
    Object.defineProperty(wx, "%s", {
        get() {
            return function (...args) {
                %s(...args);
                var res = origin(...args);
                %s(res);
                return res
            }
        }
    })
    }"""
            % (
                method,
                method + "_MiniumOrigin",
                method + "_MiniumOrigin",
                method,
                method + "_" + super_before.__name__,
                method + "_" + super_after.__name__,
            )
        )

    def release_hook_wx_method(self, method):
        """
        释放 hook wx 方法
        :param method: 需要释放 hook 的方法
        :return:
        """
        self.evaluate(
            """function () {
    var origin = wx.%s;
    if(origin){
        Object.defineProperty(wx, "%s", {
            get() {
                return function (...args) {
                    return origin(...args);
                }
            }
        })
    }
    }"""
            % (
                method + '_MiniumOrigin',
                method,
            )
        )

    def evaluate(self, app_function: str, args=None, sync=False):
        """
        向 app Service 层注入代码并执行
        :param app_function:
        :param args:
        :param sync:
        :return:
        """
        return self._evaluate(app_function=app_function, args=args, sync=sync)

    # private method

    def _call_wx_method(self, method, args=None):
        if args is None:
            args = []
        if not isinstance(args, list):
            if isinstance(args, str):
                # 如果是字符型参数，就可以不用管是否是 sync 方法，直接转数组传参即可
                args = [args]
            elif "Sync" in method:
                # 如果是 sync 方法，则需要从字典里面提取所有的 value 成为一个数组进行传参
                if isinstance(args, dict):
                    temp_args = list()
                    for key in args.keys():
                        temp_args.append(args[key])
                    args = temp_args
            else:
                # 异步方法的话无需管 args 是str 还是 dict，直接转成 list 即可
                args = [args]

        params = {"method": method, "args": args}
        return self.connection.send("App.callWxMethod", params)

    def _evaluate(self, app_function: str, args=None, sync=False):
        if not args:
            args = []
        if sync:
            return self.connection.send(
                "App.callFunction", {"functionDeclaration": app_function, "args": args}
            )
        else:
            return self.connection.send_async(
                "App.callFunction", {"functionDeclaration": app_function, "args": args}
            )

    def _expose_function(self, name, binding_function):
        self.connection.register(name, binding_function)
        self.connection.send("App.addBinding", {"name": name})

    def _mock_wx_method(
        self, method, functionDeclaration: str, result=None, args=None, success=True
    ):
        if not args:
            args = []
        else:
            args = [args]
        callback_type = "ok" if success else "fail"
        if functionDeclaration:
            self.connection.send(
                "App.mockWxMethod",
                {
                    "method": method,
                    "functionDeclaration": functionDeclaration,
                    "args": args,
                },
            )
        else:
            if isinstance(result, str):
                self.connection.send(
                    "App.mockWxMethod",
                    {
                        "method": method,
                        "result": {
                            "result": result,
                            "errMsg": "%s:%s" % (method, callback_type),
                        },
                    },
                )
            elif isinstance(result, dict):
                self.connection.send(
                    "App.mockWxMethod", {"method": method, "result": result}
                )
            else:
                self.logger.warning("mock wx method accept str or dict result only")
