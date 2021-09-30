#!/usr/bin/env python3
# Created by xiazeng on 2019-06-03
import time
import minium


class ComponentTest(minium.MiniTest):
    def test_set_data(self):
        self.app.navigate_to("/page/component/pages/text/text")
        self.page.data = {"text": "只能加文字，不能删除文字", "canAdd": True, "canRemove": False}
        time.sleep(1)
        self.capture("canAdd")
        self.page.data = {"text": "只能删除文字，不能加文字", "canAdd": False, "canRemove": True}
        time.sleep(1)
        self.capture("canRemove")

    def test_ui_op(self):
        self.page.get_element("view", inner_text="视图容器").click()
        self.page.get_element(".navigator-text", inner_text="swiper").click()
        self.capture("swiper")
        self.page.get_elements("switch")[0].click()
        self.page.get_elements("switch")[1].click()

    def test_input_element(self):
        self.app.navigate_to("pages/input/input")
        es = self.page.get_elements(".weui-input")
        # 直接触发事件，但是不会影响UI变化
        es[2].trigger("input", {"value": "测试以惺惺相惜"})

    def test_slider(self):
        self.app.navigate_to("pages/slider/slider")
        e = self.page.get_element("slider")
        e.trigger("change", {"value": 10})
        e.trigger("change", {"value": 30})
        e.trigger("change", {"value": 80})
