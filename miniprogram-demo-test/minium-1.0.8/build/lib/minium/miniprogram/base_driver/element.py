#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 元素相关的操作和信息获取
@Date: 2019-03-11 14:42:10
@LastEditTime: 2019-06-06 15:13:32
"""
from .minium_object import MiniumObject, timeout
import time
from .prefixer import *


class BaseElement(MiniumObject):
    """
    元素基类
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super().__init__()
        self.element_id = element.elementId
        self.page_id = page_id
        self._tag_name = element.tagName
        self.connection = connection

    @property
    def data(self):
        """
        自定义组件子类来实现
        :param data:
        :return:
        """
        return

    @data.setter
    def data(self, data):
        """
        自定义组件子类来实现
        :param data:
        :return:
        """
        pass

    def call_method(self, method: str, *params):
        """
        子类来实现
        """
        pass

    def call_func(self, func: str, args=None):
        """
        在 WebView 中执行 JS 脚本，同时会传入 dom 元素
        :param func: 方法名
        :param args: 参数
        :return:
        """
        if not args:
            args = []
        return self._send(
            "Element.callFunction", {"functionName": func, "args": args}
        ).result

    def tap(self):
        """
        点击
        :return: NULL
        """
        self._send("Element.tap")

    def click(self):
        """
        点击, 同 tap
        :return: NULL
        """
        styles = self.styles("pointer-events")
        if styles and styles[0] == "none":
            self.logger.warning("can't click, because pointer-events is none")
            return
        self._send("Element.tap")
        time.sleep(1)

    def move(self, x_offset, y_offset, move_delay=350, smooth=False):
        """
        移动 element
        :param x_offset: x 方向上的偏移，往右为正数，往左为负数
        :param y_offset: y 方向上的偏移，往下为正数，往上为负数
        :param move_delay: 移动延时 (ms)
        :param smooth: 是否平滑移动
        :return:
        """
        self._move(
            x_offset=x_offset, y_offset=y_offset, move_delay=move_delay, smooth=smooth
        )

    def long_press(self, duration=350):
        """
        长按
        :param duration: 时长 (ms)
        :return: NULL
        """
        offset = self.offset
        size = self.size
        ori_changed_touch = ori_touch = {
            "identifier": 0,
            "pageX": offset["left"] + size["width"] // 2,
            "pageY": offset["top"] + size["height"] // 2,
            "clientX": offset["left"] + size["width"] // 2 - self.page_scroll_x,
            "clientY": offset["top"] + size["height"] // 2 - self.page_scroll_y,
        }
        self._touch_start(touches=[ori_touch], changed_touches=[ori_changed_touch])
        time.sleep(duration / 1000)
        self._touch_end(changed_touches=[ori_changed_touch])

    def touch_start(self, touches: list, changed_touches: list):
        """
        touch start
        :param touches:
        :param changed_touches:
        :return:
        """
        self._touch_start(touches=touches, changed_touches=changed_touches)

    def touch_end(self, changed_touches: list):
        """
        touch end
        :param changed_touches:
        :return:
        """
        self._touch_end(changed_touches=changed_touches)

    def touch_move(self, touches: list, changed_touches: list):
        """
        touch move
        :param touches:
        :param changed_touches:
        :return:
        """
        self._touch_move(touches=touches, changed_touches=changed_touches)

    def touch_cancel(self):
        """
        touch cancel
        :return: NULL
        """
        self._send("Element.touchcancel")

    def slide(self, direction, distance):
        """
        拖动
        :param direction:方向
        :param distance:距离
        :return:NULL
        """
        raise NotImplementedError()

    def get_element(
        self, selector, inner_text=None, value=None, text_contains=None, max_timeout=0
    ):
        """
        find elements in current page
        目前支持的选择器有：

        选择器	              样例	                    样例描述
        .class	                      .intro	                    选择所有拥有 class="intro" 的组件
        #id	                      #firstname	            选择拥有 id="firstname" 的组件
        tagname	              view	选择所有    view 组件
        tagname, tagname	  view, checkbox	    选择所有文档的 view 组件和所有的 checkbox 组件
        ::after	                  view::after	            在 view 组件后边插入内容
        ::before	                  view::before	            在 view 组件前边插入内容

        :param selector: 选择器
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        :param max_timeout: 超时时间
        :return:element 对象
        """

        def _element_filter():
            elements = self._get_elements(selector, max_timeout)
            for element in elements:
                if inner_text and element.inner_text != inner_text:
                    continue
                if value and element.value() != value:
                    continue
                if text_contains and text_contains not in element.inner_text:
                    continue
                return element
            return None

        r = _element_filter()
        return r

    def get_elements(self, selector, max_timeout=10):
        """
        find elements in current page
        目前支持的选择器有：

        选择器	              样例	                    样例描述
        .class	                      .intro	                    选择所有拥有 class="intro" 的组件
        #id	                      #firstname	            选择拥有 id="firstname" 的组件
        tagname	              view	选择所有    view 组件
        tagname, tagname	  view, checkbox	    选择所有文档的 view 组件和所有的 checkbox 组件
        ::after	                  view::after	            在 view 组件后边插入内容
        ::before	                  view::before	            在 view 组件前边插入内容

        :param selector: 选择器
        :param max_timeout: 超时时间
        :return:element 对象 list
        """
        return self._get_elements(selector, max_timeout)

    def attribute(self, name):
        """
        获取元素属性
        :return: attribute
        """
        return self._getter("getAttributes", "attributes", name)

    @property
    def size(self):
        """
        get element size
        :return: "offsetWidth", "offsetHeight"
        """
        size_arr = self._dom_property(["offsetWidth", "offsetHeight"])
        return {"width": size_arr[0], "height": size_arr[1]}

    @property
    def offset(self):
        """
        get element offset,
        :return: "offsetLeft","offsetTop"
        """
        rtn = self._send("Element.getOffset")
        return rtn.get("result")

    @property
    def rect(self):
        """
        get element Rect
        :return: "offsetLeft","offsetTop","offsetWidth", "offsetHeight"
        """
        rect_arr = self._dom_property(["offsetWidth", "offsetHeight"])
        offset = self.offset
        return {
            "left": offset["left"],
            "top": offset["top"],
            "width": rect_arr[0],
            "height": rect_arr[1],
        }

    def styles(self, names):
        """
        get element styles
        :param names:
        :return:
        """
        return self._getter("getStyles", "styles", names)

    @property
    def page_scroll_x(self):
        """
        获取窗口顶点与页面顶点的 x 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollX"])[0]

    @property
    def page_scroll_y(self):
        """
        获取窗口顶点与页面顶点的 y 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollY"])[0]

    @property
    def value(self):
        """
        get element vaule
        :return:
        """
        return self._property("value")[0]

    @property
    def inner_text(self):
        """
        get element text
        :return:
        """
        return self._dom_property("innerText")[0]

    @property
    def inner_wxml(self):
        """
        get wxml for element
        :return:
        """
        return self._send("Element.getWXML", {"type": "inner"}).result.wxml

    @property
    def outer_wxml(self):
        """
        get wxml for element self
        :return:
        """
        return self._send("Element.getWXML", {"type": "outer"}).result.wxml

    def _property(self, name):
        """
        get property
        :param name:
        :return:
        """
        return self._getter("getProperties", "properties", name)

    def _dom_property(self, name):
        """
        get property from dom
        :param name:
        :return:
        """
        return self._getter("getDOMProperties", "properties", name)

    def trigger(self, trigger_type, detail):
        """
        just a trigger
        :param trigger_type:
        :param detail:
        :return:
        """
        return self._trigger(trigger_type, detail)

    # private method

    def _get_window_properties(self, names=None):
        """
        获取 window 对象的属性值。
        :param names:
        :return:
        """
        if names is None:
            names = []
        return self._send(
            "Page.getWindowProperties", {"names": names}
        ).result.properties

    def _trigger(self, trigger_type, detail):
        params = dict()
        params["type"] = trigger_type
        if detail:
            params["detail"] = detail
        return self._send("Element.triggerEvent", params)

    def _getter(self, method, return_name, names=""):
        if isinstance(names, list):
            result = self._send("Element." + method, {"names": names})
        elif isinstance(names, str):
            result = self._send("Element." + method, {"names": [names]})
        else:
            raise Exception("invalid names type")
        ret = getattr(result.result, return_name)
        return ret

    def _send(self, method, params=None):
        if params is None:
            params = {}
        params["elementId"] = self.element_id
        params["pageId"] = self.page_id

        return self.connection.send(method, params)

    def _move(self, x_offset, y_offset, move_delay=350, smooth=False):
        offset = self.offset
        size = self.size
        changed_touch = touch = ori_changed_touch = ori_touch = {
            "identifier": 0,
            "pageX": offset["left"] + size["width"] // 2,
            "pageY": offset["top"] + size["height"] // 2,
            "clientX": offset["left"] + size["width"] // 2 - self.page_scroll_x,
            "clientY": offset["top"] + size["height"] // 2 - self.page_scroll_y,
        }
        self._touch_start(touches=[ori_touch], changed_touches=[ori_changed_touch])
        # time.sleep(move_delay / 1000)
        if smooth and (x_offset or y_offset):  # offset不能都为0
            time.sleep(move_delay / 4000)
            temp_x_offset = temp_y_offset = 0
            max_offset = max(abs(x_offset), abs(y_offset))
            step = (move_delay / 2000) / max_offset
            while abs(temp_x_offset) <= abs(x_offset) or abs(temp_y_offset) <= abs(
                y_offset
            ):
                if temp_x_offset == x_offset:
                    pass
                elif not x_offset == 0:
                    temp_x_offset = (
                        (temp_x_offset + 1) if x_offset > 0 else (temp_x_offset - 1)
                    )
                if temp_y_offset == y_offset:
                    pass
                elif not y_offset == 0:
                    temp_y_offset = (
                        (temp_y_offset + 1) if y_offset > 0 else (temp_y_offset - 1)
                    )

                changed_touch = touch = {
                    "identifier": 0,
                    "pageX": offset["left"] + size["width"] // 2 + temp_x_offset,
                    "pageY": offset["top"] + size["height"] // 2 + temp_y_offset,
                    "clientX": offset["left"]
                    + size["width"] // 2
                    - self.page_scroll_x
                    + temp_x_offset,
                    "clientY": offset["top"]
                    + size["height"] // 2
                    - self.page_scroll_y
                    + temp_y_offset,
                }
                self._touch_move(touches=[touch], changed_touches=[changed_touch])
                if temp_x_offset == x_offset and temp_y_offset == y_offset:
                    break
                time.sleep(step)
            time.sleep(move_delay / 4000)
        else:
            time.sleep(move_delay / 2000)
            changed_touch = touch = {
                "identifier": 0,
                "pageX": offset["left"] + size["width"] // 2 + x_offset,
                "pageY": offset["top"] + size["height"] // 2 + y_offset,
                "clientX": offset["left"]
                + size["width"] // 2
                - self.page_scroll_x
                + x_offset,
                "clientY": offset["top"]
                + size["height"] // 2
                - self.page_scroll_y
                + y_offset,
            }
            self._touch_move(touches=[touch], changed_touches=[changed_touch])
            time.sleep(move_delay / 2000)
        # time.sleep(move_delay / 1000)
        self._touch_end(changed_touches=[changed_touch])

    def _touch_start(self, touches: list, changed_touches: list):
        self._send(
            "Element.touchstart",
            params={"touches": touches, "changedTouches": changed_touches},
        )

    def _touch_move(self, touches: list, changed_touches: list):
        self._send(
            "Element.touchmove",
            params={"touches": touches, "changedTouches": changed_touches},
        )

    def _touch_end(self, changed_touches: list):
        touches = []
        self._send(
            "Element.touchend",
            params={"touches": touches, "changedTouches": changed_touches},
        )

    def _get_elements(self, selector, max_timeout=0):
        @timeout(max_timeout)
        def search_elements():
            elements = []
            ret = self._send("Element.getElements", {"selector": selector})
            if hasattr(ret, "error"):
                raise Exception(
                    "Error when finding elements[%s], %s" % (selector, ret.error)
                )
            for el in ret.result.elements:
                if "nodeId" in el.keys():
                    element_cus = CustomElement(el, self.page_id, self.connection)
                    elements.append(element_cus)
                else:
                    element = ELEMENT_TYPE.get(el.tagName, BaseElement)(
                        el, self.page_id, self.connection
                    )

                    elements.append(element)
            return elements

        try:
            self.logger.info("try to find elements: %s" % selector)
            els = search_elements()
            if len(els) == 0:
                self.logger.warning(
                    f"Could not found any element '{selector}' you need"
                )
            else:
                self.logger.info("find elements success: %s" % str(els))
            return els
        except Exception as e:
            raise Exception("elements search fail cause: " + str(e))


