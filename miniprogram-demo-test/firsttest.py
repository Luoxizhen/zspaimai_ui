#!/usr/bin/env python3

import minium


class FirstTest(minium.MiniTest):
    def test_get_system_info(self):
        sys_info = self.app.call_wx_method("getSystemInfo")
        self.assertIn("SDKVersion", sys_info.result.result)
