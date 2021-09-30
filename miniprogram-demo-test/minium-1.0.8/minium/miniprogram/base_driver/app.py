#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 小程序层面的操作(包含 web 和 Native)
@Date: 2019-03-11 14:41:43
@LastEditTime: 2019-06-05 16:30:44
"""
from .page import Page
from .minium_object import MiniumObject
from minium.framework.exception import *
import os
import threading
import base64
import io
import time

cur_path = os.path.dirname(os.path.realpath(__file__))  # source_path是存放资源文件的路径
conf_path = os.path.join(os.path.dirname(cur_path), "conf/iOS_conf")


class App(MiniumObject):
    def __init__(self, connection, relaunch=False):
        """
        创建一个 APP 实例
        :param connection:
        """
        super().__init__()
        self.connection = connection
        self._msg_lock = threading.Condition()
        self.route_is_changed = False
        self.main_page_path = None
        # self.current_path_path = self.main_page_path
        # self.current_page_id = None  # self._current_page().page_id
        self.route_return_page = None
        # self._create_context_listener()
        self._route_change_listener()
        self.evaluate("function () {global.minium = {};}", sync=True)
        self.current_video_id = None
        self.video_this = None
        self.current_audio_id = None
        self.audio_this = None
        self.current_live_player_id = None
        self.live_player_this = None
        if relaunch:
            self.go_home()

    @property
    def app_id(self):
        return self._get_account_info_sync().result.result.miniProgram.appId

    @property
    def current_page(self):
        ret = self.connection.send("App.getCurrentPage")
        if hasattr(ret, "error"):
            raise Exception("Get current page fail, cause: %s" % ret.error)

        # bug here is :https://git.code.oa.com/devtools/automator/issues/3
        page = Page(
            ret.result.pageId, "/" + ret.result.path, ret.result.query, self.connection
        )
        # self.current_path_path = page.path
        # self.current_page_id = page.page_id
        return page

    def enable_log(self):
        """
        打开日志
        """
        self.connection.send("App.enableLog")

    def exit(self):
        """
        退出小程序
        :return: None
        """
        self.connection.send("App.exit")

    def get_account_info_sync(self):
        """
        获取账号信息
        :return:
        """
        return self._get_account_info_sync()

    def screen_shot(self, save_path=None, format="raw"):
        """
        截图，仅能截取 webview 部分，原生控件不能截取到
        :param save_path:
        :param format: raw or pillow
        :return:
        """
        try:
            b64_data = (
                self.connection.send("App.captureScreenshot").get("result").get("data")
            )
        except MiniAppError as e:
            self.logger.error(e)
            return None
        else:
            raw_value = base64.b64decode(b64_data)
            png_header = b"\x89PNG\r\n\x1a\n"
            if not raw_value.startswith(png_header) and save_path:
                self.logger.error("screenshot png format error")

            if save_path:
                with open(save_path, "wb") as f:
                    f.write(raw_value)

            if format == "raw":
                return raw_value
            elif format == "pillow":
                from PIL import Image

                buff = io.BytesIO(raw_value)
                return Image.open(buff)
            else:
                self.logger.warning(f"unknown format:{format} for screenshot")
                return raw_value

    def expose_function(self, name, binding_function):
        """
        在 AppService 全局暴露方法，供小程序侧调用测试脚本中的方法。
        :param name:
        :param binding_function:
        :return:
        """
        self._expose_function(name, binding_function)

    def add_observer(self, event, callback):
        """
        监听小程序的事件
        :param event: 需要监听的事件
        :param callback: 收到事件后的回调函数
        :return:
        """
        if not callable(callback):
            raise Exception("the callback is not a function")

        self.connection.register(event, callback)

    def remove_observer(self, event):
        """
        移除小程序事件监听
        :param event: 监听的事件
        :return:
        """
        self.connection.remove(event)

    def on_exception_thrown(self, func):
        """
        JS 错误回调
        :param func: 回调函数
        :return:
        """
        self.connection.register("App.exceptionThrown", func)

    def get_all_pages_path(self):
        """
        获取所有已配置的页面路径
        :return:
        """
        ret = self.evaluate(
            "function(){return __wxConfig.pages}", sync=True
        ).result.result
        return ret

    def get_current_page(self) -> Page:
        """
        获取当前顶层页面
        :return: Page 对象
        """
        return self.current_page

    def get_page_stack(self):
        """
        获取当前小程序所有的页面
        :return: Page List
        """
        ret = self.connection.send("App.getPageStack")
        page_stack = []
        for page in ret.result.pageStack:
            page_stack.append(Page(page.pageId, page.path, page.query, self.connection))
        return page_stack

    def get_perf_time(self, entry_types: list = None):
        if not entry_types:
            entry_types = ["render", "script", "navigation", "loadPackage"]
        for item_type in entry_types:
            if item_type not in ["render", "script", "navigation", "loadPackage"]:
                raise Exception("the entryType is not available")

        script = """function () {
            global.minium.performanceList = [];
            var performance = wx.getPerformance();
            global.minium.observer = performance.createObserver((list, observer) => {
                console.log('performance event:', list.getEntries());
                global.minium.performanceList = global.minium.performanceList.concat(list.getEntries());
            })
            global.minium.observer.observe({ entryTypes:%s});
            }""" % str(entry_types)
        self.evaluate(script, sync=True)

    def stop_get_perf_time(self):
        time.sleep(2)  # 收集数据的时间推后一点点，怕收集不完全
        script = """function () {
    global.minium.allperfdata = global.minium.performanceList;
    global.minium.observer.disconnect();
    global.minium.performanceList = [];
    return global.minium.allperfdata;
}"""
        ret = (
            self.evaluate(script, sync=True)
            .get("result", {"result": {}})
            .get("result", None)
        )
        return ret

    def go_home(self, main_page_path=None):
        """
        跳转到首页
        :param main_page_path: 路径
        :return: Page 对象
        """
        if not main_page_path:
            if self.main_page_path:
                main_page_path = self.main_page_path
            else:
                main_page_path = "/" + self._get_launch_options_sync().result.result.path
                if main_page_path == "/":
                    raise MiniLaunchError("get launch options failed")
                self.main_page_path = main_page_path

        page = self._relaunch(main_page_path)
        return page

    def _get_launch_options_sync(self):
        return self._call_wx_method("getLaunchOptionsSync")

    def _change_route(self, open_type, path, is_wait_url_change=True):
        self._call_wx_method(open_type, [{"url": path}])
        if self._route_changed():
            return self.route_return_page
        else:
            return self.current_page  # todo: 状态有BUG，超时也认为可用的


    def _on_route_changed(self, message):
        if not message.name == "onAppRouteDone":
            return
        self.route_is_changed = True
        # self.current_path_path = message.args[0].path
        # self.current_page_id = message.args[0].webviewId
        self.route_return_page = Page(
            message.args[0].webviewId,
            "/"+message.args[0].path,
            message.args[0].query,
            self.connection,
        )
        self._msg_lock.acquire()
        self._msg_lock.notify()
        self._msg_lock.release()
        self.logger.info("Route changed, %s" % message)

    def _on_video_context_created(self, message):
        if not message.name == "onVideoContextCreated":
            return
        self.logger.info(message)
        self.current_video_id = message.args[0]
        self.video_this = message.args[1]

    def _on_audio_context_created(self, message):
        if not message.name == "onAudioContextCreated":
            return
        self.logger.info(message)
        self.current_audio_id = message.args[0]
        self.audio_this = message.args[1]

    def _on_live_pusher_context_created(self, message):
        if not message.name == "onLivePusherContextCreated":
            return
        self.logger.info(message)

    def _on_live_player_context_created(self, message):
        if not message.name == "onLivePlayerContextCreated":
            return
        self.logger.info(message)
        self.current_live_player_id = message.args[0]
        self.live_player_this = message.args[1]

    def navigate_to(self, url, params=None, is_wait_url_change=True):
        """
        以导航的方式跳转到指定页面, 但是不能跳到 tabbar 页面。支持相对路径和绝对路径, 小程序中页面栈最多十层
        支持相对路径和绝对路径
        /page/tabBar/API/index: 绝对路径,最前面为/
        tabBar/API/index: 相对路径, 会被拼接在当前页面的路径后面
        :param url:"/page/tabBar/API/index"
        :param params: 页面参数
        :param is_wait_url_change: 是否等待页面变换完成
        :return:Page 对象
        """
        if params:
            url += "?" + "&".join(["%s=%s" % (k, v) for k, v in params.items()])
        self.logger.info("NavigateTo: %s" % url)
        page = self._change_route("navigateTo", url, is_wait_url_change)
        if page.path != url.split("?")[0]:
            self.logger.warning(
                "NavigateTo(%s) but(%s)" % (url, page.path)
            )
        return page

    def redirect_to(self, url):
        """
        关闭当前页面，重定向到应用内的某个页面。但是不允许跳转到 tabbar 页面
        :param url:"/page/tabBar/API/index"
        :return:Page 对象
        """
        # wait = False if url == self.current_page else True
        self.logger.info("RedirectTo: %s" % url)
        page = self._change_route("redirectTo", url)
        if page.path != url.split("?")[0]:
            self.logger.warning(
                "RedirectTo(%s) but(%s)" % (url, page.path)
            )
        return page

    def relaunch(self, url):
        """
        关闭所有页面，打开到应用内的某个页面
        :param url: "/page/tabBar/API/index"
        :return:Page 对象
        """
        return self._relaunch(url=url)

    def navigate_back(self, delta=1):
        """
        关闭当前页面，返回上一页面或多级页面。
        :param delta: 返回的层数, 如果超出 page stack 最大层数返回首页
        :return:Page 对象
        """
        # self._wait_until_page_is_stable()
        page = self.current_page
        page_stack = self._page_stack()
        if page.page_id == page_stack[0].page_id:
            self.logger.warning("Current page is root, can't navigate back")
            return page
        self.logger.info("NavigateBack from:%s" % page.path)
        self._call_wx_method("navigateBack", [{"delta": delta}])
        if self._route_changed():
            return self.route_return_page
        else:
            self.logger.warning("route has not change, may be navigate back fail")

    def switch_tab(self, url):
        """
        跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面
        :param url: "/page/tabBar/API/index"
        :return:Page 对象
        """
        page = self._change_route("switchTab", url)
        if page.path != url.split("?")[0]:
            self.logger.warning(
                "Switch tab(%s) but(%s)" % (url, page.path)
            )
        return page

    ###
    # 各类 mock
    ###
    
    def _mock_network(self, interface: str, rule: str or dict, success=None, fail=None):
        if success and fail:
            raise RuntimeError("Can't call back both SUCCESS and FAIL")
        if not (success or fail):
            raise RuntimeError("Must call back either SUCCESS or FAIL")
        if isinstance(rule, (str, bytes)):
            # 默认匹配url
            _rule = { "url": rule }
        else:
            _rule = rule
        if success:
            _rule["success"] = success
        elif fail:
            if isinstance(fail, (str, bytes)):
                fail = {"errMsg": "%s:fail %s" % (interface, fail)}
            _rule["fail"] = fail
        has_mock = self.evaluate("""function (rule){
            if (!global.%(interface)s_MiniumNetworkMock) {
                Object.defineProperty(global, "%(interface)s_MiniumNetworkMock", {
                    value: true,
                    writable: false
                })
                Object.defineProperty(global, "%(interface)s_MiniumMockRule", {
                    value: [],
                    writable: false
                })
                global.%(interface)s_MiniumMockRule.push(rule)
                return false
            }
            global.%(interface)s_MiniumMockRule.push(rule)
            return true
        }""" % { "interface": interface }, [_rule], sync=True).get("result", {}).get("result")
        if not has_mock:
            self.evaluate("""function (){
                function isRuleMatched(rule, req) {
                    if (typeof(rule) !== typeof(req)) return false
                    switch(typeof(rule)) {
                        case "string":
                            var r = new RegExp(rule)
                            if (r.exec(req)) return true
                            return false
                            break
                        case "number":
                            return rule === req
                        case "object":
                            if (rule instanceof Array) {
                                if (rule.length != req.length) return false
                                for (var i=0; i < rule.length; i++) {
                                    if (!isRuleMatched(rule[i], req[i])) return false
                                }
                                return true
                            } else {
                                for (var key in rule) {
                                    if(key == "success" || key == "fail" || key == "complete") continue
                                    if (!req[key]) return false
                                    if (!isRuleMatched(rule[key], req[key])) return false
                                }
                                return true
                            }
                            break
                    }
                    return false
                }
                var origin = wx.%(interface)s
                Object.defineProperty(wx, "%(interface)s", {
                    configurable: true,
                    get() {
                        return function (obj) {
                            for (var i=0; i < global.%(interface)s_MiniumMockRule.length; i++) {
                                if (isRuleMatched(global.%(interface)s_MiniumMockRule[i], obj)) {
                                    if (global.%(interface)s_MiniumMockRule[i].success) {
                                        obj.success && obj.success(global.%(interface)s_MiniumMockRule[i].success)
                                        obj.complete && obj.complete(global.%(interface)s_MiniumMockRule[i].success)
                                        return
                                    } else if (global.%(interface)s_MiniumMockRule[i].fail) {
                                        obj.fail && obj.fail(global.%(interface)s_MiniumMockRule[i].fail)
                                        obj.complete && obj.complete(global.%(interface)s_MiniumMockRule[i].fail)
                                        return
                                    }
                                }
                            }
                            return origin(obj);
                        }
                    }
                })
            }""" % { "interface": interface }, sync=True)
    
    def _restore_network(self, interface: str):
        """
        恢复被mock的网络接口
        """
        self.evaluate("""function (){
            if (global.%(interface)s_MiniumNetworkMock) {
                global.%(interface)s_MiniumMockRule.splice(0, global.%(interface)s_MiniumMockRule.length)
            }
        }""" % { "interface": interface }, sync=True)
    
    def mock_request(self, rule: str or dict, success=None, fail=None):
        """
        mock wx.request, 根据正则mock规则返回mock结果
        """
        return self._mock_network("request", rule, success, fail)
    
    def restore_request(self):
        return self._restore_network("request")

    def mock_show_modal(self, answer=True):
        """
        mock 弹窗
        :param answer: 默认点击确定
        :return: None
        """
        self._mock_wx_method(
            "showModal",
            result={
                "cancel": answer,
                "confirm": False if answer else True,
                "errMsg": "showModal:ok",
            },
        )

    def mock_get_location(
        self,
        acc=65,
        horizontal_acc=65,
        vertical_acc=65,
        speed=-1,
        altitude=0,
        latitude=23.12908,
        longitude=113.26436,
    ):
        """
        mock 位置获取
        :param acc: 位置的精确度
        :param horizontal_acc: 水平精度，单位 m
        :param vertical_acc: 垂直精度，单位 m（Android 无法获取，返回 0）
        :param speed: 速度，单位 m/s
        :param altitude: 高度，单位 m
        :param latitude: 纬度，范围为 -90~90，负数表示南纬
        :param longitude: 经度，范围为 -180~180，负数表示西经
        :return:
        """
        self._mock_wx_method(
            "getLocation",
            result={
                "accuracy": acc,
                "altitude": altitude,
                "errMsg": "getLocation:ok",
                "horizontalAccuracy": horizontal_acc,
                "verticalAccuracy": vertical_acc,
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed,
            },
        )

    def mock_show_action_sheet(self, tap_index=0):
        """
        mock 显示操作菜单
        :param tap_index: 用户点击的按钮序号，从上到下的顺序，从0开始
        :return:
        """
        self._mock_wx_method(
            "showActionSheet",
            result={"errMsg": "showActionSheet:ok", "tapIndex": tap_index},
        )

    def create_audio_context_listener(self):
        """
        添加音频组件 context 监听者
        :return:
        """
        self._expose_function("onAudioContextCreated", self._on_audio_context_created)
        self._evaluate(
            """function () {
    var cac = wx.createAudioContext;
    Object.defineProperty(wx, "createAudioContext", {
        get() {
            return function (audioId, pageOptions) {
                onAudioContextCreated(audioId, pageOptions);
                global.minium.audioContext = null;
                audioContext = cac(audioId, pageOptions);
                global.minium.audioContext = audioContext;
                return audioContext
            }
        }
    });
}"""
        )

    def create_live_pusher_context_listener(self):
        """
        添加直播推流组件 context 监听者
        :return:
        """
        self._expose_function(
            "onLivePusherContextCreated", self._on_live_pusher_context_created
        )
        self._evaluate(
            """function () {
    var clpuc = wx.createLivePusherContext;
    Object.defineProperty(wx, "createLivePusherContext", {
        get() {
            return function () {
                onLivePusherContextCreated();
                global.minium.livePusherContext = null;
                livePusherContext = clpuc();
                global.minium.livePusherContext = livePusherContext;
                return livePusherContext
            }
        }
    });
}"""
        )

    def create_live_player_context_listener(self):
        """
        添加直播播放组件 context 监听者
        :return:
        """
        self._expose_function(
            "onLivePlayerContextCreated", self._on_live_player_context_created
        )
        self._evaluate(
            """function () {
    var clplc = wx.createLivePlayerContext;
    Object.defineProperty(wx, "createLivePlayerContext", {
        get() {
            return function (playerId, pageOptions) {
                onLivePlayerContextCreated(playerId, pageOptions);
                global.minium.livePlayerContext = null;
                livePlayerContext = clplc(playerId, pageOptions);
                global.minium.livePlayerContext = livePlayerContext;
                return livePlayerContext
            }
        }
    });
}"""
        )

    def create_context_listener(self):
        """
        添加媒体组件 context 监听者
        :return:
        """
        # self._expose_function("onVideoContextCreated", self._on_video_context_created)
        self.create_audio_context_listener()
        self.create_live_player_context_listener()
        self.create_live_pusher_context_listener()

    # @timeout(10)
    # def _wait_until_page_is_stable(self):
    #     return True if self.current_page_id == self.current_page.page_id else False
    #
    # @timeout(10)
    # def _wait_until_page_is_change(self):
    #     return True if self.current_page_id != self.current_page.page_id else False

    def _route_changed(self, timeout=None):
        if not timeout:
            timeout = 5

        self._msg_lock.acquire()
        self._msg_lock.wait(timeout)
        self._msg_lock.release()

        if self.route_is_changed:
            time.sleep(3)
            self.route_is_changed = False
            return True
        else:
            self.route_is_changed = False
            return False

    def _route_change_listener(self):
        self._expose_function("onAppRouteDone", self._on_route_changed)
        self._evaluate(
            """function () {
    wx.onAppRouteDone(function (options) {
        onAppRouteDone(options)
    })
}"""
        )

    def _get_account_info_sync(self):
        return self._call_wx_method("getAccountInfoSync")

    def _relaunch(self, url):
        self.logger.info("ReLaunch: %s" % url)
        page = self._change_route("reLaunch", url)
        if page.path != url.split("?")[0]:
            self.logger.warning("ReLaunch(%s) but(%s)" % (url, page.path))
        # time.sleep(1)
        return page

    def _page_stack(self):
        ret = self.connection.send("App.getPageStack")
        page_stack = []
        for page in ret.result.pageStack:
            page_stack.append(Page(page.pageId, page.path, page.query, self.connection))
        return page_stack

    def _stop_audits(self):
        ret = self.connection.send("Tool.stopAudits")
        return ret

    def edit_editor_text(self, editorid, text):
        script = '''function(){
                    global.minium.edRes = ""
                    wx.createSelectorQuery().select("#%s").context(function (res) {
                    console.log("context",res.context)
                    res.context.insertText({
        text: "%s",
        success(res){
          global.minium.edRes = res.errMsg
        },
        fail(res){
          global.minium.edRes = res.errMsg
        }
      })
    }).exec() }''' % (editorid, text)
        ret = self.evaluate(script, sync=True)
        self.logger.info(ret)
        time.sleep(1) #得等下异步的结果过来
        script2 = """function () {
            console.log("global.minium.edRes",global.minium.edRes)
            return global.minium.edRes;
        }"""
        ret2 = (
            self.evaluate(script2, sync=True)
                .get("result", {"result": {}})
                .get("result", None)
        )
        self.logger.info(ret2)
        return ret2