class FormElement(BaseElement):
    """
    表单类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(FormElement, self).__init__(element, page_id, connection)

    ############
    #      input     #
    ############
    def input(self, text):
        """
        input 标签输入文本
        :param text:
        :return:
        """
        if self._tag_name != "input" and self._tag_name != "textarea":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "{x}.input".format(x=self._tag_name)
        self.call_func(func, args=[text])
        # self.trigger("input", {"value": text})

    ############
    #      picker   #
    ############
    def pick(self, value):
        """
        处理 picker 组件
        picker 的类型:{
            selector: 普通选择器 => value(int) 表示选择了 range 中的第几个 (下标从 0 开始) ,
            multiSelector: 多列选择器 => value(int) 表示选择了 range 中的第几个 (下标从 0 开始)  ,
            time: 时间选择器 => value(str) 表示选中的时间，格式为"hh:mm"
            date: 日期选择器 => value(str) 表示选中的日期，格式为"YYYY-MM-DD"
            region: 省市区选择器 => value(int) 表示选中的省市区，默认选中每一列的第一个值
            }
        :param value: 需要选择的选项
        :return:
        """
        if self._tag_name != "picker":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        self.trigger("change", {"value": value})
        return

    ############
    #    switch    #
    ############
    def switch(self):
        """
        点击改变 switch 的状态
        :return:
        """
        if self._tag_name != "switch":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "switch.tap"
        self.call_func(func, args=[])

    ###########
    #    slider    #
    ###########
    def slide_to(self, value):
        """
        slider 组件滑动到指定数值
        :return:
        """
        if self._tag_name != "slider":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "slider.slideTo"
        self.call_func(func, args=[value])


class ViewElement(BaseElement):
    """
    视图类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(ViewElement, self).__init__(element, page_id, connection)

    ############
    # scroll-view #
    ############
    def scroll_to(self, x=0, y=0):
        """
        scroll-view 滚动指定距离
        :param x: x 轴上的距离
        :param y: y 轴上的距离
        :return:
        """
        if self._tag_name != "scroll-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "scroll-view.scrollTo"
        self.call_func(func, args=[x, y])

    @property
    def scroll_left(self):
        """
        scroll-view scrollLeft
        :return:
        """
        if self._tag_name != "scroll-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "scroll-view.scrollLeft"
        return self.call_func(func)

    @property
    def scroll_top(self):
        """
        scroll-view scrollTop
        :return:
        """
        if self._tag_name != "scroll-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "scroll-view.scrollTop"
        return self.call_func(func)

    @property
    def scroll_width(self):
        """
        scroll-view scrollWidth
        :return:
        """
        if self._tag_name != "scroll-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "scroll-view.scrollWidth"
        self.call_func(func)

    @property
    def scroll_height(self):
        """
        scroll-view 滚动指定距离
        :return:
        """
        if self._tag_name != "scroll-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "scroll-view.scrollHeight"
        self.call_func(func)

    ############
    #    swiper    #
    ############
    def swipe_to(self, index):
        """
        切换滑块视图容器当前的页面
        :param index:
        :return:
        """
        if self._tag_name != "swiper":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "swiper.swipeTo"
        self.call_func(func, args=[index])

    ###############
    # movable-view #
    ###############
    def move_to(self, x, y):
        """
        可移动的视图容器拖拽滑动
        :param x: x轴方向的偏移
        :param y: y轴方向的偏移
        :return:
        """
        if self._tag_name != "movable-view":
            self.logger.warning(
                "Element's type is not fit for the method which you call"
            )
            return
        func = "movable-view.moveTo"
        self.call_func(func, args=[x, y])


