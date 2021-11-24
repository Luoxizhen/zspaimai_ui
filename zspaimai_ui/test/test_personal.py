from page.firstp import Firstp
from page.personal import Personal
from selenium import webdriver
from common.readconfig import ini
from common.readpagedata import Pagedata
personal_data = Pagedata('personal')
import pytest
class TestPersonalInfo:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        self.fp = Firstp(self.driver)
        self.fp.click_login()
        self.fp.click_num_login()
        self.fp.send_num("15622145010")
        self.fp.send_password('123456')
        self.fp.click_login_botton()
        self.fp.click_nickname()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.pp = Personal(self.driver)

    def teardown_class(self):
        self.driver.quit()
    def test_nickname(self):
        nickname = self.pp.nickname().removeprefix("昵称：")
        personal_data.setitem_c("info", "nickname", nickname)
        #assert nickname == "昵称：hello world"
    def test_money(self):
        money = self.pp.money().removeprefix("￥")
        personal_data.setitem_c("info", 'money', money)
    def test_quota(self):
        quota = self.pp.quota()
        personal_data.setitem_c("info", 'quota', quota)
    def test_userno(self):
        userno = self.pp.userno().removeprefix("用户编码：")
        personal_data.setitem_c("info", "userno", userno)
