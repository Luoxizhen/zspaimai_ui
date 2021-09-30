#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import os.path
import at
import time
from .basenative import BaseNative, NativeError
import json
import logging
import threading
import shutil

WECHAT_PACKAGE = "com.tencent.mm"
WECHAT_ACTIVITY = "ui.LauncherUI"
logger = logging.getLogger()
_MIN_NORMALIZED_FRAME_LENGTH = 0.5


class UiDefine:
    def __init__(self, _at: at.At):
        self.at = _at

        # 小程序权限申请弹框
        self.btn_authorize_ok = self.at.e.cls_name("android.widget.Button").text("允许")
        self.btn_authorize_cancel = self.at.e.cls_name("android.widget.Button").text(
            "取消"
        )

        # 小程序菜单
        self.action_menu = self.at.e.cls_name("android.widget.ImageButton").desc("更多")
        self.action_home = self.at.e.cls_name("android.widget.ImageButton").desc("关闭")
        self.title = (
            self.action_home.parent()
                .cls_name("android.widget.LinearLayout")
                .instance(1)
                .child()
                .cls_name("android.widget.TextView")
        )

        # 小程序组件
        self.comp_picker_input = self.at.e.cls_name("android.widget.EditText").rid(
            "android:id/numberpicker_input"
        )


