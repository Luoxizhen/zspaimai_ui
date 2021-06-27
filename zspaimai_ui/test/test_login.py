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

from .init import TestLoginInit, Init, Init2
from parameterized import parameterized, param



class TestLogin_001(TestLoginInit, Login):
    '''账号登陆： 登陆框基本元素显示，限制等验证'''
    def test_001_click_loginTypeN(self):
        '''验证选中账号登陆时，账号登陆显示选中标识：下滑线'''
        self.click_loginTypeNo()
        self.assertEqual('0', self.get_loginTypeNo_tabindex())
        self.assertEqual('-1', self.get_loginTypeP_tabindex())
    def test_loginType(self):
        '''验证页面显示： 快捷登陆'''
        self.assertEqual("账号登录", self.get_loginTypeNo_text())
    def test_number_default(self):
        '''验证账号输入框的默认文本'''
        self.assertEqual('请输入账号', self.get_no_placeholder())
    def test_number_maxLength(self):
        '''验证账号输入框的限制长度为11'''
        self.assertEqual('11', self.get_no_maxLength())
    def test_password_default(self):
        '''验证密码输入框的默认文本'''
        self.assertEqual('请输入6位数字密码', self.get_password_placeholder())
    def test_password_maxLength(self):
        '''验证密码输入框的限制长度为6'''
        self.assertEqual('6', self.get_password_maxLength())
    def test_password_defaultType(self):
        '''验证密码输入框,输入密码，默认显示形式为小黑点 '''
        self.assertEqual('password', self.get_password_type())
    def test_number_sendLetter(self):
        '''验证账号无法输入非数字'''
        self.click_loginTypeNo()
        self.send_no('Aa我。')
        self.assertEqual(None, self.get_no_text())
    def test_password_sendLetter(self):
        '''验证手机号码无法输入非数字'''
        self.click_loginTypeNo()
        self.send_pw('Aa我。')
        self.assertEqual(None, self.get_pw_text())
    def test_number_subfix(self):
        '''验证账号有输入内容时，显示删除按钮'''
        self.clear_no()
        self.send_no('1')
        self.assertTrue(self.nmE())
    def test_password_subfix(self):
        '''验证密码有输入内容时，显示眼睛按钮'''
        self.clear_pw()
        self.send_pw('1')
        self.assertTrue(self.eyeE())
    def test_password_type001(self):
        '''验证密码框实际输入密码时，默认显示为小黑点'''
        self.clear_pw()
        self.send_pw('123456')
        self.assertEqual('password', self.get_pw_type())
    def test_password_type002(self):
        '''验证密码框输入密码后，点击眼睛按钮，显示为数字'''
        self.clear_pw()
        self.send_pw('123456')
        self.click_eye()
        self.assertEqual('text', self.get_pw_type())
    def test_password_type003(self):
        '''验证密码输入框输入密码后，点击眼睛按钮，显示为数字，切换到快捷登陆后再切换回账号登陆，密码显示为小黑点'''
        self.click_loginTypeP()
        self.click_loginTypeNo()
        self.assertEqual('password', self.get_pw_type())

class TestLogin_002(TestLoginInit,Login):
    '''快捷登陆: 登陆框基本元素显示、显示等验证'''
    def test_001_click_loginTypeP(self):
        '''验证选中快捷登陆时，快捷登陆显示选中标识：下滑线'''
        self.click_loginTypeNo()
        self.click_loginTypeP()
        self.assertEqual('-1', self.get_loginTypeNo_tabindex())
        self.assertEqual('0', self.get_loginTypeP_tabindex())
    def test_phone_default(self):
        '''验证手机号输入框的默认文本'''
        self.assertEqual('请输入手机号（未注册手机号验证自动注册）', self.get_phone_placeholder())
    def test_phone_maxLength(self):
        '''验证手机号输入框的限制长度为11'''
        self.assertEqual('11', self.get_phone_maxLength())
    def test_validCode_default(self):
        '''验证验证码输入框的默认文本'''
        self.assertEqual('输入验证码', self.get_validCode_placeholder())
    def test_validCode_maxLength(self):
        '''验证验证码输入框的限制长度为6'''
        self.assertEqual('6', self.get_validCode_maxLength())
    def test_loginTitle(self):
        '''验证登陆框标题显示准确 ： 中晟在线'''
        self.assertEqual("中晟在线", self.get_loginTitle())

    def test_loginType(self):
        '''验证页面显示： 账号登陆'''
        self.assertEqual("快捷登录", self.get_loginTypeP_text())
    unittest.skip('未确定默认登陆方式')
    def test_loginType_default(self):
        '''验证默认的登陆方式为快捷登陆'''
        self.assertEqual('-1', self.get_loginTypeNo_tabindex())
        self.assertEqual('0', self.get_loginTypeP_tabindex())
    def test_sendVcButton_default(self):
        '''验证发送验证码按钮的默认标签为 ： 发送验证码'''
        self.assertEqual('发送验证码', self.get_svcb_text())

    def test_validCode_sendLetter(self):
        '''验证 验证码无法输入非数字'''
        self.send_validCode('Aa我。')
        self.assertEqual(None, self.get_vc_text())

    def test_phone_sendLetter(self):
        '''验证手机号码无法输入非数字'''
        self.send_phone('Aa我。')
        self.assertEqual(None, self.get_phone_text())
    @unittest.skip('获取输入框文本的方法未确定')
    def test_phone_sendLetter12(self):
        '''验证手机号码输入12位数字，只保留11位'''
        self.send_phone('123456789012')
        #self.assertEqual('12345678901', self.get_phone_text())
    def test_phone_subfix(self):
        '''验证手机号码有输入内容时，文本框显示删除按钮'''
        self.clear_phone()
        self.send_phone('1')
        self.assertTrue(self.delE())
    def test_vc_subfix(self):
        '''验证验证码有输入内容时，文本框显示删除按钮'''
        self.clear_vc()
        self.send_validCode('1')
        self.assertTrue(self.delE())