class VideoElement(BaseElement):
    """
    视频播放类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(VideoElement, self).__init__(element, page_id, connection)
        self.video_id = element.get("videoId", None)
        self.controller = VideoController(connection, self.video_id)
        self.media_type = MediaType.VIDEO

    def _call_context_method(self, method: str, args: list = None):
        if not args:
            args = []
        params = {"videoId": self.video_id, "method": method, "args": args}
        return self._send("Element.callContextMethod", params=params)

    def play(self):
        """
        播放视频
        :return:
        """
        # self.controller.play()
        self._call_context_method(method="play")

    def pause(self):
        """
        暂停视频
        :return:
        """
        # self.controller.pause()
        self._call_context_method(method="pause")

    def stop(self):
        """
        停止视频
        :return:
        """
        # self.controller.stop()
        self._call_context_method(method="stop")

    def seek(self, position: int):
        """
        跳转到指定位置
        :param position: 跳转到的位置，单位 s
        :return:
        """
        # self.controller.seek(position)
        self._call_context_method(method="seek", args=[position])

    def send_danmu(self, text: str, color="#ff0000"):
        """
        发送弹幕
        :param text: 弹幕文字
        :param color: 弹幕颜色
        :return:
        """
        # self.controller.send_danmu(text, color)
        self._call_context_method(
            method="sendDanmu", args=[{"text": text, "color": color}]
        )

    def playback_rate(self, rate: float):
        """
        设置倍速播放
        :param rate: 倍率，支持 0.5/0.8/1.0/1.25/1.5，2.6.3 起支持 2.0 倍速
        :return:
        """
        # self.controller.playback_rate(rate)
        self._call_context_method(method="playbackRate", args=[rate])

    def request_full_screen(self, direction=0):
        """
        全屏
        :param direction: 设置全屏时视频的方向，不指定则根据宽高比自动判断
        0	正常竖向
        90	屏幕逆时针90度
        -90	屏幕顺时针90度
        :return: status
        """
        # self.controller.request_full_screen(direction)
        self._call_context_method(
            method="requestFullScreen", args=[{"direction": direction}]
        )

    def exit_full_screen(self):
        """
        退出全屏
        :return:
        """
        # self.controller.exit_full_screen()
        self._call_context_method(method="exitFullScreen")

    def show_status_bar(self):
        """
        显示状态栏，仅在iOS全屏下有效
        :return:
        """
        # self.controller.show_status_bar()
        self._call_context_method(method="showStatusBar")

    def hide_status_bar(self):
        """
        隐藏状态栏，仅在iOS全屏下有效
        :return:
        """
        # self.controller.hide_status_bar()
        self._call_context_method(method="hideStatusBar")


class AudioElement(BaseElement):
    """
    音频播放类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(AudioElement, self).__init__(element, page_id, connection)
        self.controller = AudioController(connection)
        self.media_type = MediaType.AUDIO

    def set_src(self, src):
        """
        设置音频地址
        :param src: 音频地址
        :return:
        """
        self.controller.set_src(src)

    def play(self):
        """
        播放音频
        :return:
        """
        self.controller.play()

    def pause(self):
        """
        暂停音频
        :return:
        """
        self.controller.pause()

    def seek(self, position):
        """
        跳转到指定位置
        :param position: 时间，单位：s
        :return:
        """
        self.controller.seek(position)


