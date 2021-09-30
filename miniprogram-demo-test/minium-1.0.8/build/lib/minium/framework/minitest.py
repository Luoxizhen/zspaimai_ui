#!/usr/bin/env python3
# Created by xiazeng on 2019-05-06
import datetime
import json
import os.path
import shutil
import time

import minium
import minium.miniprogram.base_driver.minium_log
import minium.native
from .assertbase import AssertBase
from .log_color import *
from .exception import *

# import matplotlib.pyplot as plt

logger = logging.getLogger()

g_minium = None
g_native = None
g_log_message_list = []
g_network_message_dict = {}


def full_reset():
    """
    在整个测试流程结束之后调用
    1. miniProgram 部分同 reset_minium()
    2. native 部分
        1.1 关闭微信
        1.2 释放原生 driver
    :return:
    """
    global g_minium, g_native
    if g_minium:
        reset_minium()
    if g_native:
        g_native.stop_wechat()
        g_native.release()
        g_native = None


def reset_minium():
    """
    1. miniProgram 部分 release
        1.1 非 ide 运行退出小程序
    2. 释放所有观察者的事件监听
    3. 销毁与 ide 的连接
    :return:
    """
    global g_minium
    g_minium.shutdown()
    g_minium.connection.remove_all_observers()
    g_minium.connection.destroy()
    g_minium = None


def get_native(cfg):
    """
    native 部分完全由配置中的 platform 参数控制
    为了确保不会过多地重启微信，已存在 g_native 则不创建,
    teardown 的时候也不会 release
    :param cfg: 配置
    :return:
    """
    global g_native
    if g_native is None:
        g_native = minium.native.get_native_driver(cfg.platform, cfg)
        g_native.start_wechat()
    return g_native


