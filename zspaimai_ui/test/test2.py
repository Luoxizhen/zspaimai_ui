import time
import sys
import os

from HtmlTestRunner import HTMLTestRunner

currrentPath = os.path.abspath(__file__)
rootPath = os.path.dirname(currrentPath)
zz = os.path.dirname(rootPath)
sys.path.append(zz)

from page.zslogin import Login
import unittest
from selenium import webdriver

from init import TestLoginInit, Init, Init2
from parameterized import parameterized,param




class TestLogin_003(Init2, Login):
    ''' 快捷登陆异常操作： 验证码错误'''
    @parameterized.expand([
        param("1", '15622145010', '123455', '短信验证码有误，请重新输入'),
        param("2" ,'15622145010', '', '请输入您的6位数验证码'),

    ])
    def test_login_error(self, phone, vc, msg):
        '''验证验证码输入错误或未输入时，进行登陆，错误信息提示准确'''
        self.click_loginL()
        self.click_loginTypeP()
        self.clear_phone()
        self.clear_vc()
        self.send_phone(phone)
        self.click_svcb()
        time.sleep(5)
        self.send_validCode(vc)
        self.click_lb()
        self.assertEqual(msg, self.get_loginMsg())
        self.close_loginbox()




if __name__ == '__main__':
    suite = unittest.TestSuite()  # 定义一个测试集合

    suite.addTests(unittest.makeSuite(TestLogin_003))  # 把写的用例加进来（将TestCalc类）加进来
    f = open('test.html', 'w')  # 以二进制模式打开一个文件
    runner = HTMLTestRunner(stream=f,
                            report_title="Testcase Report",
                            descriptions=u"测试用例明细",
                            verbosity=2)
    runner.run(suite)  # 运行用例（用例集合)
