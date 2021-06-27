import time
import unittest

from HtmlTestRunner import HTMLTestRunner

from init import Init,Init3
from page.zslogin import Login
from page.firstp import Firstp
import unittest
from selenium import webdriver
from init import TestLoginInit
from parameterized import param,parameterized

class TestLogin_003(Init3,Firstp):
    def test_click_help(self):
        '''验证点击页面顶部 帮助中心 ，页面正确跳转'''
        self.click_helpB()
        self.assertEqual('中晟在线-帮助', self.driver.title)

    def test_click_contact(self):
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        self.click_contactB()
        self.assertEqual('中晟在线-联系我们', self.driver.title)

    def test_click_firstPage(self):
        '''验证点击页面中间导航栏 首页 ，页面正确跳转'''
        self.click_bid()
        self.click_firstPage()
        self.assertEqual("中晟在线", self.driver.title)

# if __name__ == '__main__':
#     unittest.main(verbosity=2)
if __name__ == '__main__':

    # suit = unittest.TestSuite()
    # suit.addTest(TestLogin_003('test_login_phone'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    suite = unittest.TestSuite()  # 定义一个测试集合

    suite.addTests(unittest.makeSuite(TestLogin_003))  # 把写的用例加进来（将TestCalc类）加进来
    f = open('test.html', 'w')  # 以二进制模式打开一个文件
    runner = HTMLTestRunner(stream=f,
                      report_title="Testcase Report",
                      descriptions=u"测试用例明细",
                            verbosity=2)
    runner.run(suite)  # 运行用例（用例集合)