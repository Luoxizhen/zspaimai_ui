# encoding:utf-8

import minium


class MockTest(minium.MiniTest):
    def test_mock_location(self):
        self.app.navigate_to("/page/API/pages/get-location/get-location")

        # 模拟武汉光谷位置
        mock_location = {
            "latitude": 30.5078502719,
            "longitude": 114.4191741943,
            "speed": -1,
            "accuracy": 65,
            "verticalAccuracy": 65,
            "horizontalAccuracy": 65,
            "errMsg": "getLocation:ok",
        }
        self.app.mock_wx_method("getLocation", mock_location)

        # 检查mock数据
        self.page.get_element("button", inner_text="获取位置").click()
        self.native.allow_get_location()
        locations = self.page.get_element(".page-body-text-location").get_elements(
            "text"
        )
        self.assertEqual(locations[0].inner_text, "E: 114°42′", "经度校验")
        self.assertEqual(locations[1].inner_text, "N: 30°51′", "纬度校验")

        # 去掉mock
        self.app.restore_wx_method("getLocation")
        self.page.get_element("button", inner_text="获取位置").click()
        self.native.allow_get_location()
        locations = self.page.get_element(".page-body-text-location").get_elements(
            "text"
        )
        self.assertNotEqual(locations[0].inner_text, "E: 114°42′", "经度校验")
        self.assertNotEqual(locations[1].inner_text, "N: 30°51′", "纬度校验")


    def test_mock_request(self):
        """
        模拟网络请求返回结果
        :return:
        """
        response = "{'rtn': 0, 'msg': 'OK'}"
        # 设置 mock 网络请求结果
        self.app.mock_wx_method("request", result=response, success=True)

        # 注入代码发起请求
        self.app.evaluate(
            """function (){
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

        # 恢复对 request 的 mock
        self.app.restore_wx_method("request")

    def test_mock_show_modal(self):
        self.app.mock_wx_method("showModal", result={"confirm": True, "errMsg": "showModal:ok"})
        self.app.navigate_to("/page/API/pages/modal/modal")
        self.page.get_element("button").click()
