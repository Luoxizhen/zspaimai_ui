#!/usr/bin/env python3
# Created by xiazeng on 2019-06-26
import minium


class ErrorTest(minium.MiniTest):
    def test_assert_failed(self):
        """
        测试assert异常
        """
        self.assertIsInstance(self.page.query, dict)
        # 这里会报错
        self.assertEqual(self.page.path, "page/component/index")

    def test_error_failed(self):
        """
        会引起异常: AttributeError: 'NoneType' object has no attribute 'click'
        """
        # self.mini.call_wx_method("getLaunchOptionsSync")
        self.page.get_element("sunny").click()
