#!/usr/bin/env python3
# Created by xiazeng on 2019-06-20

import minium


class NativeTest(minium.MiniTest):
    def test_action_sheet(self):
        """
        操作原生action_sheet
        """
        self.app.navigate_to("/page/API/pages/action-sheet/action-sheet")
        self.page.get_element("button").click()
        self.native.handle_action_sheet("item1")

    def test_modal(self):
        """
        操作原生modal实例
        """
        self.app.navigate_to("/page/API/pages/modal/modal")
        self.page.get_element("button", inner_text="有标题的modal").click()
        self.capture("有标题的modal")
        self.native.handle_modal("确定")
        self.page.get_element("button", inner_text="无标题的modal").click()
        self.capture("无标题的modal")
        self.native.handle_modal("取消")

    def test_authorize_setting_page(self):
        """
        小程序授权设置页面操作
        """
        # todo: iOS尚未支持
        self.app.navigate_to("/page/API/pages/setting/setting")
        self.page.get_element("button", inner_text="打开小程序设置").click()
        self.capture("小程序授权设置-之前")
        self.native.authorize_page_checkbox_enable("摄像头", False)
        self.native.authorize_page_checkbox_enable("用户信息", True)
        self.capture("小程序授权设置-之后")
        authorize_setting = self.native.get_authorize_settings()
        self.assertFalse(authorize_setting["摄像头"], "摄像头权限")
        self.assertTrue(authorize_setting["用户信息"], "用户信息权限")
        self.native.back_from_authorize_setting()

    def test_authorize(self):
        """
        辅助点击授权
        """
        self.app.navigate_to("/page/API/pages/get-user-info/get-user-info")
        self.page.get_element("button", inner_text="获取用户信息").click()
        self.native.allow_get_user_info(False)
        self.page.get_element("button", inner_text="获取用户信息").click()
        self.native.allow_get_user_info(True)
        ret = self.page.wait_data_contains(["userInfo", "nickName"])
        self.assertTrue(ret, "获取个人信息")

    def test_forward(self):
        """
        转发小程序示例
        """
        # 从右上角菜单中转发 文件传输小助手 是微信上的联系人昵称
        self.app.navigate_to("/page/API/pages/share/share")
        self.native.forward_miniprogram("反馈跟进", "转发发送的文字")

        # 小程序内部调用转发方法 aauisendmsg是微信上的联系人昵称
        self.app.navigate_to("/page/API/pages/share-button/share-button")
        self.page.get_element(".button-share").click()
        self.native.forward_miniprogram_inside("反馈跟进", "转发发送的文字")

    def test_input(self):
        """
        input 标签输入
        :return:
        """
        self.app.navigate_to("/page/component/pages/input/input")
        self.page.get_elements("input.weui-input")[3].click()
        self.native.input_text("hi, sherlock")
