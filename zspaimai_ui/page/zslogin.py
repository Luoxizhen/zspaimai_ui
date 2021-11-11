from typing import Tuple

from base.webpage import Web

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
class Login(Web):
    loginL = (By.XPATH, '//div[text()="未登录"]')
    loginBox = (By.XPATH, '//div[@class="login-box"]')
    loginTitle = (By.XPATH, '//div[@class="login-title"]')
    loginTypeOfPhone = (By.ID, 'tab-phone')
    loginTypeOfUsernum = (By.ID, 'tab-usernum')
    # 快捷登陆，手机号码输入框
    phone = (By.XPATH, '//div[@class="login-input"]/div[1]/input')
    # 短信验证码输入框
    validCode = (By.XPATH, '//div[@class="login-input"]/div[2]/div[1]/input')
    # 发送验证码按钮
    elButton = (By.XPATH, '//div[@class="login-input"]/div[2]/button/span')
    sendVcButton = (By.XPATH, '//div[@class="login-input"]/div[2]/button')
    # 登陆按钮
    loginButton = (By.XPATH, '//div[@class="login-footer"]/button/span')
    # 账号输入框
    no = (By.XPATH, '//div[@class="login-input"]/div[1]/input')
    # 密码输入框
    password = (By.XPATH, '//div[@class="login-input"]/div[2]/input')
    # 注册按钮
    register = (By.XPATH, '//div[text()="注册"')
    # 微信登陆按钮
    weChat = (By.XPATH, '//div[@class="login-box-content"]/div[6]/img')

    # 登陆框关闭按钮
    loginClose = (By.XPATH, '//img[@class="login-title-close"]')
    # 获取账号输入框默认文本
    '''密码输入框眼睛按钮'''
    eye = (By.TAG_NAME, 'i')
    '''账号输入框的删除按钮'''
    textDel = (By.XPATH, '//span[@class="el-input__suffix"]')
    tipsIcon = (By.XPATH, '//div[contains(@id,"message")]/i')
    tipsMsg = (By.XPATH, '//div[contains(@id,"message")]/p')
    tipsMsgContains = (By.XPATH, '//div[contains(@id,"message")]')
    '''微信登陆框的标题'''
    weChatTitle = (By.XPATH, '//div[text()="微信登陆"]')
    '''微信登陆图片'''
    weChatImg = (By.XPATH, '//div[text()="微信登陆"]/../div[2]/div[1]/img')
    '''请使用微信扫描二维码登录'''
    weChatTip1 = (By.XPATH, '//div[text()="微信登陆"]/../div[2]/div[2]/div/p[1]')
    weChatTip2 = (By.XPATH, '//div[text()="微信登陆"]/../div[2]/div[2]/div/p[2]')
    '''其他登陆方式'''
    otherL = (By.XPATH, '//div[text()="其他登陆方式"]')

    '''注册框的元素定位: 注册标签'''
    registerTab = (By.ID, 'tab-register')
    '''手机号输入框'''
    registerInput = (By.TAG_NAME, 'input')
    '''注册按钮'''
    registerButton = (By.TAG_NAME, 'Button')
    '''我同意并遵守选择框'''
    agreeCheck = (By.XPATH, '//div[@id="login_container"]/../div[5]/div[2]/div/div/img')


    





    def phE(self):
        '''手机号码输入框元素'''
        return self.driver.find_element(*self.phone)
    def click_phone(self):
        self.phE().click()
    def pwE(self):
        '''密码输入框元素'''
        return self.driver.find_element(*self.password)
    def nmE(self):
        return self.driver.find_element(*self.no)
    def vcE(self):
        return self.driver.find_element(*self.validCode)
    def eyeE(self):
        return self.driver.find_element(*self.eye)
    def delE(self):
        return self.driver.find_element(*self.textDel)
    def ltpE(self):
        return self.driver.find_element(*self.loginTypeOfPhone)
    def ltnE(self):
        return self.driver.find_element(*self.loginTypeOfUsernum)
    def tiE(self):
        return self.driver.find_element(*self.tipsIcon)
    def tmE(self):
        return self.driver.find_element(*self.tipsMsg)
    def svcbE(self):
        return self.driver.find_element(*self.elButton)
    def sendE(self):
        return self.driver.find_element(*self.sendVcButton)
    def lbE(self):
        return self.driver.find_element(*self.loginButton)
    def loginLE(self):
        return self.driver.find_element(*self.loginL)
    def closeLbE(self):
        return self.driver.find_element(*self.loginClose)
    def weCharImgE(self):
        return self.driver.find_element(*self.weChatImg)
    def weChatTitleE(self):
        return self.driver.find_element(*self.weChatTitle)
    def weCharTip1E(self):
        return self.driver.find_element(*self.weChatTip1)

    def weCharTip2E(self):
        return self.driver.find_element(*self.weChatTip2)







    def get_no_placeholder(self):
        return self.nmE().get_attribute("placeholder")
    # 获取账号输入框限制长度
    def get_no_maxLength(self):
        return self.nmE().get_attribute("maxlength")

    # 获取密码输入框默认文本
    def get_password_placeholder(self):
        return self.pwE().get_attribute("placeholder")

    # 获取密码输入框限制长度
    def get_password_maxLength(self):
        return self.pwE().get_attribute("maxlength")

    # 获取手机号码输入框默认文本
    def get_phone_placeholder(self):
        return self.phE().get_attribute("placeholder")

    # 获取手机号码输入框限制长度
    def get_phone_maxLength(self):
        return self.phE().get_attribute("maxlength")

    # 获取验证码输入框默认文本
    def get_validCode_placeholder(self):
        return self.vcE().get_attribute("placeholder")

    # 获取验证码输入框限制长度
    def get_validCode_maxLength(self):
        return self.vcE().get_attribute("maxlength")

    

    def get_loginTitle(self):
        return self.driver.find_element(*self.loginTitle).text

    def get_loginTypeP_text(self):
        return self.ltpE().text
    def get_loginTypeNo_text(self):
        return self.ltnE().text
    def get_loginTypeP_tabindex(self):
        '''获取登陆方式选择属性'''
        return self.ltpE().get_attribute("tabindex")
    def get_loginTypeNo_tabindex(self):
        '''获取登陆方式选择属性'''
        return self.ltnE().get_attribute("tabindex")
    def click_loginTypeP(self):
        '''点击快捷登陆'''
        self.ltpE().click()
    def click_loginTypeNo(self):
        '''点击账号登陆'''
        self.ltnE().click()
    def send_no(self,nb):
        '''账号框输入信息'''
        self.nmE().send_keys(nb)
    def send_pw(self,pw):
        '''密码输入款输入信息'''
        self.pwE().send_keys(pw)
    def send_phone(self,pn):
        '''手机号码框输入信息'''
        self.phE().send_keys(pn)
    def send_validCode(self,vc):
        '''密码输入款输入信息'''
        self.vcE().send_keys(vc)
    def get_password_type(self):
        '''获取密码输入框文本属性'''
        return self.pwE().get_attribute('type')
    def click_eye(self):
        '''点击眼睛按钮'''
        self.eyeE().click()
    def click_del(self):
        '''点击文本框删除按钮'''
        self.delE().click()
    def get_no_text(self):
        '''获取账号输入框输入内容'''
        self.nmE().get_attribute('value')
    def get_pw_text(self):
        '''获取密码输入框输入内容'''
        self.pwE().get_attribute('value')
    def get_phone_text(self):
        '''获取电话输入框输入内容'''
        self.phE().get_attribute('oninput')
    def get_vc_text(self):
        '''获取验证码输入框输入内容'''
        self.vcE().get_attribute('value')
    def get_pw_type(self):
        '''获取密码文本属性'''
        return self.pwE().get_attribute('type')
    def get_tipMsg(self):
        '''获取提示信息'''
        return self.tmE().text
    def click_svcb(self):
        '''点击发送验证码按钮'''
        self.svcbE().click()
    def get_svcb_text(self):
        '''获取发送验证码按钮的标签'''
        return self.svcbE().text
    def get_sendButton_enabled(self):
        '''获取发送验证码按钮的可交互性'''
        return self.sendE().is_enabled()
    def clear_phone(self):
        '''删除电话号码'''
        self.phE().clear()
    def clear_vc(self):
        '''删除验证码'''
        self.vcE().clear()
    def clear_no(self):
        self.nmE().clear()
    def clear_pw(self):
        self.pwE().clear()
    def click_lb(self):
        self.lbE().click()

    def click_loginL(self):
        self.loginLE().click()
    def get_loginMsg(self):
        return self.findElements(*self.tipsMsgContains)[-1].find_element(By.TAG_NAME, 'p').text
    def close_loginbox(self):
        self.closeLbE().click()
    def click_weChat(self):
        self.findElement(*self.weChat).click()
    def get_weCharTitle(self):
        return self.weChatTitleE().is_displayed()
    def get_weCharImg(self):
        return self.weCharImgE().is_displayed()

    def get_weCharTip1(self):
        return self.weCharTip1E().get_attribute('textContent')
    def get_weCharTip2(self):
        return self.weCharTip2E().get_attribute('textContent')
    def click_otherL(self):
        self.driver.find_element(*self.otherL).click()
    def getLoginButton(self):
        return self.lbE().is_display()
    def login_num(self, num, pw):
        self.click_loginTypeNo()
        time.sleep(3)
        self.send_no(num)
        self.send_pw(pw)
        time.sleep(2)
        self.click_lb()
        time.sleep(3)











