#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       interfacetest.py
Create time:    2019-09-12 11:32
Description:

"""

import minium


class InterfaceTest(minium.MiniTest):
    def test_api(self):
        """
        接口测试
        :return:
        """
        self.app.navigate_to("/page/API/pages/get-system-info/get-system-info")
        # 直接调用页面上的方法
        ret = self.page.call_method(method="onShareAppMessage", args=None)
        self.assertIn("title", ret.result.result, "Key 校验")

    def test_inject(self):
        """
        代码注入测试
        :return:
        """
        self.app.evaluate("""function (){
        wx.request({
            url: 'https://14592619.qcloud.la/testRequest',
            data: {
                noncestr: Date.now()
            },
            success(result) {
                console.log('request success', result)
            },
            fail({errMsg}) {
                console.log('request fail', errMsg)
            }
        })}"""
        )

    def test_log_check(self):
        """
        获取小程序的 log 并分析
        :return:
        """
        # 3. 分析 log
        def analysis_log(log):
            # 所有 log 的输出都会回调到这里
            # 可以检查是否是预期的输出
            print(log)

        # 1. 注册 log 监听
        self.app.add_observer("App.logAdded", analysis_log)

        # 2. 执行用例步骤
        self.app.navigate_to("/page/API/pages/get-system-info/get-system-info")
        self.page.call_method(method="onShareAppMessage", args=None)

    def test_custom_method_binding(self):
        """
        将回调绑定到自定义的方法里面
        :return:
        """
        # 1. 设置一个回调函数
        def feedback(res):
            print("Get feedback:", res)

        # 2. 将回调函数暴露给小程序
        self.app.expose_function("feedback", feedback)

        # 3. 跳转到某个页面
        self.app.navigate_to("/page/API/pages/request/request")

        # 4. 获取当前页面, 命名为 self
        # 5. 从页面中记录下需要绑定回调的函数 makeRequest ，命名为 oldMakeRequest
        # 6. 重写 makeRequest ，将回调的调用添加进去，实现绑定
        self.app.evaluate("""function (){
        self = this.getCurrentPages().slice(-1)[0]
        oldMakeRequest = self.makeRequest
        self.makeRequest = function(event){
            oldMakeRequest(event)
            feedback(event)
        }
        }""")

        # 7. 点击控件，触发控件绑定函数 makeRequest
        self.page.get_element("button").click()

        self.app.navigate_to("/page/API/pages/request/request")

        # 8. feedback() 接收到回调
        # Get feedback: {'name': 'feedback', 'args': [{'type': 'tap', 'timeStamp': 104245, 'target': {'id': '', 'offsetLeft': 16, 'offsetTop': 423, 'dataset': {}}, 'currentTarget': {'id': '', 'offsetLeft': 16, 'offsetTop': 423, 'dataset': {}}, 'mark': {}, 'detail': {'x': 207, 'y': 446}, 'touches': [{'pageX': 207, 'pageY': 446, 'force': 0}], 'changedTouches': []}]}