class WXAndroidNative(BaseNative):
    def __init__(self, json_conf):
        super(WXAndroidNative, self).__init__(json_conf)
        if json_conf is None:
            json_conf = {}
        self.serial = json_conf.get("serial")
        uiautomator_version = int(json_conf.get("uiautomator_version", "2"))
        at.uiautomator_version = uiautomator_version
        self.at = at.At(self.serial)
        self.at.java_driver.set_capture_op(False)
        self.ui = UiDefine(self.at)
        self.lang = json_conf.get("lang")
        self.perf_thread = None
        self.perf_flag = False
        self.ef_able_flag = False
        self.pref_data = []
        self.fps_data_dict = {}  # fps dict
        self.jank_count_dict = {}  # 卡顿次数
        self.fps_thread = None
        self.outputs_screen = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image")
        self._empty_base_screen_dir(self.outputs_screen)

    def _empty_base_screen_dir(self, dirname):
        if os.path.exists(dirname):
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
                time.sleep(1)
            else:
                os.remove(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    @property
    def logcat(self):
        return self.at.logcat

    def connect_weapp(self, path):
        self.at.apkapi.launch()
        gallery_name = "atstub"
        self.at.apkapi.add_gallery(path)
        self.stop_wechat()
        self.start_wechat()
        if self.lang == "en":
            self.e.text("Discover").click()
            self.e.text("Scan").click()
            # self.e.cls_name("android.widget.ImageButton").click()
            # self.e.text("Choose QR Code from Album").click()
            self.e.cls_name("android.widget.LinearLayout").instance(1).click()
            self.e.text("All Images").click()
            self.e.text(gallery_name).click()
            self.e.desc_contains("Image 1").click()
            self.e.text_contains("Scanning").wait_disappear()
        else:
            self.e.text("发现").click()
            self.e.text("扫一扫").click()
            self.e.cls_name("android.widget.LinearLayout").instance(1).click()
            # self.e.cls_name("android.widget.ImageButton").click()
            # self.e.text("从相册选取二维码").click()
            self.e.text("所有图片").click()
            self.e.text(gallery_name).click()
            self.e.desc_contains("图片 1").click()
            self.e.text_contains("扫描中").wait_disappear()

    def screen_shot(self, filename, quality=30):
        return self.at.device.screen_shot(filename, quality=quality)

    def pick_media_file(
            self,
            cap_type="camera",
            media_type="photo",
            original=False,
            duration=5.0,
            index_list=None,
    ):
        pass

    def input_text(self, text):
        """
        """
        self.at.e.edit_text().enter(text, is_click=False)

    def input_clear(self):
        """
        input 组件清除文字(使用此函数之前必须确保输入框处于输入状态)
        :return:
        """
        self.at.e.edit_text().enter("", is_click=False)

    def textarea_text(self, text, index=0):
        self.at.e.edit_text().instance(index).enter(text, is_click=False)

    def textarea_clear(self, index=0):
        self.at.e.edit_text().instance(index).enter("", is_click=False)

    def map_select_location(self, name):
        print("map_select_location")
        self.at.e.text("搜索地点").click()
        self.at.e.edit_text().enter_chinese(name)
        self.at.adb.press_search()
        self.at.adb.press_back()
        while self.at.e.cls_name("android.widget.TextView").text_contains(name).exists():
            try:
                self.at.e.cls_name("android.widget.TextView").text_contains(name).click()
                if self.at.e.text("完成").exists:
                    break
            except Exception as e:
                logger.warning(str(e))
        self.at.e.text("完成").click()

    def map_back_to_mp(self):
        self.at.e.rid("com.tencent.mm:id/btn_back_txt").click()

    def deactivate(self, duration):
        self.at.adb.press_home()
        time.sleep(duration)
        self.at.adb.start_app("com.tencent.mm", "ui.LauncherUI", "-n")
        time.sleep(2)
        screen_width = int(self.at.device.width())
        screen_height = int(self.at.device.height())
        self.at.device.swipe(
            int(screen_width / 2),
            int(screen_height * 1 / 4),
            int(screen_width / 2),
            int(screen_height * 4 / 5),
            10,
        )
        time.sleep(2)
        self.textbounds = self.at.e.rid("com.tencent.mm:id/test_mask").get_bounds()
        print(self.textbounds)
        xx = self.textbounds[0]
        yy = self.textbounds[1]
        self.at.adb.click_point(xx, yy)

    def _allow_authorize(self, answer):
        if answer:
            self._handle_btn("允许")
        else:
            self._handle_btn("取消")

    def allow_login(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_user_info(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_location(self, answer=True):
        self._allow_authorize(answer)

    def _handle_btn(self,btn_text="确定"):
        self.at.java_driver.reconnect()
        ret = self.e.cls_name("android.widget.Button").focusable(True).text(btn_text).click()
        return ret

    def handle_modal(self, btn_text="确定", title=None):
        if title:
            if not self.at.e.text_contains(title).exists():
                logger.info("没有出现预期弹窗：title[%s]", title)
                return False
        ret = self._handle_btn(btn_text)
        return ret

    def handle_action_sheet(self, item):
        ret = self.e.cls_name("android.widget.TextView").text(item).click()
        return ret

    def forward_miniprogram(self, name, text=None, create_new_chat=True):
        self.ui.action_menu.click()
        self.e.text("发送给朋友").click()
        return self.forward_miniprogram_inside(name, text, create_new_chat)

    def forward_miniprogram_inside(self, name, text=None, create_new_chat=True):
        if create_new_chat:
            self.e.text("创建新聊天").click()
            self.e.text_contains(name).click(True)
            if self.e.text("确定(1)").exists():
                self.e.text("确定(1)").enabled(True).click()
            else:
                self.e.text("完成(1)").enabled(True).click()
        else:
            self.e.text_contains(name).click(True)
        if text:
            self.e.edit_text().enter(text)
        self.e.cls_name("android.widget.Button").text("发送").click()
        self.e.text("已转发").wait_disappear()

    def send_custom_message(self, message=None):
        pass

    def call_phone(self):
        pass

    def handle_picker(self, *items):
        instance = 0
        for item in items:
            input_elem = self.ui.comp_picker_input.instance(instance)
            next_elem = input_elem.parent().child("android.widget.Button")
            first_text = input_elem.get_text()
            while True:
                # todo: 要判断上滑还是下滑
                current_text = input_elem.get_text()
                if current_text == str(item):
                    break
                if first_text == str(item):
                    raise NativeError(" not found")
            instance += 1

    def get_authorize_settings(self):
        """
        在小程序的授权页面，获取小程序的授权设置
        :return:
        """
        ui_views = self.at.java_driver.dump_ui()
        setting_map = {}
        for ui_view in ui_views:
            if ui_view.cls_name == "android.view.View" and ui_view.content_desc in [
                "已开启",
                "已关闭",
            ]:
                check_status = True if ui_view.content_desc == "已开启" else False
                parant_view = ui_view.sibling().get_children()[0]
                setting_map[parant_view.text] = check_status
        return setting_map

    def back_from_authorize_setting(self):
        """
        从小程序授权页面跳转回小程序
        :return:
        """
        self.at.adb.press_back()

    def authorize_page_checkbox_enable(self, name, enable):
        """
        在小程序授权设置页面操作CheckBox
        :param name: 设置的名称
        :param enable: 是否打开
        :return:
        """
        setting_map = self.get_authorize_settings()
        if setting_map.get(name) == enable:
            return
        self.e.text(name).parent().instance(2).child().cls_name(
            "android.view.View"
        ).click()
        if not enable:
            self.e.cls_name("android.widget.Button").text("关闭授权").click_if_exists(5)

    def release(self):
        self.at.release()

    def start_wechat(self):
        if self.at.adb.app_is_running(WECHAT_PACKAGE):           
            self.at.adb.stop_app(WECHAT_PACKAGE)  #先关掉
        self.at.adb.start_app(WECHAT_PACKAGE, WECHAT_ACTIVITY)

    def stop_wechat(self):
        self.at.adb.stop_app(WECHAT_PACKAGE)

    def click_point(self, x, y):
        self.at.adb.click_point(x, y)

    def stop_get_perf(self):
        self.perf_flag = False
        self.perf_thread.join()
        if self.pref_data:
            pref_data_str = json.dumps(self.pref_data)
            return pref_data_str
        else:
            logger.error("get perf data fail")
            return ""

    def write_perf_data(self, processname, pid, curview, timeinterval):
        while self.perf_flag:
            if not self.ef_able_flag:
                perf_cpu = self.at.adb.get_cpu_rate_new_c(pid)
            else:
                perf_cpu = self.at.adb.get_cpu_rate_new_ef(pid)
            perf_mem = self.at.adb.get_mem_used(processname)

            fps_lines = self.at.adb.get_fps(curview)
            # print(fps_lines)
            refresh_period, timestamps = self._collectFPSData(fps_lines)
            fps_data = self._CalculateResults(refresh_period, timestamps)

            timestamp = int(time.time())
            self.pref_data.append(
                {"cpu": perf_cpu, "mem": perf_mem, "fps": fps_data, "timestamp": timestamp}
            )
            img_name = os.path.join(self.outputs_screen, "%d.png" % timestamp)
            self.screen_shot(img_name)
            time.sleep(timeinterval)

    def start_get_perf(self, timeinterval=15):
        retry = 3
        while retry > 0:
            retry -= 1
            processname, pid = self.at.adb.get_current_process_appbrand()
            # print(processname)
            self.at.adb.clearbuffer()
            curview = self.at.adb.get_current_view_appbrand()
            if (not processname) or (not curview):
                logger.error("current activity is not appbrand")
                time.sleep(2)
                continue
            else:
                break
        # logger.debug(processname)
        # logger.debug(curview)
        # logger.debug(pid)
        output = self.at.adb.run_shell("ps -ef")
        if output.count("bad pid") != 0:
            self.ef_able_flag = False
        else:
            self.ef_able_flag = True
        if processname and curview:
            try:
                self.perf_flag = True
                self.pref_data = []
                self.perf_thread = threading.Thread(
                    target=self.write_perf_data, args=(processname, pid, curview, timeinterval)
                )
                self.perf_thread.daemon = True
                self.perf_thread.start()
                return self.perf_flag
            except:
                return None
        else:
            return None

    def get_pay_value(self):
        try:
            if self.e.text_contains("￥").exists():
                return self.e.text_contains("￥").get_text()
            else:
                return ""
        except:
            return ""

    def close_payment_dialog(self):
        if self.e.text_contains("￥").exists(10):
            return self.e.desc("关闭").click()
        else:
            if self.e.text_contains("支付方式").exists():
                self.at.adb.press_back() #有可能找不到输入框，先后退尝试
            raise TypeError("支付框不存在")

    def text_exists(self, text="", iscontain=False, wait_seconds=5):
        if iscontain:
            return self.e.text_contains(text=text).exists(wait_seconds)
        else:
            return self.e.text(text=text).exists(wait_seconds)

    def text_click(self, text="", iscontain=False):
        if iscontain:
            return self.e.text_contains(text=text).click(is_scroll=True)
        else:
            return self.e.text(text=text).click(is_scroll=True)

    def _get_number_point(self, number):
        """
        获取数字的中心坐标
        :param number:
        :return:
        """
        if type(number) is str:
            if type(eval(number)) is not int:
                raise TypeError(u"number应该为int")
            number = int(number)
        rect = self.e.rid("com.tencent.mm:id/g60").get_rect()
        column_distance = (rect.right - rect.left) / 3  # 列距
        line_distance = (rect.bottom - rect.top) / 4  # 行距

        start_center_point = {"x": rect.left + column_distance / 2, "y": rect.top + line_distance / 2}

        if number == 1:
            x = start_center_point['x']
            y = start_center_point['y']
        elif number == 0:
            x = start_center_point['x'] + column_distance
            y = start_center_point['y'] + line_distance * 3
        else:
            row_num = (number - 1) // 3  # 跟起点相差几行
            column_num = number % 3
            if column_num == 0:
                column_num = 3
            column_num = column_num - 1  # 跟起点相差几列
            x = start_center_point['x'] + column_distance * column_num
            y = start_center_point['y'] + line_distance * row_num
        print("number:{0} ===> Point({1},{2})".format(number, x, y))
        return {"x": x, "y": y}

    def input_pay_password(self, psw=""):
        check_flag = self.e.text("请输入支付密码").click_if_exists(5)
        if not check_flag:
            return False
        if not psw:
            raise TypeError("未传入支付密码")
        psw = str(psw)
        if type(eval(psw)) is not int:
            raise TypeError("非法支付密码字符串")
        elif len(psw) != 6 :
            raise TypeError(u"密码长度必须为6位数")
        for number in psw:
            point = self._get_number_point(number)
            self.at.device.click_on_point(point['x'], point['y'])

        if self.e.text("支付成功").exists(10):
            self.e.text("完成").click(is_scroll=True)
        else:
            raise TypeError("支付失败")

    def _collectFPSData(self, results):
        timestamps = []
        if len(results)<128:
            return (0, timestamps)
        nanoseconds_per_second = 1e9
        refresh_period = int(results[0]) / nanoseconds_per_second
        # logger.debug("refresh_period: %s" % refresh_period)
        pending_fence_timestamp = (1 << 63) - 1
        for line in results[1:]:
            fields = line.split()
            if len(fields) != 3:
                continue
            if not fields[0].isnumeric():
                continue
            if int(fields[0]) == 0:
                continue
            timestamp = int(fields[1])
            if timestamp == pending_fence_timestamp:
                continue
            timestamp /= nanoseconds_per_second
            timestamps.append(timestamp)
        # logger.error("timestamps: %s" % timestamps)
        return (refresh_period,timestamps)

    def _GetNormalizedDeltas(self, data, refresh_period, min_normalized_delta=None):
        deltas = [t2 - t1 for t1, t2 in zip(data, data[1:])]
        if min_normalized_delta != None:
            deltas = filter(lambda d: d / refresh_period >= min_normalized_delta,
                            deltas)
            deltas = list(deltas)
        return (deltas, [delta / refresh_period for delta in deltas])

    def _CalculateResults(self, refresh_period, timestamps):
        """Returns a list of SurfaceStatsCollector.Result."""
        frame_count = len(timestamps)
        if frame_count == 0:
            return 0
        seconds = timestamps[-1] - timestamps[0]
        frame_lengths, normalized_frame_lengths = \
            self._GetNormalizedDeltas(
                timestamps, refresh_period, _MIN_NORMALIZED_FRAME_LENGTH)
        if len(frame_lengths) < frame_count - 1:
            logging.warning('Skipping frame lengths that are too short.')
            frame_count = len(frame_lengths) + 1
        if len(frame_lengths) == 0:
            raise Exception('No valid frames lengths found.')
        return str(int(round((frame_count - 1) / seconds)))

    # def start_get_fps(self, timeinterval=1):
    #     self.fps_flag = True
    #     self.at.adb.clearbuffer()
    #     curview = self.at.adb.get_current_view_appbrand()
    #     if not curview:
    #         return None
    #     try:
    #         self.fps_thread = threading.Thread(
    #             target=self.count_fps_data, args=(curview, timeinterval)
    #         )
    #         self.fps_thread.setDaemon(True)
    #         self.fps_thread.start()
    #
    #     except Exception as e:
    #         print(e)
    #
    # def count_fps_data(self, curview, timeinterval):
    #     fps_index = -1
    #     while self.fps_flag:
    #         fps_index += 1
    #         fps_data = True
    #         fps_lines = self.at.adb.get_fps(curview)
    #         if len(fps_lines) < 128:
    #             raise RuntimeError("current activity is not appbrand")
    #         for line in fps_lines:
    #             if line.count("0\t0\t0") != 0:
    #                 fps_data = False
    #                 break
    #         if not fps_data:
    #             time.sleep(timeinterval)
    #         else:
    #             fps_data_lines = [line.split("	") for line in fps_lines]
    #             end_timestamp = fps_data_lines[len(fps_data_lines) - 1][1]
    #             start_timestamp = fps_data_lines[len(fps_data_lines) - 127][1]
    #             time_period = (float(end_timestamp) - float(start_timestamp)) / 10 ** 9
    #
    #             refresh_period = int(fps_data_lines[0][0])
    #             jank_count = 0
    #             for fps_data_index in range(1, len(fps_data_lines)):
    #                 jank_prob = (
    #                     int(fps_data_lines[fps_data_index][2])
    #                     - int(fps_data_lines[fps_data_index][0])
    #                 ) / refresh_period
    #                 if jank_prob >= 1:
    #                     jank_count += 1
    #
    #             fps_data = int(126 / time_period)
    #             if fps_data != 0:
    #                 self.fps_data_dict[fps_index] = fps_data
    #             if jank_count != 0:
    #                 self.jank_count_dict[fps_index] = jank_count
    #             time.sleep(timeinterval)
    #
    # def stop_get_fps(self):
    #     self.fps_flag = False
    #     self.fps_thread.join()
    #     if len(self.fps_data_dict) != 0:
    #         fps_data_arr = list(self.fps_data_dict.values())
    #         fps_max = max(fps_data_arr)
    #         fps_min = min(fps_data_arr)
    #         fps_avg = int(sum(fps_data_arr) / len(fps_data_arr))
    #         get_fps_result = {
    #             "fps_max": fps_max,
    #             "fps_min": fps_min,
    #             "fps_avg": fps_avg,
    #             "fpsvalue": self.fps_data_dict,
    #             "jankvalue": self.jank_count_dict,
    #         }
    #         return json.dumps(get_fps_result)
    #     else:
    #         raise RuntimeError("get fps data fail")

    @property
    def e(self):
        return self.at.e


if __name__ == "__main__":
    n = WXAndroidNative({"lang": "en"})
    n.handle_modal("queding", "")
