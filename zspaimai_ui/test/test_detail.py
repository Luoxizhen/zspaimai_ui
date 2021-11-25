import time
import pytest
from page.detailp import Detail
from common.readconfig import ini
from selenium import webdriver
from page.firstp import Firstp
from common.readpagedata import Pagedata
from interface_test.goods_test import user_bid, good_edit
from utils import times

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

        if fp.is_display_login_box()==1:
            fp.close_login_box()
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
    def test_minus(self):
        self.dp.send_price(49)
        self.dp.minus()
        assert self.dp.bid_price() == '48'
        self.dp.send_price(51)
        self.dp.minus()
        assert self.dp.bid_price() == '50'
        # self.dp.send_price(51.500004)
        # self.dp.minus()
        # assert self.dp.bid_price() == '50'

        self.dp.send_price(52)
        self.dp.minus()
        assert self.dp.bid_price() == '50'

        self.dp.send_price(99)
        self.dp.minus()
        assert self.dp.bid_price() == '98'
        self.dp.send_price(101)
        self.dp.minus()
        assert self.dp.bid_price() == '100'

        self.dp.send_price(100)
        self.dp.minus()
        assert self.dp.bid_price() == '98'
        self.dp.send_price(105)
        self.dp.minus()
        assert self.dp.bid_price() == '100'
        self.dp.send_price(500)
        self.dp.minus()
        assert self.dp.bid_price() == '495'
        self.dp.send_price(510)
        self.dp.minus()
        assert self.dp.bid_price() == '500'
        self.dp.send_price(1000)
        self.dp.minus()
        assert self.dp.bid_price() == '990'
        self.dp.send_price(1025)
        self.dp.minus()
        assert self.dp.bid_price() == '1020'
        self.dp.send_price(2000)
        self.dp.minus()
        assert self.dp.bid_price() == '1980'
        self.dp.send_price(2049)
        self.dp.minus()
        assert self.dp.bid_price() == '2000'
        self.dp.send_price(5000)
        self.dp.minus()
        assert self.dp.bid_price() == '4950'
        self.dp.send_price(5100)
        self.dp.minus()
        assert self.dp.bid_price() == '5000'
        self.dp.send_price(10000)
        self.dp.minus()
        assert self.dp.bid_price() == '9900'
        self.dp.send_price(10200)
        self.dp.minus()
        assert self.dp.bid_price() == '10000'
        self.dp.send_price(20000)
        self.dp.minus()
        assert self.dp.bid_price() == '19800'
        self.dp.send_price(20400)
        self.dp.minus()
        assert self.dp.bid_price() == '20000'
        self.dp.send_price(50000)
        self.dp.minus()
        assert self.dp.bid_price() == '49500'
        self.dp.send_price(51000)
        self.dp.minus()
        assert self.dp.bid_price() == '50000'
        self.dp.send_price(200000)
        self.dp.minus()
        assert self.dp.bid_price() == '199000'
        self.dp.send_price(20000000000)
        self.dp.minus()
        assert self.dp.bid_price() == '19999998000'
    def test_add(self):
        self.dp.send_price(49)
        self.dp.add()
        assert self.dp.bid_price() == '50'
        self.dp.send_price(51)
        self.dp.add()
        assert self.dp.bid_price() == '52'
        # self.dp.send_price(51.500004)
        # self.dp.add()
        # assert self.dp.bid_price() == '52'
        self.dp.send_price(98)
        self.dp.add()
        assert self.dp.bid_price() == '100'

        self.dp.send_price(100)
        self.dp.add()
        assert self.dp.bid_price() == '105'
        self.dp.send_price(496)
        self.dp.add()
        assert self.dp.bid_price() == '500'


        self.dp.send_price(500)
        self.dp.add()
        assert self.dp.bid_price() == '510'
        self.dp.send_price(990)
        self.dp.add()
        assert self.dp.bid_price() == '1000'
        self.dp.send_price(1000)
        self.dp.add()
        assert self.dp.bid_price() == '1020'
        self.dp.send_price(1980)
        self.dp.add()
        assert self.dp.bid_price() == '2000'
        self.dp.send_price(2000)
        self.dp.add()
        assert self.dp.bid_price() == '2050'
        self.dp.send_price(4950)
        self.dp.add()
        assert self.dp.bid_price() == '5000'
        self.dp.send_price(5000)
        self.dp.add()
        assert self.dp.bid_price() == '5100'
        self.dp.send_price(9900)
        self.dp.add()
        assert self.dp.bid_price() == '10000'
        self.dp.send_price(10000)
        self.dp.add()
        assert self.dp.bid_price() == '10200'
        self.dp.send_price(19800)
        self.dp.add()
        assert self.dp.bid_price() == '20000'
        self.dp.send_price(20000)
        self.dp.add()
        assert self.dp.bid_price() == '20500'
        self.dp.send_price(49500)
        self.dp.add()
        assert self.dp.bid_price() == '50000'
        self.dp.send_price(50000)
        self.dp.add()
        assert self.dp.bid_price() == '51000'
        self.dp.send_price(199500)
        self.dp.add()
        assert self.dp.bid_price() == '200000'
        self.dp.send_price(200000)
        self.dp.add()
        assert self.dp.bid_price() == '202000'
        self.dp.send_price(19999998000)
        self.dp.add()
        assert self.dp.bid_price() == '20000000000'
    def test_alway_ask(self):
        # js = "var q=document.documentElement.scrollTop=150"
        # self.driver.execute_script(js)
        self.dp.alway_ask()
        time.sleep(2)
        assert self.dp.is_displayed_of_alway_ask() == 1
    def test_alway_ask1(self):
        self.dp.move(10, 10)
        self.dp.alway_ask1()
        assert self.dp.is_displayed_of_alway_ask() == 1
    def test_read_alway_ask(self):
        self.dp.move(10, 10)
        self.dp.alway_ask()

        self.dp.read_alway_ask()
        url = self.driver.current_url
        self.driver.back()
        assert url == "http://home.online.zspaimai.cn/article?keywords=proxy_bid_description"



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

    #@pytest.mark.skip()
    def test_bid_001(self):
        #self.dp.bid()
        #self.dp.refresh()
        # print(self.quota)
        quota = int(self.dp.bid_quota())
        pd = Pagedata("detail")
        user_data = pd['users']
        user_data['user1']['quota'] = quota
        pd.setitem("users", user_data)

        # self.quota =100
        # print(self.dp.bid_quota())
        # print(self.quota)
        assert self.dp.button_text() == "出代理价"
        assert self.dp.collection_price() == "￥"+str(good_info['price'])+".00"
        assert self.dp.bid_price() == str(good_info['price'] + 1)
        assert self.dp.my_status() == "领先"
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert self.dp.bid_num() == '(1)'


        #quota = Pagedata("personal")['info']['quota']

        #assert self.dp.bid_quota() == quota
    #@pytest.mark.skip()
    def test_click_favorite(self):
        self.dp.favorite()
        time.sleep(3)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAeCAMAAAB61OwbAAAAeFBMVEUAAADCEy/DFDDCEi/DEzG+ESy4ACPCEzHCEy/CEi/CEi3DEzDCEi66ACjDEzDDEzDDEzDCEzDCEjDCES/AEi3DEzDCFDDDEzDDEzHCFDDCEzDBEjC/Dy2/DCzDEzDCFDDCEzDDEi/BEzHAETHAEjDCCim8CyzDFDFMUyALAAAAJ3RSTlMAXfZN+x4H0mxhMvE2C+2+rnVxVyng29XHtqNAIhTkxJaMeElFGRdXRQ27AAAAz0lEQVQoz4XQ2ZKCMBCF4ZOVEHZh3J0Z137/NxQ1JaKk/e5Sf6qTajwUeZseDQKj0tZbDIpmQb1y7dHL6+x2StzzSrekIHNAIymowsjtnAbuQIPkjJ6tKKpGTxBDAXZJjBXQSWJkBi2xTpgRS3y7kEIQS8FrrsstbEKMPwAN/wVg9xPvSfFl1wp3dayv8WAijyx2CDZyqpceT0JPrEDhhfvoWmBk9t5TvHF6NF/gg5BDzxQmqJKC3w0m5fOw4A4Rprr11QVRxT/pvQUn9xi7AhtpXMgykASqAAAAAElFTkSuQmCC"
        assert self.dp.favorite_src() == a

    #@pytest.mark.skip()
    def test_click_remind(self):
        self.dp.remind()
        time.sleep(3)
        a = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAhCAMAAACP+FljAAAAjVBMVEUAAACoABPDEzDDEzDDFDC8ECm2ACPDEzDDEzDDEzDCEzDCEjDCEi/CES3ADyy/CyrDFDDDEzDCEzDCEzDDEzDCEzDAEzDCEi6+ECrDEzDCEzDDEzDCEzDDEzDCEy/CEi/BETHCEi/CDi+5DSbDFDHDEzDDETHBEy/DEzDCFDDDEzHCEy/CETDDFDH///9MeZsOAAAALXRSTlMABMn7+A8JxPLvpX5hMhoV6tGilY6EQDce5ODBsat5ckcpJA3c11lOurWIbDs0En7jAAABE0lEQVQ4y33S17KCQBBF0TMDDDlLMGe96fj/n3cFLSzQmfXa+6G7qtFrVhEmolWDwcWnRCfdN80+RUfSv+BBhBbnNRBXbmaTduZWMVAvaIUCd05BygPqb4sDe/WHgyQLB0BAro+qfI6HZKaOazIAUHoVEpdvlgkqrwQgWiQ5P5ApWoGOWvKjL4WHH2qE6MU2Nbw9OgG1CtwdPL7cbqPAbwH8Uh8wArA2BQEgzqYgF0gzUzB30HqmwE+Q+OOgN3RZCmduChYKQtLABVDSYAbgSoMdAGdBrdMRdxtqbdFxTtQ4O+hdLX5k7fAUGh+qM9OdONjYnLA3GNlJjsgaEyqS1rCdGym8E/E2cPN8WWxjAS0xnf0DtH5+r8QWNBAAAAAASUVORK5CYII="
        assert self.dp.remind_src() == a
    #@pytest.mark.skip()
    def test_bid_002(self):
        '''验证出代理价功能'''
        #self.dp.refresh()
        self.dp.bid()
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
        assert self.dp.my_status() == "代理·领先"
        quota = Pagedata('detail')['users']['user1']['quota']
        assert self.dp.bid_quota() == str(quota - 1)
        # self.quota = self.dp.bid_quota()

    #@pytest.mark.skip()
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

    #@pytest.mark.skip()
    def test_bid_004(self):
        '''验证"是否关闭代理"弹窗，否按钮功能'''
        self.dp.close_proxy()
        self.dp.refuse_alert()
        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()

    #@pytest.mark.skip()
    def test_bid_005(self):
        '''验证"是否关闭代理"弹窗，是按钮功能'''
        self.dp.close_proxy()
        self.dp.accept_alert()
        assert "出代理价" in self.dp.button_text()
        quota = Pagedata('detail')['users']['user1']['quota']
        assert self.dp.bid_quota() == str(quota)

    #@pytest.mark.skip()
    def test_bid_006(self):
        '''验证关闭代理后，重新出价'''
        #self.dp.refresh()
        time.sleep(2)
        self.dp.bid()
        assert self.dp.buyer_service_rate() == "成交需支付￥21.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert "当前代理价￥11.00 (更新)" in self.dp.proxy()
        assert self.dp.my_status() == "代理·领先"
        quota = Pagedata('detail')['users']['user1']['quota']
        assert self.dp.bid_quota() == str(quota -1)

    @pytest.mark.skip()
    def test_bid_007(self):
        self.dp.change_price()
        tip = "请勿重复出同样代理价"
        assert self.dp.tip() == tip

    #@pytest.mark.skip()
    def test_bid_008(self):
        '''验证默认代理价情况下，点 - ，代理价不变'''
        bid_price = self.dp.bid_price()
        self.dp.minus()
        assert self.dp.bid_price() == bid_price

    #@pytest.mark.skip()
    def test_bid_009(self):
        '''验证默认代理价情况下，点 +，代理价 +1'''
        bid_price = self.dp.bid_price()
        self.dp.add()
        assert self.dp.bid_price() == str(int(bid_price)+1)

    #@pytest.mark.skip()
    def test_bid_010(self):
        '''验证更新代理价情况'''
        self.dp.change_price()
        quota = Pagedata('detail')['users']['user1']['quota']
        assert self.dp.bid_quota() == str(quota - 2)
        assert self.dp.buyer_service_rate() == "成交需支付￥22.00 (其中含服务费：￥10.00，费率 10%，最低10元)"
        assert "当前代理价￥12.00 (更新)" in self.dp.proxy()

    #@pytest.mark.skip()
    def test_bid_011(self):
        '''验证更新代理价后-1'''
        bid_price = int(self.dp.bid_price()) +5
        self.dp.send_price(bid_price)
        self.dp.minus()
        assert self.dp.bid_price() == str(bid_price -1)

    #@pytest.mark.skip()
    def test_bid_012(self):
        '''验证点击查看更多按钮，显示出价记录弹框'''
        self.dp.more_bid_price()
        is_display = self.dp.is_display_of_bid_price()
        self.dp.close_bid_price()
        assert is_display == 1
    def c_price(self):
        '''返回拍品的价格'''
        return int(self.dp.collection_price().removeprefix("￥").removesuffix(".00"))
    def b_num(self):
        '''返回拍品的出价次数'''
        return int(self.dp.bid_num().removeprefix("(").removesuffix(")"))
    def test_bid_013(self):
        '''验证两个用户竞买该拍品,当前用户出局'''
        # collection_price = self.c_price()
        #
        #quota = int(self.dp.bid_quota())

        # bid_num = self.b_num()
        goods_id = Pagedata("firstp")["info"]["good_ids"][4]
        info = {"user_info":{"phone": "18023038634","password": "123456"}, "bid_info":{"goods_id": goods_id, "price": 100}}
        user_bid(**info)
        # assert self.c_price() == collection_price + 1 #拍品价格验证
        assert self.dp.my_status() == "出局" #用户当前出价状态验证
        # assert self.dp.bid_quota() == str(quota + 12) #用户额度验证
        assert self.dp.bid_price() == str(12 + 2) #出价金额验证
        assert self.b_num() == 1 + 3 #出价记录验证

    def test_bid_014(self):
        '''验证其他用户出代理价时，当前用户出价小于代理价的情况，当前用户出局'''
        collection_price = int(self.dp.collection_price().removeprefix("￥").removesuffix(".00"))
        quota = int(self.dp.bid_quota())
        bid_num = int(self.dp.bid_num().removeprefix("(").removesuffix(")"))
        self.dp.bid()
        assert self.dp.my_status() == "出局"
        assert self.dp.collection_price() == "￥" + str(collection_price + 1) + ".00"
        assert self.dp.bid_quota() == str(quota)
        assert self.dp.bid_price() == str(collection_price + 2)
        assert self.dp.bid_num().removeprefix("(").removesuffix(")") == str(bid_num + 2)

    def test_bid_015(self):
        '''验证其他用户出代理价时，当前用户出价等于代理价的情况，当前用户出局'''
        quota = int(self.dp.bid_quota())
        bid_num = int(self.dp.bid_num().removeprefix("(").removesuffix(")"))
        self.dp.bid(100)
        assert self.dp.my_status() == "出局"
        assert self.dp.collection_price() == "￥100.00"
        assert self.dp.bid_quota() == str(quota)
        assert self.dp.bid_price() == "105"
        assert self.dp.bid_num().removeprefix("(").removesuffix(")") == str(bid_num + 2)


    def test_bid_016(self):
        '''验证其他用户出代理价时，当前用户出价高于代理价的情况，当前用户领先'''
        quota = int(self.dp.bid_quota())
        bid_num = int(self.dp.bid_num().removeprefix("(").removesuffix(")"))
        self.dp.bid()
        assert self.dp.my_status() == "领先"
        assert self.dp.collection_price() == "￥105.00"
        assert self.dp.bid_quota() == str(quota-105)
        assert self.dp.bid_num().removeprefix("(").removesuffix(")") == str(bid_num + 1)
    def test_bid_017(self):
        '''验证其他用户出代理，当前用户出价高于代理价的情况，当前用户领先'''
        bid_num = int(self.dp.bid_num().removeprefix("(").removesuffix(")"))
        collection_price = int(self.dp.collection_price().removeprefix("￥").removesuffix(".00"))
        quota = int(self.dp.bid_quota())

        goods_id = Pagedata("firstp")["info"]["good_ids"][4]
        info = {"user_info": {},
                "bid_info": {"goods_id": goods_id, "price": 200}}
        user_bid(**info)
        self.dp.bid(300)
        assert self.dp.my_status() == "代理·领先"
        assert self.dp.collection_price() == "￥205.00"
        assert self.dp.bid_quota() == str(quota + 105 -300)
        assert self.dp.bid_num().removeprefix("(").removesuffix(")") == str(bid_num + 4)











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




class TestAbort:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(ini.url)
        now = times.timestamp()
        begin_time = now
        end_time = now + 120
        good = {"begin_time": begin_time,
                "end_time": end_time,
                "retain_price" :"10000"
                }
        good_id = Pagedata("firstp")["info"]["good_ids"][5]
        good_edit(good_id, **good)

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





