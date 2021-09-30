import time

from base.base import Web
from selenium.webdriver.common.by import By
class Applyp(Web):
    titel = (By.XPATH, '*[@id="app"]/div[2]/h4')
    nameT = (By.XPATH, '*[@id="app"]/div[2]/div[1]/div[1]/div[1]')
    nameI = (By.XPATH, '//input[@placeholder="请输入委托人姓名"]')
    telephoneI = (By.ID, 'phone')
    vcodeI = (By.XPATH, '//input[@placeholder="请输入手机验证码"]')
    descI = (By.XPATH, '//input[@placeholder="请输入详细描述与说明"]')
    telephoneT = (By.XPATH, '//input[@placeholder="请输入手机验证码"]/../../../div[1]')
    vcodeT = (By.XPATH, '//input[@placeholder="请输入手机验证码"]/../../../div[1]')
    descT = (By.XPATH, '//input[@placeholder="请输入详细描述与说明"]/../../../div[1]')
    sendB = (By.XPATH, '//span[text()="发送验证码"]')
    selectFB = (By.XPATH, '//span[text()=" 选择文件 "]')
    file = (By.XPATH, '//div[text()=" 只能上传JPG/PNG/PDF/PPT/DOC/RAR/ZIP格式的文件，且不超过5MB "]')
    selectB = (By.XPATH, '//span[text()="我同意并遵守"]/../div[1]/img')
    privacyL = (By.XPATH, '//span[text()="《委托拍卖规则》"]')
    commitB = (By.XPATH, '//span[text()="提交"]')
    def get_apply_tel_lenth(self):
        '''手机输入框的最大长度'''
        return self.driver.find_element(*self.telephoneI).get_attribute("maxlength")
    def get_apply_nameT(self):
        '''姓名'''
        return self.driver.find_element(*self.nameT).text()
    def get_apply_telephoneT(self):
        '''手机号'''
        return self.driver.find_element(*self.telephoneT).text()

    def get_apply_vcodeT(self):
        '''验证码'''
        return self.driver.find_element(*self.vcodeT).text()
    def get_apply_descT(self):
        '''内容描述'''
        return self.driver.find_element(*self.descT).text()
    def get_apply_telephoneT(self):
        '''手机号'''
        return self.driver.find_element(*self.telephoneT).text()
    def click_apply_selectB(self):
        '''点击 同意并遵守《委托拍卖原则》选择框'''
        self.driver.find_element(*self.selectB).click()
    def click_apply_sendB(self):
        '''点击 发送验证码'''
        self.driver.find_element(*self.sendB).click()
    def click_apply_commitB(self):
        '''点击 提交'''
        self.driver.find_element(*self.commitB).click()
    def send_apply_name(self,name):
        '''输入姓名'''
        self.driver.find_element(*self.nameI).send_keys(name)
    def send_apply_phone(self,phone):
        '''输入手机号码'''
        self.driver.find_element(*self.telephoneI).send_keys(phone)
    def send_apply_vcode(self,vcode):
        '''输入验证码'''
        self.driver.find_element(*self.vcodeI).send_keys(vcode)
    def create_apply(self, name, phone, vcode):
        '''创建一个委托申请'''
        self.send_apply_name(name)
        self.send_apply_phone(phone)
        self.click_apply_sendB()
        time.sleep(2)
        self.send_apply_vcode(vcode)
        time.sleep(1)
        self.click_apply_commitB()
        time.sleep(3)











