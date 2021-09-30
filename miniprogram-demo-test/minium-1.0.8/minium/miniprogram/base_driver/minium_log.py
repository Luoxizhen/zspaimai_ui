#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       minium_log.py
Create time:    2019-08-29 11:12
Description:

"""

from functools import wraps
import datetime
import types
import json
import requests
import queue
import threading
import logging
import os

logging.getLogger("urllib3").setLevel(logging.WARNING)
# logger = logging.getLogger("DataReport")


def build_version():
    config_path = os.path.join(os.path.dirname(__file__), "version.json")
    if not os.path.exists(config_path):
        return {}
    else:
        with open(config_path, "rb") as f:
            version = json.load(f)
            return version


def process_report():
    global existFlag
    while not existFlag:
        lock.acquire()
        lock.wait(10)
        lock.release()
        if not report_queue.empty():
            data = report_queue.get()
            # logger.debug("Thread processing report data %s" % data)
            report(data=data)


def report_exception(data: dict):
    try:
        # proxies = {'http': 'http://127.0.0.1:12639', 'https': ''}
        data["Uin"] = 0
        data["version"] = ""
        data["ext"] = ""
        docs = [data]
        print("minumexception: %s"%str(data))
        rp_data = {"logid": "minumexception", "docs": docs}
        url = "http://ilogs2.oa.com/ilogs_backend/post_data"
        r = requests.post(
            url=url,
            data=json.dumps(rp_data),
            timeout=5,
            headers={"Content-Type": "application/json"}
            # ,proxies = proxies
        )
        print(r.text)
    except Exception as e:
        pass


def report(data: dict):
    try:
        ret = requests.post(
            url="https://minitest.weixin.qq.com/xbeacon/user_report/api_log",
            data=json.dumps(data),
            timeout=10,
        )
        # logger.debug(ret.text)
        if not ret.status_code == 200:
            global fail, existFlag
            fail += 1
            if fail >= 10:
                existFlag = 1
        else:
            fail = 0
    except Exception as e:
        # logger.debug("data report fail with https")
        try:
            ret = requests.post(
                url="http://minitest.weixin.qq.com/xbeacon/user_report/api_log",
                data=json.dumps(data),
                timeout=10,
            )
            # logger.debug(ret.text)
            if not ret.status_code == 200:
                fail += 1
                if fail >= 10:
                    existFlag = 1
            else:
                fail = 0
        except Exception as e:
            # logger.error("data report fail with http, give up")
            # logger.exception(e)
            pass


# logger.debug(ret.text)


existFlag = 0
fail = 0

lock = threading.Condition()
report_queue = queue.Queue()
thread = threading.Thread(target=process_report)
thread.setDaemon(True)
thread.start()

usage = []
app_id = None
version = build_version().get("version")
revision = build_version().get("revision")


def minium_log(func):
    """
    函数统计装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        global usage, app_id, version, revision

        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()

        new_args = [args[0].__dict__] + list(args[1:])

        if (version is None or revision is None) and hasattr(args[0], "version"):
            version = args[0].version.get("version")
            revision = args[0].version.get("revision")

        if app_id is None and hasattr(args[0], "app_id"):
            app_id = args[0].app_id

        if app_id is None:
            usage.append(
                {
                    "version": version,
                    "revision": revision,
                    "app_id": app_id,
                    "func": func.__name__,
                    "args": str(new_args),
                    "kwargs": kwargs,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "consuming": int((end - start).total_seconds() * 1000),
                }
            )
        else:
            report_queue.put(
                {
                    "version": version,
                    "revision": revision,
                    "app_id": app_id,
                    "func": func.__name__,
                    "args": str(new_args),
                    "kwargs": kwargs,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "consuming": int((end - start).total_seconds() * 1000),
                }
            )
            for f in usage:
                f["app_id"] = app_id
                report_queue.put(f)
            lock.acquire()
            lock.notify()
            lock.release()
        return result

    return wrapper


class MonitorMetaClass(type):
    """
    类监控元类
    """

    def __new__(mcs, cls_name, bases, attr_dict):
        for k, v in attr_dict.items():
            if (
                isinstance(v, types.FunctionType)
                and not k.startswith("_")
                and not k.startswith("send")
                and not k.startswith("register")
                and not k.startswith("notify")
                and not k.startswith("remove")
            ):
                attr_dict[k] = minium_log(v)
        return type.__new__(mcs, cls_name, bases, attr_dict)


def singleton(cls):
    """
    单例装饰器
    :param cls:
    :return:
    """
    _instance = {}

    @wraps(cls)
    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return inner