class TestLogin_003(Init2, Login):
    '''发送验证码基本功能验证'''
    def setUp(self) -> None:
        self.click_loginL()
        self.click_loginTypeP()
    def tearDown(self) -> None:
        time.sleep(5)
        self.close_loginbox()

    def test_001(self):
        '''验证未填写手机号码，点击 发送验证码 按钮有错误信息提示，提示内容为 请输入您的手机号'''
        self.phE().clear()
        self.click_svcb()
        self.assertIsNotNone(self.tiE())
        self.assertIsNotNone(self.tmE())
        self.assertEqual('请输入您的手机号', self.get_tipMsg())
    def test_002(self):
        '''验证手机号码不规范时，点击 发送验证码 按钮有错误信息提示，提示内容为 请输入有效的手机号'''
        time.sleep(5)
        self.phE().clear()
        self.send_phone('11345678901')
        self.click_svcb()
        self.assertIsNotNone(self.tiE())
        self.assertIsNotNone(self.tmE())
        self.assertEqual('请输入有效的手机号', self.get_tipMsg())
    def test_003(self):
        '''验证手机号码规范时，点击 发送验证码
        1、按钮有已发送信息提示，提示内容为 发送成功，请注意查收验证码，
        2、发送验证码文本显示为 多少秒后重新发送，
        3、此时无法操作按钮
        4、等待60s 后 ，可以操作按钮'''
        self.phE().clear()
        self.send_phone('15622145010')
        self.click_svcb()
        self.assertIsNotNone(self.tiE())
        self.assertIsNotNone(self.tmE())
        time.sleep(2)
        self.assertEqual('发送成功，请注意查收验证码', self.get_tipMsg())
        self.assertIn('s后重新发送', self.get_svcb_text())
        self.assertFalse(self.get_sendButton_enabled())
        time.sleep(60)
        self.assertTrue(self.get_sendButton_enabled())
        self.assertEqual('发送验证码', self.get_svcb_text())

class TestLogin_004(Init2, Login):
    '''快捷登陆异常功能1 验证'''
    def setUp(self) -> None:
        self.click_loginL()
        self.click_loginTypeP()
    def tearDown(self) -> None:
        time.sleep(5)
        self.close_loginbox()

    @unittest.skip('005 已包含')
    def test_001(self):
        '''验证手机号码及验证码为空，无法登陆，并提示错误信息： 请输入有效的手机号'''
        self.clear_phone()
        self.clear_vc()
        self.click_lb()
        self.assertEqual('请输入有效的手机号', self.get_tipMsg())
    def test_002(self):
        '''验证验证码失效，无法登陆，提示错误信息： 短信验证码失效，请重新获取'''
        self.send_phone('15622145010')
        self.click_svcb()
        time.sleep(5)
        self.send_validCode('123456')
        self.send_phone('15622145011')
        self.click_lb()
        self.assertEqual('短信验证码失效，请重新获取', self.get_loginMsg())

    @unittest.skip('005 已包含')
    def test_003(self):
        '''验证未获取验证码，无法登陆，并提示错误信息：短信验证码失效，请重新获取'''
        self.send_phone('15622145012')
        self.send_validCode('123456')
        self.click_lb()
        self.assertEqual('短信验证码失效，请重新获取', self.get_loginMsg())

    @unittest.skip('005 已包含')
    def test_004(self):
        '''验证未输入验证码，无法登陆，并提示错误信息：请输入您的6位数验证码'''
        self.send_phone('15622145012')
        self.click_lb()
        self.assertEqual('请输入您的6位数验证码', self.get_loginMsg())
    @unittest.skip('005 已包含')
    def test_005(self):
        '''验证未输入手机号，无法登陆，并提示错误信息：请输入您的手机号'''
        self.send_validCode('123456')
        self.click_lb()
        self.assertEqual('请输入您的手机号', self.get_loginMsg())
    def test_006(self):
        '''验证验证码错误，无法登陆，并提示错误信息：短信验证码有误，请重新输入'''
        self.send_phone('15622145010')
        self.click_svcb()
        self.send_validCode('111111')
        time.sleep(5)
        self.click_lb()
        self.assertEqual('短信验证码有误，请重新输入', self.get_loginMsg())



