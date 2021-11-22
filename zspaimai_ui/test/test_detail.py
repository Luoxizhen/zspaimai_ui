import time

from page.detailp import Detail
from common.readconfig import ini
from selenium import webdriver
from page.firstp import Firstp
from common.readpagedata import Pagedata
good_info = Pagedata('firstp')['goods']['good1']
class TestCollectionInfo:
    '''验证拍品基本信息'''
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        fp = Firstp(self.driver)
        fp.click_collection_detail()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        dp = Detail(self.driver)
        if dp.is_diplayed_loginbox()==1:
            dp.click_close_login()



    def teardown_class(self):
        self.driver.quit()

    def test_name(self):
        dp = Detail(self.driver)
        assert dp.collection_name() == good_info['name']
    def test_start_time(self):
        dp = Detail(self.driver)
        assert dp.start_time() == good_info['begin_time']

    def test_end_time(self):
        dp = Detail(self.driver)
        assert dp.start_time() == good_info['end_time']

    def test_status(self):
        dp = Detail(self.driver)
        assert dp.collection_status() == "正在拍卖"
    def test_price(self):
        dp = Detail(self.driver)
        assert dp.collection_price() == "￥"+str(good_info['price'])+".00"
    def test_bid_price(self):
        dp = Detail(self.driver)
        assert dp.bid_price() == '10'
    def test_service_rate(self):
        dp = Detail(self.driver)
        assert dp.buyer_service_rate() == "成交需支付￥20.00 (其中含服务费：￥10.00，费率 10%，最低10元)"

    def test_bid_num(self):
        dp = Detail(self.driver)
        assert dp.bid_num() == '(0)'
    def test_bid_list(self):
        dp = Detail(self.driver)
        assert dp.bid_list() == "暂无出价记录"
    def test_pay(self):
        dp = Detail(self.driver)
        assert dp.pay() == "支付方式：转账汇款、柜台现付、线上支付"
    def test_delivery(self):
        dp = Detail(self.driver)
        assert dp.delivery() == "配送方式：快递到付、快递、上门自提、暂存"
    # def test_service_rate(self):
    #     dp = Detail(self.driver)
    def test_set_price(self):
        dp = Detail(self.driver)
        dp.send_price(1000)
        time.sleep(5)
        assert dp.bid_price() == '1000'
    def test_favorite_src(self):
        dp = Detail(self.driver)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAeCAMAAAB61OwbAAAAkFBMVEUAAADDEzDCEzDCETDDEzDCEjDDFDDCEi/ADy6AAADCEzDAES69DyqxACHCEzHCEzDDEzDDEzDCEy/BEi69DSrDFDDDEzDDEzDDFDDDEy/CEzDDEy/CEzDBEy7BEi/BEizAEC/ADiu4DiW1ACHDEzDDEzDDEzDDEzDDEi/CEjDDEjCqAADCEzDCEzHAEjDDFDFsYXSdAAAAL3RSTlMA+/RZwG7qciACTz4ZBubWurNcOBP37eDOjYSAeExFMzAjDQnbx6+niWZUA56VKlq0F4sAAAE2SURBVCjPfdHnsoIwEAXgk4SmNAErV6q9nvd/u4sOjIrE79funMymoeW4eVl3TV3mroM3I2VIkouV81y7WpCUhhp1+XTf9EsjJC0FnAMyNJaS3HttvqO1di7w3T0ZK8HI9XFx7IC76XP+gduynWUKMRN2O7pa8vAoM8oEHSVEjE4VMGsGTHjDi2m+NTYnIzhSJNDw5rMKGRcb6Ew4xokGtG40YTKC1h9txJxAa8UYBRf1jzMk2ITMdXklt5vHPpF+h7/HZS2Oh/NSWh4aJrfTodw3aHbFdfiORvuEd4v2dz4W83tXn4VQ/TyZi/P7t8neQYvgc2raW5EETPHhyFn86nKLR/SkFGZXK8kUX9bk8dJVaww4zXiYAvWV4oRBmcWl6+44H0OjCNkIC2h5ERl5+MFXyseHf+KSHDBbKcVwAAAAAElFTkSuQmCC"
        assert dp.favorite_src() == a
    def test_remind_src(self):
        dp = Detail(self.driver)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAhCAMAAACP+FljAAAAk1BMVEUAAADDEzDDEzC9DSinAADDEzDDEzC8ECnCEzDCEC69Cy23ACTCFDDDETC/ECy1ACLDFDDCEjDDEzDCEzDCETDDEzDCEzDCEzDDEzDCEzDDEzDCEjDCEzDCEy/CEi7BDy7DEzDCEy/CEi/CEi/AEzDADyvDEzDCEzDBEi/DEzDDFDHDEzDCETDBEC7DFC/CEjDDFDFMLTFrAAAAMHRSTlMA++YSA8rED6QyFge1VxsK9ZaRhUvu6+HW0bB+e1A3Jqp0bWFAIKCMKvDcvDovZ0Xb8LbmAAABoElEQVQ4y3WR2ZaiQBBEo5BFFgUBZRHZxN2ejv//uqGAaZBm7guRJ6Kqkkx05OkZM85pPhabPbVOWPc8v1ud1LjfDLZ6FIwawAx0RZBC0QMTaCKKoyp9Y01qBRpH8AfhvFFo5NoA0Pql4frS9rRrcLyVsbznZhtlmwCwewTY6iSfWaFCYue3A/myEDx2srxgm5AiWGHkIt+1cOlPuDp5CPFJLfiyBx20/htz/pDHXpkexQm/2dG7d2JN7jDg7nwbA1bEa9ePx8MWA1/kHf+ouJdGPbkAJsXXT7HdU66oJJvlABw5KDumspoGijFwZKLCOlDHJMBq03LqzmyoGLg8mI6Bb/b0/Ydtl7KTcgwUidJTy+rEgwVD4Qsj9qrDGIYZuVA1xjaW8an3Ey0WbXnW7x5ijUVyQbljI6KmYokrn678ZuRmyX97rDqxejLa/vaNhLHRy1DQcee+nVKE48yZWp++lZLZ9IcZh1M/jMkbJmSCdE7DVlcnh/QqfPCtkVQcP8t8RyGpNZjhnnXBAaGf3aXJmtVaTxJ9XZsq/os69/4CpH8t/Vk1EYAAAAAASUVORK5CYII="
        assert dp.remind_src() == a
    def test_click_favorite_unlogin(self):
        dp = Detail(self.driver)
        dp.click_favorite()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_click_remind_unlogin(self):
        dp = Detail(self.driver)
        dp.click_remind()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_click_bid_unlogin(self):
        dp = Detail(self.driver)
        dp.click_bid()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_click_change_nickname(self):
        dp = Detail(self.driver)
        dp.click_change_nickname()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_nickname(self):
        dp = Detail(self.driver)
        assert dp.nickname() == " 本场昵称：未登录"


class TestBid:
    '''验证用户出价'''

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        fp = Firstp(self.driver)
        fp.click_collection_detail()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.fp = Detail(self.driver)
        if fp.is_display_login_box() == 1:
            fp.click_num_login()
            fp.send_num('15622145010')
            fp.send_password('123456')
            fp.click_login_botton()

    def teardown_class(self):
        self.driver.quit()
    def test_login(self):
        assert 1==2

