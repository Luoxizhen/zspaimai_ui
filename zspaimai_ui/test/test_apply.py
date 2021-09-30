import time
import unittest
from selenium import webdriver
from page.applyp import Applyp
import test.init as init




class TestApply001(init.TestApplyInit001, Applyp):
    def test_apply_000(self):
        self.switch_window()
        self.send_apply_name('大罗')
        self.send_apply_phone('15622145010')
        self.click_apply_sendB()
        self.send_apply_vcode('123456')
        time.sleep(3)
        self.click_apply_commitB()
        time.sleep(3)
        self.switch_window()
        self.assertEqual("http://home.online.zspaimai.cn/entrust", self.driver.current_url)
        

    def test_apply_001(self):
        self.click_apply_commitB()










