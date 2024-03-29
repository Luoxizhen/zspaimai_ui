#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       connection_new.py
Create time:    2019/6/14 16:29
Description:

"""
import time
import websocket
import json
from .minium_object import MiniumObject
from minium.framework.exception import *
from uuid import uuid4
import threading
import logging

CLOSE_TIMEOUT = 5
MAX_WAIT_TIMEOUT = 30
g_thread = None
logger = logging.getLogger()


class DevToolMessage(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise MiniNotAttributeError(name)


def json2obj(data):
    return json.loads(data, object_hook=DevToolMessage)


class Connection(MiniumObject):
    def __init__(self, uri, timeout=MAX_WAIT_TIMEOUT):
        super().__init__()
        self.observers = {}
        self.uri = uri
        self.timeout = timeout
        self._is_connected = False
        self._msg_lock = threading.Condition()
        self._ws_event_queue = dict()
        self._req_id_counter = int(time.time() * 1000) % 10000000000
        self._is_connected = False
        self._sync_wait_msg_id = None
        self._sync_wait_msg = None
        self._sync_wait_msg_map = {}
        self._method_wait = None
        self._client = websocket.WebSocketApp(
            self.uri,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._connect()

    def register(self, method: str, callback):
        if method not in self.observers:
            self.observers[method] = []
        self.observers[method].append(callback)

    def remove(self, method: str):
        if method in self.observers.keys():
            del self.observers[method]
        else:
            self.logger.warning("remove key which is not in observers")

    def remove_all_observers(self):
        try:
            obs_list = [x for x in self.observers.keys()]
            for obs in obs_list:
                del self.observers[obs]
        except Exception as e:
            raise KeyError(e)

    def notify(self, method: str, message):
        if method == "App.bindingCalled" and message["name"] in self.observers:
            for callback in self.observers[message["name"]]:
                if callable(callback):
                    callback(message)
                else:
                    raise MiniNoncallableError(f"{str(callback)}(message={message})")
            return
        elif method in self.observers:
            for callback in self.observers[method]:
                if callable(callback):
                    callback(message)
                else:
                    raise MiniNoncallableError(f"{str(callback)}(message={message})")
        else:
            return

    def _connect(self, timeout=30):

        self._thread = threading.Thread(target=self._ws_run_forever, args=())
        self._thread.daemon = True
        self._thread.start()

        s = time.time()
        while time.time() - s < timeout:
            if self._is_connected:
                logger.info("connect to WebChatTools successfully")
                break
        else:
            raise MiniTimeoutError(
                "connect to server timeout: %s, thread:%s"
                % (self.uri, self._thread.is_alive())
            )

    def _ws_run_forever(self):
        try:
            self._client.run_forever()
        except Exception as e:
            self.logger.exception(e)
            return
        self.logger.info("websocket run forever shutdown")

    def _send(self, message):
        return self._client.send(message)

    def send(self, method, params=None, max_timeout=None):
        if not params:
            params = {}
        if not max_timeout:
            max_timeout = self.timeout
        uid = uuid4()
        message = json.dumps(
            {"id": str(uid), "method": method, "params": params}, separators=(",", ":")
        )
        self._sync_wait_msg_id = str(uid)
        self.logger.debug("SEND > %s" % message)
        self._send(message)
        return self._receive_response(max_timeout)

    def send_async(self, method, params=None):
        if not params:
            params = {}
        uid = uuid4()
        message = json.dumps({"id": str(uid), "method": method, "params": params})
        self._client.send(message)
        self.logger.debug("ASYNC_SEND > %s" % message)
        return uid

    def _receive_response(self, max_timeout=None):
        if max_timeout is None:
            max_timeout = self.timeout
        self._msg_lock.acquire()
        self._msg_lock.wait(max_timeout)
        self._msg_lock.release()

        if self._sync_wait_msg_id is None:  # 获取到了数据
            if (
                "error" in self._sync_wait_msg
                and "message" in self._sync_wait_msg["error"]
            ):
                err_msg = self._sync_wait_msg["error"]["message"]
                if err_msg:
                    raise MiniAppError(err_msg)
            return self._sync_wait_msg
        else:
            record_id = self._sync_wait_msg_id
            self._sync_wait_msg_id = None
            self._sync_wait_msg = None
            raise MiniTimeoutError("receive from remote timeout, id: %s" % record_id)

    def _on_close(self, *args):
        self._is_connected = False

    def _on_open(self, *args):
        self._is_connected = True

    def _on_message(self, message, *args):
        # 有些ws的库会传ws实例！至今不懂为什么有些会有些不会，先兼容一下
        if args:
            # 会传 ws 实例的情况
            message = args[0]
        if len(message) > 512:
            self.logger.debug("RECV < %s..." % message[:509])
        else:
            self.logger.debug("RECV < %s" % message)
        ret_json = json2obj(message)
        if ret_json is not None and "id" in ret_json:  # response
            req_id = ret_json["id"]
            if req_id == self._sync_wait_msg_id:
                self._sync_wait_msg_id = None
                self._sync_wait_msg = ret_json
                self._msg_lock.acquire()
                self._msg_lock.notify()
                self._msg_lock.release()
            else:
                self.logger.warning("received async msg: %s", req_id)
                self._sync_wait_msg_map[req_id] = ret_json
        else:  # event from server
            if "method" in ret_json and self._method_wait == ret_json["method"]:
                self._method_wait = None
                self._msg_lock.acquire()
                self._msg_lock.notify()
                self._msg_lock.release()

            if "method" in ret_json and "params" in ret_json:
                # self._push_event(ret_json["method"], ret_json["params"])
                self.notify(ret_json["method"], ret_json["params"])

    def _push_event(self, method, params):
        if method in self._ws_event_queue:
            self._ws_event_queue[method].append(params)
        else:
            self._ws_event_queue[method] = [params]

    def _on_error(self, error, *args):
        if args:
            # 会传 ws 实例的情况
            error = args[0]
        if "Connection is already closed" in str(error):
            self.logger.warning(error)
            return
        self.logger.error(error)

    def destroy(self):
        logger.error("断开连接")
        self._client.close()
        self._thread.join(CLOSE_TIMEOUT)

    def wait_for(self, method: str, max_timeout=None):
        self._method_wait = method
        if max_timeout is None:
            max_timeout = self.timeout
        self._msg_lock.acquire()
        self._msg_lock.wait(max_timeout)
        self._msg_lock.release()

        if not self._method_wait:
            return True
        else:
            self.logger.error("Can't wait until %s" % method)
            return False

    def get_aysnc_msg_return(self, msg_id=None):
        if not msg_id:
            self.logger.warning(
                "Can't get msg without msg_id, you can get msg_id when calling send_async()"
            )

        ret = self._sync_wait_msg_map.get(msg_id)
        return ret
