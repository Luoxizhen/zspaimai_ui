import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



import time

from selenium import webdriver
from page.myApplyP import MyApplyp
from page.firstp import Firstp
from page.zslogin import Login
from page.applyp import Applyp
from base.browser_driver import select_browser
from base.webpage import SeleniumHelper
import test.init as init

# @pytest.fixture(scope='class',autouse=True)
# def start():
#     # path = '/usr/local/bin/chromedriver.exe'
#     global driver
#     driver = webdriver.Chrome()
#     driver.get("http://home.online.zspaimai.cn/")
# def test_001():
#     driver = webdriver.Chrome()
#     driver.get("http://home.online.zspaimai.cn/")
#     fp = Firstp(driver)
#     lp = Login(driver)
#
#     fp.click_loginB()
#     time.sleep(3)
#     lp.click_loginTypeNo()
#     lp.send_no('15622145010')
#     lp.send_pw('123456')
#     lp.click_lb()
class Test_Apply_001:


    def setup_class(self):
        self.driver = select_browser("chrome")
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://home.online.zspaimai.cn/")


    def teardown_class(self):
        self.driver.quit()

    def test_001(self):
        fp = Firstp(self.driver)
        lp = Login(self.driver)
        ap = Applyp(self.driver)

        fp.click_loginB()

        time.sleep(3)
        lp.login_num('15622145010', '123456')
        fp.click_myApplyB()
        self.switch_window()
        ap.create_apply('大罗', '15622145010', '123456')
        current_url = self.driver.current_url
        assert current_url == 'https://www.zsonline.cn/entrust'

    def switch_window(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])