class LivePlayerElement(BaseElement):
    """
    直播播放类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(LivePlayerElement, self).__init__(element, page_id, connection)
        self.controller = LivePlayerController(connection)
        self.media_type = MediaType.LIVE_PLAY

    def play(self):
        """
        播放
        :return:
        """
        self.controller.play()

    def stop(self):
        """
        停止
        :return:
        """
        self.controller.stop()

    def mute(self):
        """
        静音
        :return:
        """
        self.controller.mute()

    def pause(self):
        """
        暂停
        :return:
        """
        self.controller.pause()

    def resume(self):
        """
        恢复
        :return:
        """
        self.controller.resume()

    def request_full_screen(self, direction=0):
        """
        全屏
        :param direction: 方向
        0	正常竖向
        90	屏幕逆时针90度
        -90	屏幕顺时针90度
        :return: status
        """
        self.controller.request_full_screen(direction)

    def exit_full_screen(self):
        """
        退出全屏
        :return:
        """
        self.controller.exit_full_screen()

    def snapshot(self):
        """
        截屏
        :return:
        """
        self.controller.snapshot()


class LivePusherElement(BaseElement):
    """
    直播推流类型元素
    """

    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(LivePusherElement, self).__init__(element, page_id, connection)
        self.controller = LivePusherController(connection)
        self.media_type = MediaType.LIVE_PUSH

    def start(self):
        """
        开始推流，同时开启摄像头预览
        :return:
        """
        self.controller.start()

    def stop(self):
        """
        停止推流，同时停止摄像头预览
        :return:
        """
        self.controller.stop()

    def pause(self):
        """
        暂停推流
        :return:
        """
        self.controller.pause()

    def resume(self):
        """
        恢复推流
        :return:
        """
        self.controller.resume()

    def switch_camera(self):
        """
        切换前后摄像头
        :return:
        """
        self.controller.switch_camera()

    def snapshot(self):
        """
        截屏
        :return:
        """
        self.controller.snapshot()

    def toggle_torch(self):
        """
        切换手电筒
        :return:
        """
        self.controller.toggle_torch()

    def play_bgm(self, url):
        """
        播放背景音
        :param url: 背景音链接
        :return:
        """
        self.controller.play_bgm(url)

    def stop_bgm(self):
        """
        停止背景音
        :return:
        """
        self.controller.stop_bgm()

    def pause_bgm(self):
        """
        暂停背景音
        :return:
        """
        self.controller.pause_bgm()

    def resume_bgm(self):
        """
        恢复背景音
        :return:
        """
        self.controller.resume_bgm()

    def set_bgm_volume(self, volume):
        """
        设置背景音音量
        :param volume: 音量大小，范围是 0-1
        :return:
        """
        self.controller.set_bgm_volume(volume)

    def start_preview(self):
        """
        开启摄像头预览
        :return:
        """
        self.controller.start_preview()

    def stop_preview(self):
        """
        关闭摄像头预览
        :return:
        """
        self.controller.stop_preview()


class CustomElement(BaseElement):
    def __init__(self, element, page_id, connection):
        """
        初始化
        """
        super(CustomElement, self).__init__(element, page_id, connection)
        self.node_id = element.get("nodeId", None)

    def _send(self, method, params=None):
        if params is None:
            params = {}
        params["elementId"] = self.element_id
        params["pageId"] = self.page_id
        params["nodeId"] = self.node_id
        return self.connection.send(method, params)

    @property
    def data(self):
        return self._send("Element.getData").result.data

    @data.setter
    def data(self, data):
        """
        设置页面 data
        :param data:
        :return:
        """
        self._send("Element.setData", {"data": data})

    def call_method(self, method: str, *params):
        """
        调用自定义组件实例方法
        :param method:
        :param params:
        :return:
        """
        if not params:
            params = []
        return self._send("Element.callMethod", {"method": method, "args": params})


class MediaController(MiniumObject):
    """
    媒体类型元素控制
    """

    def __init__(self):
        """
        初始化
        """
        pass


class VideoController(MediaController):
    """
    视频播放控制
    """

    def __init__(self, connection, video_id):
        """
        初始化
        :param connection:
        :param video_id:
        """
        super().__init__()
        self.connection = connection
        self.video_id = video_id

    def play(self):
        """
        播放视频
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.play()}")

    def pause(self):
        """
        暂停视频
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.pause()}")

    def stop(self):
        """
        停止视频
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.stop()}")

    def seek(self, position: int):
        """
        跳转到指定位置
        :param position: 跳转到的位置，单位 s
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.seek(%s)}" % position)

    def send_danmu(self, text: str, color="#000000"):
        """
        发送弹幕
        :param text: 弹幕文字
        :param color: 弹幕颜色
        :return:
        """
        self.evaluate(
            "function(){global.minium.videoContext.sendDanmu({text:'%s', color:'%s'})}"
            % (text, color)
        )

    def playback_rate(self, rate):
        """
        设置倍速播放
        :param rate: 倍率，支持 0.5/0.8/1.0/1.25/1.5，2.6.3 起支持 2.0 倍速
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.playbackRate(%s)}" % rate)

    def request_full_screen(self, direction=0):
        """
        全屏
        :return: status
        """
        self.evaluate(
            "function(){global.minium.videoContext.requestFullScreen({direction: %s})}"
            % direction
        )

    def exit_full_screen(self):
        """
        退出全屏
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.exitFullScreen()}")

    def show_status_bar(self):
        """
        显示状态栏，仅在iOS全屏下有效
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.showStatusBar()}")

    def hide_status_bar(self):
        """
        隐藏状态栏，仅在iOS全屏下有效
        :return:
        """
        self.evaluate("function(){global.minium.videoContext.hideStatusBar()}")


