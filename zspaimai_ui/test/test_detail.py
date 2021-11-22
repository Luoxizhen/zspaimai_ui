import time
import pytest
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

        if fp.is_diplayed_loginbox()==1:
            fp.click_close_login()
        self.dp = Detail(self.driver)



    def teardown_class(self):
        self.driver.quit()

    def test_name(self):
        assert self.dp.collection_name() == good_info['name']
    def test_start_time(self):
        assert self.dp.start_time() == good_info['begin_time']

    def test_end_time(self):
        assert self.dp.start_time() == good_info['end_time']

    def test_status(self):
        assert self.dp.collection_status() == "正在拍卖"
    def test_price(self):
        assert self.dp.collection_price() == "￥"+str(good_info['price'])+".00"
    def test_bid_price(self):
        assert self.dp.bid_price() == '10'
    def test_service_rate(self):
        assert self.dp.buyer_service_rate() == "成交需支付￥20.00 (其中含服务费：￥10.00，费率 10%，最低10元)"

    def test_bid_num(self):
        assert self.dp.bid_num() == '(0)'
    def test_bid_list(self):
        assert self.dp.bid_list() == "暂无出价记录"
    def test_pay(self):
        assert self.dp.pay() == "支付方式：转账汇款、柜台现付、线上支付"
    def test_delivery(self):
        assert self.dp.delivery() == "配送方式：快递到付、快递、上门自提、暂存"
    # def test_service_rate(self):
    #     dp = Detail(self.driver)
    def test_set_price(self):
        self.dp.send_price(1000)
        time.sleep(5)
        assert self.dp.bid_price() == '1000'
    def test_favorite_src(self):
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAeCAMAAAB61OwbAAAAkFBMVEUAAADDEzDCEzDCETDDEzDCEjDDFDDCEi/ADy6AAADCEzDAES69DyqxACHCEzHCEzDDEzDDEzDCEy/BEi69DSrDFDDDEzDDEzDDFDDDEy/CEzDDEy/CEzDBEy7BEi/BEizAEC/ADiu4DiW1ACHDEzDDEzDDEzDDEzDDEi/CEjDDEjCqAADCEzDCEzHAEjDDFDFsYXSdAAAAL3RSTlMA+/RZwG7qciACTz4ZBubWurNcOBP37eDOjYSAeExFMzAjDQnbx6+niWZUA56VKlq0F4sAAAE2SURBVCjPfdHnsoIwEAXgk4SmNAErV6q9nvd/u4sOjIrE79funMymoeW4eVl3TV3mroM3I2VIkouV81y7WpCUhhp1+XTf9EsjJC0FnAMyNJaS3HttvqO1di7w3T0ZK8HI9XFx7IC76XP+gduynWUKMRN2O7pa8vAoM8oEHSVEjE4VMGsGTHjDi2m+NTYnIzhSJNDw5rMKGRcb6Ew4xokGtG40YTKC1h9txJxAa8UYBRf1jzMk2ITMdXklt5vHPpF+h7/HZS2Oh/NSWh4aJrfTodw3aHbFdfiORvuEd4v2dz4W83tXn4VQ/TyZi/P7t8neQYvgc2raW5EETPHhyFn86nKLR/SkFGZXK8kUX9bk8dJVaww4zXiYAvWV4oRBmcWl6+44H0OjCNkIC2h5ERl5+MFXyseHf+KSHDBbKcVwAAAAAElFTkSuQmCC"
        assert self.dp.favorite_src() == a
    def test_remind_src(self):
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAhCAMAAACP+FljAAAAk1BMVEUAAADDEzDDEzC9DSinAADDEzDDEzC8ECnCEzDCEC69Cy23ACTCFDDDETC/ECy1ACLDFDDCEjDDEzDCEzDCETDDEzDCEzDCEzDDEzDCEzDDEzDCEjDCEzDCEy/CEi7BDy7DEzDCEy/CEi/CEi/AEzDADyvDEzDCEzDBEi/DEzDDFDHDEzDCETDBEC7DFC/CEjDDFDFMLTFrAAAAMHRSTlMA++YSA8rED6QyFge1VxsK9ZaRhUvu6+HW0bB+e1A3Jqp0bWFAIKCMKvDcvDovZ0Xb8LbmAAABoElEQVQ4y3WR2ZaiQBBEo5BFFgUBZRHZxN2ejv//uqGAaZBm7guRJ6Kqkkx05OkZM85pPhabPbVOWPc8v1ud1LjfDLZ6FIwawAx0RZBC0QMTaCKKoyp9Y01qBRpH8AfhvFFo5NoA0Pql4frS9rRrcLyVsbznZhtlmwCwewTY6iSfWaFCYue3A/myEDx2srxgm5AiWGHkIt+1cOlPuDp5CPFJLfiyBx20/htz/pDHXpkexQm/2dG7d2JN7jDg7nwbA1bEa9ePx8MWA1/kHf+ouJdGPbkAJsXXT7HdU66oJJvlABw5KDumspoGijFwZKLCOlDHJMBq03LqzmyoGLg8mI6Bb/b0/Ydtl7KTcgwUidJTy+rEgwVD4Qsj9qrDGIYZuVA1xjaW8an3Ey0WbXnW7x5ijUVyQbljI6KmYokrn678ZuRmyX97rDqxejLa/vaNhLHRy1DQcee+nVKE48yZWp++lZLZ9IcZh1M/jMkbJmSCdE7DVlcnh/QqfPCtkVQcP8t8RyGpNZjhnnXBAaGf3aXJmtVaTxJ9XZsq/os69/4CpH8t/Vk1EYAAAAAASUVORK5CYII="
        assert self.dp.remind_src() == a
    def test_click_favorite_unlogin(self):
        self.dp.click_favorite()
        is_display = self.dp.is_diplayed_loginbox()
        self.dp.click_close_login()
        assert is_display == 1
    def test_click_remind_unlogin(self):
        self.dp.click_remind()
        is_display = self.dp.is_diplayed_loginbox()
        self.dp.click_close_login()
        assert is_display == 1
    def test_click_bid_unlogin(self):
        self.dp.click_bid()
        is_display = self.dp.is_diplayed_loginbox()
        self.dp.click_close_login()
        assert is_display == 1
    def test_click_change_nickname(self):
        dp = Detail(self.driver)
        dp.click_change_nickname()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_click_change_nickname_1(self):
        dp = Detail(self.driver)
        dp.change_nickname()
        is_display = dp.is_diplayed_loginbox()
        dp.click_close_login()
        assert is_display == 1
    def test_nickname(self):
        assert self.dp.nickname() == " 本场昵称：未登录"
    def test_button_text(self):
        assert self.dp.button_text() == "立即出价"