def get_minium(cfg):
    """
    miniProgram 部分每次 classTearDown 是否 release 由配置 close_ide 控制
    初始化有如下工作：
        1. 处理配置
        2. 如果配置了 project_path 则启动 ide
        3. 连接 ide
        4. 根据配置 platform 判断是否需要远程调试
        5. 根据配置 enable_app_log 判断是否需要监听小程序 log 输出
        6. 根据配置 enable_network_panel 判断是否需要监听小程序 request, downloadFile, uploadFile 输出
    :param cfg: 配置
    :return:
    """
    global g_minium, g_native
    if g_minium is None:
        g_minium = minium.miniprogram.get_minium_driver(conf=cfg)

        if not cfg.use_push and cfg.platform != "ide":
            g_native.connect_weapp(g_minium.qr_code)
            ret = g_minium.connection.wait_for(method="App.initialized")
            if ret is False:
                raise MiniAppError("Launch MiniProgram Fail")

        if cfg.enable_app_log:
            g_minium.connection.register("App.logAdded", mini_log_added)
            g_minium.app.enable_log()

        if cfg.enable_network_panel:
            # 没有uuid库，随便注入一个随机ID库
            g_minium.app.evaluate("""function() {
                if (!global.get_mini_network_id) global.get_mini_network_id = function (){for(var a=[],
                b=0;36>b;b++)a[b]="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".substr(Math.floor(16*Math.random()),
                1);a[14]="4";a[19]="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".substr(a[19]&3|8,1);a[8]=a[13]=a[18]=a[
                23]="-";return a.join("")};
            }""", sync=True)
            g_minium.app.expose_function("mini_request_callback", request_callback)
            g_minium.app.expose_function("mini_send_request", send_request)
            g_minium.app.evaluate("""function() {
                var origin = wx.request;
                if (!global.request_MiniumNetworkHook) {
                    Object.defineProperty(global, "request_MiniumNetworkHook", {
                        value: true,
                        writable: false
                    })
                    Object.defineProperty(wx, "request", {
                        configurable: true,
                        get() {
                            return function (obj) {
                                if (!global || !global.get_mini_network_id) return origin(obj);
                                if (obj.url == "https://weapp.tencent.com/jscov_driver/CollectCovTimer") return origin(obj);
                                var nid = global.get_mini_network_id();
                                var request_obj = Object.assign({}, obj);
                                delete request_obj.success;
                                delete request_obj.fail;
                                delete request_obj.complete;
                                var complete = obj.complete;
                                obj.complete = (res) => {
                                    mini_request_callback(nid, res, Date.now())
                                    complete && complete(res);
                                }
                                mini_send_request(nid, request_obj, Date.now());
                                return origin(obj);
                            }
                        }
                    })
                }
            }""", sync=True)

        if isinstance(cfg.mock_native_modal, dict) and cfg.platform == "ide":  # IDE上不支持原生接口, 用特殊方法mock
            g_native.mini = g_minium
            # mini_auth_setting: 记录MOCK过的授权窗，如果确认过授权，后面不需要再通过handle来点击;
            # mock_native_modal_list: 回调栈;
            # handle_mock_native_modal: 弹窗操作;
            # handle_mock_map_modal: 地图操作;
            # mock_native_modal: 添加回调栈;
            # mock_map_modal: 添加地图操作回调栈
            has_mock_native_modal = g_minium.app.evaluate("""function() {
                if (!global.mock_native_modal) {
                    global.mini_auth_setting = {}
                    global.mock_native_modal_list = []
                    global.handle_mock_modal = function(btn_text, type) {
                        let tmp = []
                        while (global.mock_native_modal_list.length > 0) {
                            let item = global.mock_native_modal_list.pop()
                            if (item.type !== type) {
                                tmp.unshift(item)
                                continue
                            }
                            let callback = item[btn_text]
                            global.mock_native_modal_list.push(...tmp)
                            if (!callback) {
                                throw `${btn_text} not in callback item ${Object.keys(item)}`
                            }
                            if (typeof callback !== "function") {
                                throw `${callback} is not callable`
                            }
                            return callback()
                        }
                        global.mock_native_modal_list.push(...tmp)
                    }
                    global.handle_mock_native_modal = function(btn_text) {
                        return global.handle_mock_modal(btn_text, "modal")
                    }
                    global.handle_mock_map_modal = function(btn_text) {
                        return global.handle_mock_modal(btn_text, "map")
                    }
                    global.mock_native_modal = function(obj) {
                        obj.type = "modal"
                        global.mock_native_modal_list.push(obj)
                    }
                    global.mock_map_modal = function(obj) {
                        obj.type = "map"
                        global.mock_native_modal_list.push(obj)
                    }
                    return false;
                }
                return true
            }""", sync=True).get("result", {}).get("result")
            if not has_mock_native_modal:
                # wx.showModal
                g_minium.app.mock_wx_method("showModal", """function(obj) {
                    let confirmText = obj.confirmText || '确定'
                    let cancelText = obj.cancelText || '取消'
                    return new Promise(resolve => {
                        let args = {}
                        args[confirmText] = function(){
                            let cb_args = {
                                "errMsg": "showModal:ok",
                                "confirm": true,
                                "cancel": false
                            }
                            resolve(cb_args)
                            return cb_args
                        }
                        args[cancelText] = function(){
                            let cb_args = {
                                "errMsg": "showModal:ok",
                                "confirm": false,
                                "cancel": true
                            }
                            resolve(cb_args)
                            return cb_args
                        }
                        return global.mock_native_modal(args)
                    })
                }""")
                # wx.showActionSheet
                g_minium.app.mock_wx_method("showActionSheet", """function(obj) {
                    return new Promise( (resolve, reject) => {
                        let args = {}
                        let itemList = obj.itemList
                        for(let i=0; i<itemList.length; i++) {
                            args[itemList[i]] = function() {
                                let cb_args = {
                                    "errMsg": "showActionSheet:ok",
                                    "tapIndex": i
                                }
                                resolve(cb_args)
                                return cb_args
                            }
                        }
                        args["取消"] = function() {
                            let cb_args = {
                                "errMsg": "showActionSheet:fail cancel"
                            }
                            reject(cb_args)
                            return cb_args
                        }
                        return global.mock_native_modal(args)
                    } )
                }""")
                # 授权相关接口需要先获取SETTING
                mini_setting = g_minium.app.call_wx_method("getSetting").get("result", {}).get("result")
                # 获取到原始setting，mock这个接口
                g_minium.app.mock_wx_method("getSetting", """function(obj) {
                  return new Promise(resolve => {
                    this.origin({
                      success(res) {
                        Object.assign(res.authSetting, global.mini_auth_setting)
                        resolve(res)
                      },
                    })
                  })
                }""")
                g_minium.app.mock_wx_method("authorize", """function(obj) {
                    let scope = obj.scope
                    let origin = this.origin
                    return new Promise((resolve, reject) => {
                        wx.getSetting({
                            success(res) {
                                if (res.authSetting[scope] === true) {
                                    resolve({"errMsg": "authorize:ok"})
                                } else if (res.authSetting[scope] === true) {
                                    reject({errMsg: "authorize:fail auth deny"})
                                } else {
                                    let args = {}
                                    args["允许"] = function() {
                                        global.mini_auth_setting[scope] = true
                                        resolve({"errMsg": "authorize:ok"})
                                    }
                                    args["不允许"] = function() {
                                        global.mini_auth_setting[scope] = false
                                        reject({errMsg: "authorize:fail auth deny"})
                                    }
                                    global.mock_native_modal(args)
                                }
                            } 
                        })
                    })
                }""")
                # wx.getLocation，先看看是否有`scope.userLocation`权限，如果已有，则不需要MOCK
                if mini_setting["authSetting"].get("scope.userLocation") is None:  # 没有授权，mock掉使之不弹窗
                    g_minium.app.mock_wx_method("getLocation", """function(obj) {
                        return new Promise( (resolve, reject) => {
                            let res
                            if (obj.type === "gcj02") res = {"speed":-1,"steps":0,"errMsg":"getLocation:ok",
                            "provider":"gps","buildingId":"","longitude":113.32489013671875,
                            "latitude":23.099933624267578,"verticalAccuracy":10,"floorName":"1000","accuracy":65,
                            "direction":-1,"horizontalAccuracy":65}
                            else res = {"speed":-1,"steps":0,"errMsg":"getLocation:ok","provider":"gps",
                            "buildingId":"","longitude":113.31950378417969,"latitude":23.102487564086914,
                            "verticalAccuracy":10,"floorName":"1000","accuracy":65,"direction":-1,
                            "horizontalAccuracy":65}
                            if (obj.altitude) res.altitude = 23.102540969848633
                            let mock_data = %s
                            for (let key in res) {
                                if (mock_data[key] !== undefined) res[key] = mock_data[key]
                            }
                            let err = {"errMsg":"getLocation:fail auth deny"}
                            function success() {
                                resolve(res)
                                return res
                            }
                            function fail() {
                                reject(err)
                                return err
                            }
                            if (global.mini_auth_setting["scope.userLocation"] === true) {
                                return success()
                            } else if (global.mini_auth_setting["scope.userLocation"] === false) {
                                return fail()
                            }
                            let args = {}
                            args["确定"] = function() {
                                global.mini_auth_setting["scope.userLocation"] = true
                                return success()
                            }
                            args["取消"] = function() {
                                global.mini_auth_setting["scope.userLocation"] = false
                                return fail()
                            }
                            return global.mock_native_modal(args)
                        } )
                    }""" % (json.dumps(cfg.mock_native_modal.get("location", {}))))
                    g_minium.app.mock_wx_method("chooseLocation", """function(obj) {
                        return new Promise( (resolve, reject) => {
                            let res = {"errMsg":"chooseLocation:ok","name":"腾讯微信总部","address":"广东省广州市",
                            "latitude":23.12463,"longitude":113.36199}
                            let cancel = {"errMsg":"chooseLocation:fail cancel"}
                            let err = {"errMsg":"chooseLocation:fail auth deny"}
                            let mock_data = %s
                            for (let key in res) {
                                if (mock_data[key] !== undefined) res[key] = mock_data[key]
                            }
                            function success() {
                                let map_args = {}
                                map_args["确定"] = function() {
                                    resolve(res)
                                    return res
                                }
                                map_args["取消"] = function() {
                                    reject(cancel)
                                    return cancel
                                }
                                global.mock_map_modal(map_args)
                            }
                            function fail() {
                                reject(err)
                                return err
                            }
                            if (global.mini_auth_setting["scope.userLocation"] === true) {
                                return success()
                            } else if (global.mini_auth_setting["scope.userLocation"] === false) {
                                return fail()
                            }
                            let args = {}
                            args["确定"] = function() {
                                global.mini_auth_setting["scope.userLocation"] = true
                                return success()
                            }
                            args["取消"] = function() {
                                global.mini_auth_setting["scope.userLocation"] = false
                                return fail()
                            }
                            return global.mock_native_modal(args)
                        } )
                    }""" % (json.dumps(cfg.mock_native_modal.get("location", {}))))
                if mini_setting["authSetting"].get(
                        "scope.werun") is None:  # 没有授权，mock掉使之不弹窗, 返回的参数由于有加密信息，直接mock数据会导致后面后台解密过不去，需要添加配置来输入MOCK数据
                    g_minium.app.mock_wx_method("getWeRunData", """function(obj) {
                        return new Promise( (resolve, reject) => {
                            let res = {"errMsg":"getWeRunData:ok","encryptedData":"%s","iv":"%s"}
                            let err = {"errMsg":"getWeRunData:fail auth deny"}
                            function success() {
                                resolve(res)
                                return res
                            }
                            function fail() {
                                reject(err)
                                return err
                            }
                            if (global.mini_auth_setting["scope.werun"] === true) {
                                return success()
                            } else if (global.mini_auth_setting["scope.werun"] === false) {
                                return fail()
                            }
                            let args = {}
                            args["确定"] = function() {
                                global.mini_auth_setting["scope.werun"] = true
                                return success()
                            }
                            args["拒绝"] = function() {
                                global.mini_auth_setting["scope.werun"] = false
                                return fail()
                            }
                            return global.mock_native_modal(args)
                        } )
                    }""" % (cfg.mock_native_modal.get("weRunData", {}).get("encryptedData", "testencryptedData"),
                            cfg.mock_native_modal.get("weRunData", {}).get("iv", "testiv")))
                # getUserProfile在2.10.4后才支持
                try:
                    g_minium.app.mock_wx_method("getUserProfile", """function(obj) {
                        return new Promise( (resolve, reject) => {
                            let res = {"errMsg":"getUserProfile:ok","userInfo": %s}
                            let err = {"errMsg":"getUserProfile:fail auth deny"}
                            function success() {
                                resolve(res)
                                return res
                            }
                            function fail() {
                                reject(err)
                                return err
                            }
                            let args = {}
                            args["允许"] = function() {
                                return success()
                            }
                            args["拒绝"] = function() {
                                return fail()
                            }
                            return global.mock_native_modal(args)
                        } )
                    }""" % (json.dumps(cfg.mock_native_modal.get("userInfo", {}))))
                except MiniAppError as e:
                    logger.error("wx.getUserProfile not exists, please ensure sdk version")

        if cfg.mock_request and isinstance(cfg.mock_request, (list, tuple)):
            for item in cfg.mock_request:
                try:
                    g_minium.app.mock_request(**item)
                except Exception as e:
                    logger.exception("mock_request config error, configure item is %s, error is %s" % (str(item), str(e)))
            
    return g_minium


