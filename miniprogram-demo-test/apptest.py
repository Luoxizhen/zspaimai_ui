#!/usr/bin/env python3
# Created by xiazeng on 2019-05-06
import minium


class AppTest(minium.MiniTest):
    def test_call_wx_method(self):
        """
        测试call_wx_method
        """
        sys_info = self.app.call_wx_method("getSystemInfo")
        self.assertIn("SDKVersion", sys_info.result.result)

    def test_get_current_page(self):
        self.assertEqual(self.page.path, "page/component/index")  # 有错误，报告会把这行代码标红
        self.assertIsInstance(self.page.query, dict)

    def test_switch_bar(self):
        """
        测试switch_tab
        """
        self.app.switch_tab("/page/API/index")
        self.app.switch_tab("/page/cloud/index")
        self.app.switch_tab("/page/component/index")