class AudioController(MediaController):
    """
    音频播放控制
    """

    def __init__(self, connection):
        """
        初始化
        """
        super().__init__()
        self.connection = connection

    def set_src(self, src):
        """
        设置音频地址
        :param src: 音频地址
        :return:
        """
        self.evaluate("function(){global.minium.audioContext.setSrc(%s)}" % src)

    def play(self):
        """
        播放音频
        :return:
        """
        self.evaluate("function(){global.minium.audioContext.play()}")

    def pause(self):
        """
        暂停音频
        :return:
        """
        self.evaluate("function(){global.minium.audioContext.pause()}")

    def seek(self, position):
        """
        跳转到指定位置
        :param position: 时间，单位：s
        :return:
        """
        self.evaluate("function(){global.minium.audioContext.seek(%s)}" % position)


class LivePlayerController(MediaController):
    """
    直播播放/推流控制
    """

    def __init__(self, connection):
        """
        初始化
        """
        super().__init__()
        self.connection = connection

    def play(self):
        """
        播放
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.play()}")

    def stop(self):
        """
        停止
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.stop()}")

    def mute(self):
        """
        静音
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.mute()}")

    def pause(self):
        """
        暂停
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.pause()}")

    def resume(self):
        """
        恢复
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.resume()}")

    def request_full_screen(self, direction=0):
        """
        全屏
        :param direction: 方向
        0	正常竖向
        90	屏幕逆时针90度
        -90	屏幕顺时针90度
        :return: status
        """
        self.evaluate(
            "function(){global.minium.livePlayerContext.requestFullScreen({direction: %s})}"
            % direction
        )

    def exit_full_screen(self):
        """
        退出全屏
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.exitFullScreen()}")

    def snapshot(self):
        """
        截屏
        :return:
        """
        self.evaluate("function(){global.minium.livePlayerContext.snapshot()}")