def mini_log_added(message):
    """
    小程序 log 监听回调函数
    将小程序的 log 格式化然后保存起来
    :param message:
    :return:
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message["dt"] = dt
    g_log_message_list.append(message)


def send_request(message):
    [msg_id, obj, ms] = message["args"]
    if msg_id not in g_network_message_dict:
        g_network_message_dict[msg_id] = {"timestamp": time.time() * 1000}
    g_network_message_dict[msg_id]["start_timestamp"] = ms
    g_network_message_dict[msg_id]["request"] = obj


def request_callback(message):
    [msg_id, res, ms] = message["args"]
    if msg_id not in g_network_message_dict:
        g_network_message_dict[msg_id] = {"timestamp": time.time()}
    g_network_message_dict[msg_id]["end_timestamp"] = ms
    g_network_message_dict[msg_id]["response"] = res


class MiniTest(AssertBase):
    mini = None
    app = None
    native = None
    appId = ""
    appName = ""

    @classmethod
    def _miniClassSetUp(cls):
        logger.debug("=====================")
        logger.debug("Testing class：%s" % cls.__name__)
        logger.debug("=====================")
        super(MiniTest, cls)._miniClassSetUp()
        if not cls.CONFIG.report_usage:
            minium.miniprogram.base_driver.minium_log.existFlag = 1

        cls.native = get_native(cls.CONFIG)
        if cls.CONFIG.only_native:
            logger.info(f"Only native: {cls.CONFIG.only_native}, setUpClass complete")
            return
        else:
            cls.mini = get_minium(cls.CONFIG)
            cls.app = cls.mini.app
            cls.DEVICE_INFO["system_info"] = cls.mini.get_system_info()
            conf = cls.mini.get_app_config()
            account_info = conf.get("accountInfo", {})
            if account_info:
                cls.appId = account_info.get("appId", "")
                cls.appName = account_info.get("appName", "") or account_info.get("nickname", "")  # 发现appname改成了nickname

    @classmethod
    def tearDownClass(cls):
        """
        1. 存在 g_minium
        2. 配置 close_ide=True
        3. ide 下不释放
        :return:
        """
        if cls.CONFIG.full_reset:
            logger.info("full reset")
            full_reset()
            return
        if g_minium and cls.CONFIG.close_ide and cls.CONFIG.platform != "ide":
            logger.info("close ide and reset minium")
            reset_minium()

    def _miniSetUp(self):
        super(MiniTest, self)._miniSetUp()
        self._is_perf_setup = False
        self._is_audits_setup = False
        logger.debug("=========Current case：%s=========" % self._testMethodName)
        if self.test_config.only_native:
            logger.info(f"Only native: {self.test_config.only_native}, setUp complete")
            return
        else:
            if self.test_config.auto_relaunch:
                self.app.go_home()
            if self.test_config.platform != "ide":
                if not self.native.handle_modal(btn_text="确定", title="本地调试已结束"):
                    self.native.handle_modal(btn_text="OK", title="Local debugging ended")
        if self.test_config.audit:
            self._is_audits_setup = self._setup_audits()
        if self.test_config.assert_capture:
            self.capture("setup")
        self._is_perf_setup = self._setup_perf()

    def _setup_perf(self):
        self._get_perf_flag = False
        self.perf_data = ""
        if self.test_config.need_perf:
            # logger.debug("_setup_perf")
            self._get_perf_flag = bool(self.native.start_get_perf(timeinterval=0.8))
        return True

    def _teardown_perf(self):
        """
        落地性能相关数据
        """
        if not self._is_perf_setup:
            return
        perf_init = {
            "startup": 0,  # 启动时间
            "avg_cpu": 0,  # 平均CPU
            "max_cpu": 0,  # 最大CPU
            "cpu_data_list": [],  # cpu 数据，可以每3s 打一次
            "avg_mem": 0,  # 平均内存
            "max_mem": 0,  # 最大内存
            "mem_data_list": [],  # 内存数据，可以每3s 打一次
            "avg_fps": 0,  # 平均FPS, 小游戏才有
            "min_fps_rt": 0,  # 最小FPS, 小游戏才有
            "fps_data_list": [],  # FPS数据，可以每3s 打一次
            "fps_time_series_list": [],
            "cpu_time_series_list": [],
            "mem_time_series_list": []
        }
        if self._get_perf_flag:
            self._get_perf_flag = False
            perf_str = self.native.stop_get_perf()
            if self.native.outputs_screen and os.listdir(self.native.outputs_screen):
                page_path = self.page.path
                for file_name in os.listdir(self.native.outputs_screen):
                    file_name_all = os.path.join(self.native.outputs_screen, file_name)
                    # logger.error(file_name_all)
                    shutil.copy(file_name_all, self.screen_dir)
                    path = os.path.join(self.screen_dir, file_name)
                    # logger.error(path)
                    file_name_noext = os.path.splitext(file_name)[0]
                    self.screen_info.append(
                        {
                            "name": file_name,
                            "url": page_path,
                            "path": self.get_relative_path(path),
                            "ts": int(file_name_noext),
                            "datetime": datetime.datetime.fromtimestamp(
                                int(file_name_noext)).strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
            if not perf_str:
                self.perf_data = json.dumps(perf_init)
            else:
                try:
                    perf_arr = json.loads(perf_str)
                    perf_re = {
                        "startup": self.native.get_start_up(),  # 启动时间
                        "avg_cpu": 0,  # 平均CPU
                        "max_cpu": 0,  # 最大CPU
                        "cpu_data_list": [],  # cpu 数据，可以每3s 打一次
                        "avg_mem": 0,  # 平均内存
                        "max_mem": 0,  # 最大内存
                        "mem_data_list": [],  # 内存数据，可以每3s 打一次
                        "avg_fps": 0,  # 平均FPS, 小游戏才有
                        "min_fps_rt": 0,  # 最小FPS, 小游戏才有
                        "fps_data_list": [],  # FPS数据，可以每3s 打一次
                        "fps_time_series_list": [],
                        "cpu_time_series_list": [],
                        "mem_time_series_list": []
                    }
                    timestamp_arr = [int(item["timestamp"]) for item in perf_arr]
                    cpu_arr = [int(item["cpu"]) for item in perf_arr]
                    mem_arr = [float(item["mem"]) for item in perf_arr]
                    fps_arr = [int(item["fps"]) for item in perf_arr]
                    perf_re["fps_time_series_list"] = timestamp_arr
                    perf_re["cpu_time_series_list"] = timestamp_arr
                    perf_re["mem_time_series_list"] = timestamp_arr
                    perf_re["cpu_data_list"] = cpu_arr
                    perf_re["mem_data_list"] = mem_arr
                    perf_re["fps_data_list"] = fps_arr
                    perf_re["avg_cpu"] = sum(cpu_arr) / len(cpu_arr)
                    perf_re["avg_mem"] = sum(mem_arr) / len(mem_arr)
                    perf_re["avg_fps"] = sum(fps_arr) / len(fps_arr)
                    perf_re["max_cpu"] = max(cpu_arr)
                    perf_re["max_mem"] = max(mem_arr)
                    perf_re["min_fps_rt"] = min(fps_arr)
                    self.perf_data = json.dumps(perf_re)
                except:
                    self.perf_data = json.dumps(perf_init)

        else:
            self.perf_data = json.dumps(perf_init)
        self.results["perf_data"] = self.perf_data
        self.results["android_image_list"] = self._gen_android_image_list()
    
    def _setup_audits(self):
        self.audit_html = ""
        self.audit_json = ""
        self.start_audit = False
        if self.test_config.platform == "ide":
            logger.info(f"start run audit score")
            self.start_audit = True
            #开始执行体验评分用例
        else:
            logger.warn(f"Only ide can run audit score")
        return True

    def _teardown_audits(self):
        """
        落地测评数据
        """
        if not self._is_audits_setup:
            return
        if self.start_audit:
            self.stop_audits()
        self.results["audit_html"] = self.audit_html
        self.results["audit_json"] = self.audit_json
        
    def _teardown_app_log(self):
        """
        落地小程序相关的log
        """
        global g_log_message_list, g_network_message_dict
        # 落地小程序log
        weapp_path = "weapp.log"
        weapp_filename = self.wrap_filename(weapp_path)
        log_messages = g_log_message_list
        g_log_message_list = []
        with open(weapp_filename, "w") as f:
            for log_message in log_messages:
                f.write(json.dumps(log_message, ensure_ascii=False) + "\n")
        self.results["weapp_log_path"] = weapp_path
        
        # 落地网络请求log
        request_path = "request.log"
        request_filename = self.wrap_filename(request_path)
        network_message = g_network_message_dict
        g_network_message_dict = {}
        network_message_list = [network_message[msg_id] for msg_id in network_message]
        network_message_list.sort(key=lambda x: x.get("start_timestamp", None) or x["timestamp"])
        with open(request_filename, "w") as f:
            # msg => {timestamp, start_timestamp, request: dict or None, end_timestamp, response: dict or None}
            for msg in network_message_list:
                # logger.debug("\nrequest: {}\nresponse: {}".format(msg.get("request", "Error: Request None"),
                # msg.get("response", "Error: Response Empty")))
                if not msg.get("start_timestamp"):
                    msg["start_timestamp"] = msg["timestamp"]
                    msg["request"] = None
                if not msg.get("end_timestamp"):
                    msg["end_timestamp"] = msg["timestamp"]
                    msg["response"] = None
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.results["request_log_path"] = request_path
    
    def _gen_android_image_list(self):
        """
        整理获取性能数据过程中，相应的截图
        """
        current_monkey_ext_list = []
        perf_data = json.loads(self.perf_data)
        time_series = perf_data["cpu_time_series_list"]
        if len(time_series) == 0:
            return [item["path"] for item in self.screen_info]
        else:
            time_start_index = 0
            time_end_index = 0
            for v in self.screen_info:
                timecount = v["ts"]
                # 从time_series中寻找小于timecount的最大的index
                for index, val in enumerate(time_series[time_start_index:]):
                    logger.info(val)
                    if (val > timecount) or (index == len(time_series) - time_start_index - 1):
                        time_end_index = time_start_index + index - 1
                        break
                # logger.info(time_end_index)
                current_monkey_ext_list += [v["path"] for n in range(time_end_index - time_start_index + 1)]
                time_start_index = time_end_index + 1
            last_count = len(time_series) - len(current_monkey_ext_list)
            # logger.info(last_count)
            if last_count != 0:
                current_monkey_ext_list += [self.screen_info[-1]["path"] for n in range(last_count)]
            # logger.info(current_monkey_ext_list)
            return current_monkey_ext_list

    def _miniTearDown(self):
        logger.debug("=========Current case Down：%s=========" % self._testMethodName)
        try:
            # 更新小程序专属的数据
            self._teardown_perf()
            if self.test_config.audit:
                self._teardown_audits()
            self._teardown_app_log()
            if self.test_config.assert_capture:
                self.capture("teardown")
            # todo: 加参数说明是否需要保存页面参数
            self.results["page_data"] = self.page.data
        except Exception as e:
            logger.exception(e)
            self.results["page_data"] = None
        finally:
            super(MiniTest, self)._miniTearDown()

    @property
    def page(self) -> minium.Page:
        return self.mini.app.get_current_page()

    def capture(self, name=""):
        """
        :param name: 图片名称
        :return:
        """
        if name:
            filename = "%s.png" % name
        else:
            filename = "%s.png" % datetime.datetime.now().strftime("%H%M%S%f")
        path = os.path.join(self.screen_dir, filename)
        if self.CONFIG.platform == "ide":
            try:
                self.mini.app.screen_shot(path)
            except MiniTimeoutError:
                logger.error("App.captureScreenshot fail")
        else:
            self.native.screen_shot(path)
        if os.path.exists(path):
            page_path = self.mini.app.route_return_page.path if self.mini and self.mini.app.route_return_page else ""
            self.add_screen(name, path, page_path)
        else:
            logger.warning("%s not exists", path)
        return path

    def stop_audits(self, format=None):
        """
        获取体验评分
        :return: 体验评分报告
        """
        format = ["html", "json"] if format is None else format
        ret = self.app._stop_audits()
        if len(format) == 0:
            raise Exception("未定义format")
        if not "result" in ret:
            raise Exception("stop_audits获取数据为空")
        if not "report" in ret["result"]:
            raise Exception("stop_audits获取html数据为空")
        if not "data" in ret["result"]:
            raise Exception("stop_audits获取json数据为空")

        for item in format:
            if item == "html":
                audits_html_file = "Audits.html"
                audits_htmlname = self.wrap_filename(audits_html_file)
                html_result = ret["result"]["report"]
                with open(audits_htmlname, "w", encoding="utf-8") as h_f:
                    h_f.write(html_result)
                h_f.close()
                self.audit_html = audits_html_file
                logger.info("success create Audits.html")
            elif item == "json":
                audits_json_file = "Audits.json"
                audits_jsonname = self.wrap_filename(audits_json_file)
                json_result = ret["result"]["data"]
                with open(audits_jsonname, "w") as j_f:
                    j_f.write(json_result)
                j_f.close()
                self.audit_json = audits_json_file
                logger.info("success create Audits.json")
            else:
                pass

    # 加入fps绘图
    # def capture_fps_data(self, fps_str=""):
    #     fpsdata_path = "fpsdata.json"
    #     fpsdata_filename = self.wrap_filename(fpsdata_path)
    #     fpspic_path = "fpsdatapic.png"
    #     fpspic_filename = os.path.join(self.screen_dir, fpspic_path)
    #     if fps_str == "":
    #         return False
    #     with open(fpsdata_filename, "w") as f:
    #         f.write(fps_str)
    #     f.close()
    #
    #     fps_data = json.loads(fps_str)
    #     fps_max = fps_data["fps_max"]
    #     fps_min = fps_data["fps_min"]
    #     fps_avg = fps_data["fps_avg"]
    #     fpsvalue = fps_data["fpsvalue"]
    #     jankvalue = fps_data["jankvalue"]
    #
    #     plt.clf()
    #     plt.subplots_adjust(wspace=0, hspace=0.4)  # 调整子图间距
    #     plt.subplot(211, facecolor="#333744")
    #     plt.xlabel("time(s)", color="c")
    #     plt.ylabel("fps", color="peachpuff")
    #     plt.legend(
    #         title="fps_max:%s fps_min:%s fps_average:%s" % (fps_max, fps_min, fps_avg),
    #         loc="lower left",
    #         fontsize="small",
    #     )
    #     plt.plot(
    #         list(fpsvalue.keys()),
    #         list(fpsvalue.values()),
    #         marker="^",
    #         linewidth=1.0,
    #         color="C4",
    #     )
    #
    #     plt.subplot(212, facecolor="#333744")
    #     plt.xlabel("time(s)", color="c")
    #     plt.ylabel("jank num", color="peachpuff")
    #     plt.scatter(list(jankvalue.keys()), list(jankvalue.values()), s=80, marker="*")
    #     if len(jankvalue) == 0:
    #         plt.legend(title="no jank,very good", loc="lower left", fontsize="small")
    #
    #     plt.savefig(fpspic_filename, dpi=120, facecolor="#333744")
    #
    #     if os.path.exists(fpspic_filename):
    #         self.add_screen(fpspic_path, fpspic_filename, self.page.path)
    #     else:
    #         logger.warning("%s not exists", fpspic_filename)
    #     return fpspic_filename
    #
    # # 加入性能绘图
    # def capture_perf_data(self, perf_arr_str=""):
    #     weapp_path = "perfdata.json"
    #     weapp_filename = self.wrap_filename(weapp_path)
    #     perfpic_path = "perfdatapic.png"
    #     perfpic_filename = os.path.join(self.screen_dir, perfpic_path)
    #     if perf_arr_str == "":
    #         return False
    #     with open(weapp_filename, "w") as f:
    #         f.write(perf_arr_str)
    #     f.close()
    #
    #     perf_arr = json.loads(perf_arr_str)
    #     perf_data_timestamp_arr = []
    #     perf_data_cpu_arr = []
    #     perf_data_mem_arr = []
    #
    #     if len(perf_arr) == 0:
    #         return False
    #     for perf_data in perf_arr:
    #         perf_data_timestamp = list(perf_data.keys())[0]
    #         perf_data_time = int(perf_data_timestamp.split(".")[0])
    #         perf_data_cpu = perf_data[perf_data_timestamp]["cpu"]
    #         perf_data_mem = perf_data[perf_data_timestamp]["mem"]
    #         perf_data_timestamp_arr.append(perf_data_time)
    #         perf_data_cpu_arr.append(perf_data_cpu)
    #         perf_data_mem_arr.append(perf_data_mem)
    #     perf_data_timestamp_arr = [
    #         x - perf_data_timestamp_arr[0] for x in perf_data_timestamp_arr
    #     ]
    #
    #     plt.clf()
    #     plt.subplots_adjust(wspace=0, hspace=0.4)  # 调整子图间距
    #     plt.subplot(211, facecolor="#333744")
    #     plt.xlabel("time(s)", color="c")
    #     plt.ylabel("CPU Usage", color="peachpuff")
    #     plt.plot(
    #         perf_data_timestamp_arr,
    #         perf_data_cpu_arr,
    #         marker="^",
    #         linewidth=1.0,
    #         color="C4",
    #     )
    #
    #     plt.subplot(212, facecolor="#333744")
    #     plt.xlabel("time(s)", color="c")
    #     plt.ylabel("Memory Usage", color="peachpuff")
    #     plt.plot(
    #         perf_data_timestamp_arr,
    #         perf_data_mem_arr,
    #         marker="*",
    #         linewidth=1.0,
    #         color="C4",
    #     )
    #     plt.savefig(perfpic_filename, dpi=120, facecolor="#333744")
    #     if os.path.exists(perfpic_filename):
    #         self.add_screen(perfpic_path, perfpic_filename, self.page.path)
    #     else:
    #         logger.warning("%s not exists", perfpic_filename)
    #     return perfpic_filename

    # 小程序定制化的校验
    def assertPageData(self, data, msg=None):
        """

        :param data:
        :param msg:
        :return:
        """
        pass

    def assertContainTexts(self, texts, msg=None):
        pass

    def assertTexts(self, texts, selector="", msg=None):
        for text in texts:
            elem = self.page.get_element(selector, inner_text=text)
            if elem is None:
                raise AssertionError("selector:%s, inner_text=%s not Found")

    def hook_assert(self, name, ret, reason=None):
        if self.test_config.assert_capture:
            self.capture("{0}-{1}".format(name, "success" if ret else "failed"))
