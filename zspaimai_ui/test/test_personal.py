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
        self.fp.login_num_password()
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
    def test_go_to_page(self):
        self.pp.go_to_page("个人中心")
        title = self.driver.title
        assert title == "中晟在线-个人中心"
        self.pp.go_to_page("我的竞买")
        title = self.driver.title
        assert title == "中晟在线-个人中心-我的竞买"
        self.pp.go_to_page("我的订单")
        title = self.driver.title
        assert title == "中晟在线-个人中心-我的订单"
        self.pp.go_to_page("我的委托")
        title = self.driver.title
        assert title == "中晟在线-个人中心-我的委托"
        self.pp.go_to_page("收货地址")
        title = self.driver.title
        assert title == "中晟在线-个人中心-收货地址"
        self.pp.go_to_page("推广计划")
        title = self.driver.title
        assert title == "中晟在线-个人中心-推广计划"
        self.pp.go_to_page("关注")
        title = self.driver.title
        assert title == "中晟在线-个人中心-关注"
        self.pp.go_to_page("财务")
        title = self.driver.title
        assert title == "中晟在线-个人中心-财务"
        self.pp.go_to_page("优惠")
        title = self.driver.title
        assert title == "中晟在线-个人中心-优惠"
        self.pp.go_to_page("设置")
        title = self.driver.title
        assert title == "中晟在线-个人中心-个人设置"

    def test_my_order_of_good3(self):
        self.pp.go_to_page("我的订单")
        info = self.pp.order_info()
        assert info == {"price":"￥1,000.00", "num":"1", "total_money":"￥1,100.00/n(含实际服务费￥100.00)","pay_time":"下单时间：2021-12-02 11:09:12","order_num":"订单编号：2021120211091203917"}


