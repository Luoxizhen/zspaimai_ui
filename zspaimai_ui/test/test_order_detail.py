from page.firstp import Firstp
from page.mybid import MyBid
from page.order_detail import OrderDetail
from common.readconfig import ini
from selenium import webdriver
import pytest
class TestOrderDetail:
    '''验证订单详情页信息'''
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get(ini.url)
        self.driver.maximize_window()
        self.fp = Firstp(self.driver)
        self.fp.login_num_password()
        self.fp.click_my_bid_button()
        self.mb = MyBid(self.driver)
        self.mb.go_to_pay()
        self.od = OrderDetail(self.driver)
    def teardown_class(self):
        self.driver.quit()
    def test_good_info(self):
        good_info = self.od.good_info()
        assert good_info == {"name":"拍品1","pay_money":'￥225.5\n(含服务费￥20.50)',"service":"(含服务费￥20.50)"}
