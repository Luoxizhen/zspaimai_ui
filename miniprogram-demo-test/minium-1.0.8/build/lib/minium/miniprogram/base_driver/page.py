#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 小程序页面
@Date: 2019-03-11 14:42:29
@LastEditTime: 2019-06-05 17:04:02
"""
import typing
from .element import *
from .minium_object import MiniumObject, timeout
# 需要在setup中加上cssselect库
# from cssselect.xpath import HTMLTranslator
# from cssselect.parser import SelectorError

# translator = HTMLTranslator()

class Page(MiniumObject):
    """
    页面相关接口
    """

    def __init__(self, page_id, path, query, connection):
        """
        初始化页面
        """
        super().__init__()
        self.page_id = page_id
        self.path = path
        self.query = query
        self.connection = connection

    def __repr__(self):
        return "Page(id={0}, path={1}, query={2})".format(
            self.page_id, self.path, self.query
        )

    @property
    def data(self):
        """
        获取页面 Data
        :return: json
        """
        return self._send("Page.getData").result.data

    def wait_data_contains(self, *keys_list, max_timeout=10):
        @timeout(max_timeout)
        def f():
            d = self.data
            for keys in keys_list:
                obj = d
                for key in keys:
                    if obj and key in obj:
                        obj = obj[key]
                    else:
                        return False
            return True
        try:
            ret = f()
            return ret
        except Exception as e:
            self.logger.exception(e)
            return False

    @data.setter
    def data(self, data):
        """
        设置页面 data
        :param data:
        :return:
        """
        self._send("Page.setData", {"data": data})

    def element_is_exists(self, selector, max_timeout=10):
        """
        查询元素是否存在
        :param selector:
        :param max_timeout: 超时时间
        :return:
        """
        return self._element_is_exists(selector=selector, max_timeout=max_timeout)

    def get_element(
            self, selector, inner_text=None, value=None, text_contains=None, max_timeout=0
    ) -> BaseElement or VideoElement or AudioElement or \
         ViewElement or FormElement or LivePlayerElement or LivePusherElement:
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

    def call_method(self, method, args=None):
        if not args:
            args = []
        if isinstance(args, dict):
            args = [args]
        return self._send("Page.callMethod", {"method": method, "args": args})

    def wait_for(self, condition=None, max_timeout=10):
        s_time = time.time()
        if isinstance(condition, int):
            time.sleep(condition)
            self.logger.debug("waitFor: %s s"%(time.time()-s_time))
            return True
        elif isinstance(condition, str):
            while (time.time()-s_time) < max_timeout:
                if self._element_is_exists(condition):
                    return True
                else:
                    time.sleep(0.25)
            else:
                return False
        elif hasattr(condition, '__call__'):
            while (time.time() - s_time) < max_timeout:
                res = condition()
                if res:
                    return True
                else:
                    time.sleep(0.25)
            else:
                return False

    def get_elements(self, selector, max_timeout=20) -> typing.List[BaseElement]:
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

    @property
    def inner_size(self):
        """
        get window size
        :return:
        """
        size_arr = self._get_window_properties(["innerWidth", "innerHeight"])
        return {"width": size_arr[0], "height": size_arr[1]}

    @property
    def scroll_height(self):
        """
        get scroll height
        :return:
        """
        return self._get_window_properties(["document.documentElement.scrollHeight"])[0]

    @property
    def scroll_width(self):
        """
        get scroll width
        :return:
        """
        return self._get_window_properties(["document.documentElement.scrollWidth"])[0]

    @property
    def scroll_x(self):
        """
        获取窗口顶点与页面顶点的 x 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollX"])[0]

    @property
    def scroll_y(self):
        """
        获取窗口顶点与页面顶点的 y 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollY"])[0]

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

    def scroll_to(self, scroll_top, duration=300):
        """
        滚动到指定位置
        :param scroll_top:  位置 px
        :param duration:  滚动时长
        :return:
        """
        self.call_wx_method(
            "pageScrollTo", [{"scrollTop": scroll_top, "duration": duration}]
        )

    def _send(self, method, params=None):
        if params is None:
            params = {}
        params["pageId"] = self.page_id
        return self.connection.send(method, params)

    def _get_elements(self, selector, max_timeout=0) -> typing.List[BaseElement]:
        @timeout(max_timeout)
        def search_elements():
            elements = []
            ret = self._send("Page.getElements", {"selector": selector})
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
            self.logger.info("try to get elements: %s" % selector)
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

    def _element_is_exists(self, selector, max_timeout=10) -> bool:
        @timeout(max_timeout)
        def refresh_elements():
            ret = self._send("Page.getElements", {"selector": selector})
            if hasattr(ret, "error"):
                raise Exception(
                    "Element not found with selector: [%s], cause: %s"
                    % (selector, ret.error)
                )
            if len(ret.result.elements) > 0:
                return True

        try:
            self.logger.info("try to find elements: %s" % selector)
            rtn = refresh_elements()
            self.logger.info("element(%s) exists" % selector)
            # return rtn
            if not rtn:
                return False
            else:
                return True
        except Exception as e:
            self.logger.warning("element(%s) not exists" % selector)
            self.logger.error(e)
            return False

    # 正式支持xpath后，考虑复用get_element接口，通过检测selector类型来决定使用什么选择器
    # def _is_xpath(self, selector):
    #     """
    #     检测一个selector是否是xpath
    #     1. start with "/"
    #     2. start with "//"
    #     3. start with "./" or == "."
    #     4. translator.css_to_xpath(css_selector) fail
    #     """
    #     if selector.startswith("/") or selector.startswith("//") or selector.startswith("./"):
    #         return True
    #     if selector == ".":
    #         return True
    #     try:
    #         translator.css_to_xpath(selector)
    #         return False
    #     except SelectorError:
    #         return True
    #     return False

    def _get_element_by_xpath(self, xpath, max_timeout=10) -> BaseElement:
        @timeout(max_timeout)
        def search_element():
            ret = self._send("Page.getElementByXpath", {"selector": xpath})
            if hasattr(ret, "error"):
                raise Exception(
                    "Error when finding element[%s], %s" % (xpath, ret.error)
                )
            el = ret.result
            if "nodeId" in el.keys():
                return CustomElement(el, self.page_id, self.connection)
            else:
                return ELEMENT_TYPE.get(el.tagName, BaseElement)(
                    el, self.page_id, self.connection
                )

        try:
            self.logger.info("try to get elements: %s" % xpath)
            el = search_element()
            if not el:
                self.logger.warning(
                    f"Could not found any element '{xpath}' you need"
                )
            else:
                self.logger.info("find element success: %s" % str(el))
            return el
        except Exception as e:
            raise Exception("elements search fail cause: " + str(e))

    def get_element_by_xpath(self, xpath, max_timeout=10)-> BaseElement or VideoElement or AudioElement or \
         ViewElement or FormElement or LivePlayerElement or LivePusherElement:
        """
        根据xpath查找元素
        """
        return self._get_element_by_xpath(xpath, max_timeout)