class TestLogin_005(Init2, Login):
    '''快捷登陆异常功能2： 不发送验证码的异常登陆 验证'''
    def setUp(self) -> None:
        self.click_loginL()
        self.click_loginTypeP()
    def tearDown(self) -> None:
        time.sleep(5)
        self.close_loginbox()
    @parameterized.expand([
        param('15622145010', '123455', '短信验证码失效，请重新获取'),
        param('15622145010', '123456', '短信验证码失效，请重新获取'),
        param('15622145010', '', '请输入您的6位数验证码'),
        param('', '', '请输入有效的手机号'),
        param('', '123456', '请输入您的手机号'),

    ])
    def test_login_error_phone(self, phone, vc, msg):

        self.clear_phone()
        self.clear_vc()
        self.send_phone(phone)
        # self.click_svcb()
        # time.sleep(9)
        self.send_validCode(vc)
        self.click_lb()
        time.sleep(1)
        self.assertEqual(msg, self.get_tipMsg())

@unittest.skip('用例异常')
class TestLogin_003(Init2, Login):
    ''' 快捷登陆异常操作： 验证码错误'''
    @parameterized.expand([
        param('varid code error', '15622145010', '123455', '短信验证码有误，请重新输入'),
        param('varid code null', '15622145010', '', '请输入您的6位数验证码'),

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

class TestLogin_006(Init2, Login):
    '''账号密码 异常登陆功能验证'''
    def setUp(self) -> None:
        self.click_loginL()
        self.click_loginTypeNo()
    def tearDown(self) -> None:
        time.sleep(5)
        self.close_loginbox()
    @parameterized.expand([
        param('账号、密码为空', '', '', '请输入您的手机号'),
        param('账号为空', '', '123456', '请输入您的手机号'),
        param('密码为空', '15622145010', '', '请输入您的6位数验证码'),
        param('手机号无效', '11111111111', '123456', '请输入有效的手机号'),
        param('密码错误', '15622145010', '111111', '密码有误，可尝试微信登陆/快捷登陆'),
        param('密码长度错误', '15622145010', '11111', '请输入您的6位数密码'),
    ])
    def test_login_error_no(self, no, pw, msg):
        self.send_no(no)
        self.send_pw(pw)
        self.click_lb()
        self.assertEqual(msg, self.get_loginMsg())
@unittest.skip('未实现')
class TestLogin_007(Init2, Login):
    '''微信登陆功能验证'''
    def test_001(self):
        '''验证点击微信图标，弹出微信登陆框'''
        self.click_loginL()
        self.click_weChat()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.assertTrue(self.get_weCharTitle())
    def test_002(self):
        '''验证显示二维码'''
        self.assertTrue(self.get_weCharImg())
    def test_003(self):
        '''验证页面显示 ：请使用微信扫描二维码登录'''
        data = self.driver.find_elements_by_xpath("/*")
        self.assertIn('请使用微信扫描二维码登录', data)
    def test_004(self):
        '''验证页面显示 ：请使用微信扫描二维码登录'''
        data = self.driver.find_elements_by_xpath("/*")
        self.assertIn('中晟在线', data)
    def test_005(self):
        '''验证点击其他登陆方式，页面正确跳转'''
        self.click_otherL()
        self.driver.switch_to('main')
        self.assertTrue(self.getLoginButton())
    def test_006(self):
        '''验证点击微信登陆框的关闭，页面正确跳转'''
        self.click_otherL()
        self.driver.switch_to('main')
        self.assertTrue(self.getLoginButton())


class TestLogin_008(Init2, Login):
    '''验证注册功能'''
    def test_001(self):
        '''验证从登陆框可以进入注册框'''
        self



if __name__ == '__main__':
    unittest.main(verbosity=2)
    # suit = unittest.TestSuite()
    # suit.addTest(TestLogin_003('test_login_phone'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    suite = unittest.TestSuite()  # 定义一个测试集合
    suite.addTest(unittest.makeSuite(TestLogin_001,TestLogin_002,TestLogin_003))  # 把写的用例加进来（将TestCalc类）加进来
    f = open('report/test.html', 'wb')  # 以二进制模式打开一个文件
    runner = HTMLTestRunner.HTMLTestRunner(f, title='unittest用例标题', description='这是用例描述')
    runner.run(suite)  # 运行用例（用例集合)