class LivePusherController(MediaController):
    """
    直播播放/推流控制
    """

    def __init__(self, connection):
        """
        初始化
        """
        super().__init__()
        self.connection = connection

    def start(self):
        """
        开始推流，同时开启摄像头预览
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.start()}")

    def stop(self):
        """
        停止推流，同时停止摄像头预览
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.stop()}")

    def pause(self):
        """
        暂停推流
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.pause()}")

    def resume(self):
        """
        恢复推流
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.resume()}")

    def switch_camera(self):
        """
        切换前后摄像头
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.switchCamera()}")

    def snapshot(self):
        """
        截屏
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.snapshot()}")

    def toggle_torch(self):
        """
        切换手电筒
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.toggleTorch()}")

    def play_bgm(self, url):
        """
        播放背景音
        :param url: 背景音链接
        :return:
        """
        self.evaluate(
            "function(){global.minium.livePusherContext.PlayBGM({url:'%s'})}" % url
        )

    def stop_bgm(self):
        """
        停止背景音
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.stopBGM()}")

    def pause_bgm(self):
        """
        暂停背景音
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.pauseBGM()}")

    def resume_bgm(self):
        """
        恢复背景音
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.resumeBGM()}")

    def set_bgm_volume(self, volume):
        """
        设置背景音音量
        :param volume: 音量大小，范围是 0-1
        :return:
        """
        self.evaluate(
            "function(){global.minium.livePusherContext.setBGMVolume({volume:'%s'})}"
            % volume
        )

    def start_preview(self):
        """
        开启摄像头预览
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.startPreview()}")

    def stop_preview(self):
        """
        关闭摄像头预览
        :return:
        """
        self.evaluate("function(){global.minium.livePusherContext.startPreview()}")


ELEMENT_TYPE = {
    "video": VideoElement,
    "audio": AudioElement,
    "live-player": LivePlayerElement,
    "live-pusher": LivePusherElement,
    "scroll-view": ViewElement,
    "swiper": ViewElement,
    "movable-view": ViewElement,
    "input": FormElement,
    "textarea": FormElement,
    "switch": FormElement,
    "slider": FormElement,
    "picker": FormElement,
}