class TestBid:
    '''验证用户出价'''

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        fp = Firstp(self.driver)
        fp.click_collection_detail()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        if fp.is_display_login_box() == 1:
            fp.click_num_login()
            fp.send_num('15622145010')
            fp.send_password('123456')
            fp.click_login_botton()
        self.dp = Detail(self.driver)
    def teardown_class(self):
        self.driver.quit()
    def bid_001(self):
        #self.dp.bid()
        self.dp.refresh()
        assert self.dp.button_text() == "出代理价"
        assert self.dp.collection_price() == "￥"+str(good_info['price'])+".00"
        assert self.dp.bid_price() == str(good_info['price'] + 1)
        assert self.dp.my_status() == "领先"
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert self.dp.bid_num() == '(1)'
        assert self.dp.bid_quota() == "5000015040446"
    @pytest.mark.skip()
    def test_click_favorite(self):
        self.dp.favorite()
        time.sleep(3)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAeCAMAAAB61OwbAAAAeFBMVEUAAADCEy/DFDDCEi/DEzG+ESy4ACPCEzHCEy/CEi/CEi3DEzDCEi66ACjDEzDDEzDDEzDCEzDCEjDCES/AEi3DEzDCFDDDEzDDEzHCFDDCEzDBEjC/Dy2/DCzDEzDCFDDCEzDDEi/BEzHAETHAEjDCCim8CyzDFDFMUyALAAAAJ3RSTlMAXfZN+x4H0mxhMvE2C+2+rnVxVyng29XHtqNAIhTkxJaMeElFGRdXRQ27AAAAz0lEQVQoz4XQ2ZKCMBCF4ZOVEHZh3J0Z137/NxQ1JaKk/e5Sf6qTajwUeZseDQKj0tZbDIpmQb1y7dHL6+x2StzzSrekIHNAIymowsjtnAbuQIPkjJ6tKKpGTxBDAXZJjBXQSWJkBi2xTpgRS3y7kEIQS8FrrsstbEKMPwAN/wVg9xPvSfFl1wp3dayv8WAijyx2CDZyqpceT0JPrEDhhfvoWmBk9t5TvHF6NF/gg5BDzxQmqJKC3w0m5fOw4A4Rprr11QVRxT/pvQUn9xi7AhtpXMgykASqAAAAAElFTkSuQmCC"
        assert self.dp.favorite_src() == a

    @pytest.mark.skip()
    def test_click_remind(self):
        self.dp.remind()
        time.sleep(3)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAhCAMAAACP+FljAAAAjVBMVEUAAACoABPDEzDDEzDDFDC8ECm2ACPDEzDDEzDDEzDCEzDCEjDCEi/CES3ADyy/CyrDFDDDEzDCEzDCEzDDEzDCEzDAEzDCEi6+ECrDEzDCEzDDEzDCEzDDEzDCEy/CEi/BETHCEi/CDi+5DSbDFDHDEzDDETHBEy/DEzDCFDDDEzHCEy/CETDDFDH///9MeZsOAAAALXRSTlMABMn7+A8JxPLvpX5hMhoV6tGilY6EQDce5ODBsat5ckcpJA3c11lOurWIbDs0En7jAAABE0lEQVQ4y33S17KCQBBF0TMDDDlLMGe96fj/n3cFLSzQmfXa+6G7qtFrVhEmolWDwcWnRCfdN80+RUfSv+BBhBbnNRBXbmaTduZWMVAvaIUCd05BygPqb4sDe/WHgyQLB0BAro+qfI6HZKaOazIAUHoVEpdvlgkqrwQgWiQ5P5ApWoGOWvKjL4WHH2qE6MU2Nbw9OgG1CtwdPL7cbqPAbwH8Uh8wArA2BQEgzqYgF0gzUzB30HqmwE+Q+OOgN3RZCmduChYKQtLABVDSYAbgSoMdAGdBrdMRdxtqbdFxTtQ4O+hdLX5k7fAUGh+qM9OdONjYnLA3GNlJjsgaEyqS1rCdGym8E/E2cPN8WWxjAS0xnf0DtH5+r8QWNBAAAAAASUVORK5CYII="
        assert self.dp.remind_src() == a
    @pytest.mark.skip()
    def test_bid_002(self):
        '''验证出代理价功能'''
        self.dp.refresh()
        self.dp.bid()
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"

        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
        assert self.dp.my_status() == "代理·领先"

    @pytest.mark.skip()
    def test_bid_003(self):
        '''验证"是否关闭代理"弹窗关闭按钮功能'''
        self.dp.close_proxy()
        # alert = self.driver.switch_to.alert
        # text = alert.text
        # print(text)
        # alert.accept()
        msg = self.dp.alert_msg()
        print(msg)
        self.dp.close_alert()
        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
        assert self.dp.my_status() == "代理·领先"
    def test_bid_004(self):
        '''验证"是否关闭代理"弹窗，否按钮功能'''
        self.dp.close_proxy()

        self.dp.refuse_alert()
        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
    def test_bid_005(self):
        '''验证"是否关闭代理"弹窗，是按钮功能'''
        self.dp.close_proxy()

        self.dp.accept_alert()
        assert "出代理价" in self.dp.button_text()
    def test_bid_006(self):
        '''验证"是否关闭代理"弹窗，是按钮功能'''
        self.dp.refresh()
        time.sleep(2)
        self.dp.bid()
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"

        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
        assert self.dp.my_status() == "代理·领先"
    def test_bid_007(self):
        self.dp.change_price()
        tip = "请勿重复出同样代理价"
        assert self.dp.tip() == tip
    def test_bid_008(self):
        self.dp.minus()
        assert self.dp.bid_price() == '11'
    def test_bid_009(self):
        self.dp.add()
        assert self.dp.bid_price() == '12'
    def test_bid_010(self):
        self.dp.change_price()
        assert self.dp.bid_quota() == "5000015040454"
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert "当前代理价￥12.00 (更新)" in self.dp.proxy()
    def test_bid_011(self):
        self.dp.send_price(15)
        self.dp.minus()
        assert self.dp.bid_price() == '14'










    def click_bid_003(self):
        #self.dp.refresh()
        self.dp.bid()
        self.dp.add()
        self.dp.bid()
        #assert self.dp.buyer_service_rate() == "成交需支付￥22.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert self.dp.button_text() == " 当前代理价￥12.00 (更新)"
        assert self.dp.bid_quota() == "5000015040444"
        alert = self.driver.switch_to.alert
        alert.accept()
        assert self.dp.buyer_service_rate() == "成交需支付￥22.00 (其中含服务费：￥10.00，费率 10%，最低10元)"









