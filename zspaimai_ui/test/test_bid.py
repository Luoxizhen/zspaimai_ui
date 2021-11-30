
from page.bid import Bid
from page.firstp import Firstp
from selenium import webdriver
from common.readconfig import ini
from common.readpagedata import Pagedata
class TestBid:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        fp = Firstp(self.driver)
        fp.click_bidding()
        self.bp = Bid(self.driver)
    def teardown_class(self):
        self.driver.quit()
    def test_001(self):
        name = self.bp.good_name()
        status = self.bp.good_status()
        price = self.bp.good_price()
        good = {"name": name, "status": status, "price": price}
        bid_page_data = Pagedata("bid")
        bid_page_data.setitem("good_info", good)
    def test_002(self):
        self.bp.bid()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "http://home.online.zspaimai.cn/auction/detail?id=" in self.driver.current_url
    def test_003(self):
        fp = Firstp(self.driver)
        assert fp.is_display_login_box() == 1






