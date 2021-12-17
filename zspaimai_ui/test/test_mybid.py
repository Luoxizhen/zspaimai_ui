from page.mybid import MyBid
from page.firstp import Firstp
import pytest
from selenium import webdriver
from common.readconfig import ini
from common.readpagedata import Pagedata
user_info = Pagedata('detail')['user1']
n = user_info['phone']
p = user_info['password']
class TestMybidInfo:
    '''验证我的竞买页面第一条记录的消息'''
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get(ini.url)
        self.driver.maximize_window()
        fp = Firstp(self.driver)
        fp.login_num_password(num=n,password=p)
        fp.click_my_bid_button()
        self.mb = MyBid(self.driver)
    def teardown_class(self):
        self.driver.quit()
    '''中标记录'''
    def test_the_first_goods_info(self):
        self.mb.swith_to_list("中标记录")
        good_info = self.mb.good_info()
        assert good_info == {"name":"拍品3", "price":"￥1,000.00", "num":"1", "to_pay":'￥1,100.00\n(含服务费￥100.00)', "status":"待支付"}
    def test_click_list(self):
        self.mb.swith_to_list("中标记录")
        self.mb.swith_to_list("全部竞买")
        self.mb.swith_to_list("我的代理")
        self.mb.swith_to_list("关注")

    def test_info_of_all_bid(self):
        info = self.mb.info_list("全部竞买")
        assert info == ["拍品信息", "开拍/结束时间", "当前竞买价", "出价次数", "竞买状态", "开启提醒"]
    def test_info_of_my_proxy(self):
        info = self.mb.info_list("我的代理")
        assert info == ["拍品信息", "开拍/结束时间", "当前竞买价", "出价次数", "竞买状态", "开启提醒"]
    def test_info_of_my_favourite(self):
        info = self.mb.info_list("关注")
        assert info == ["拍品信息", "开拍/结束时间", "当前竞买价", "出价次数", "竞买状态", "开启提醒"]

    '''全部竞买'''
    def test_good_in_my_proxy(self):
        '''验证我的代理页面的第一个拍品信息'''
        info = self.mb.good_in_list("我的代理")
        assert info == {"good_name":"拍品1","good_status":"进行中","good_price":"￥205.00","good_bid_n":"58次出价","my_status_of_good":"领先"}

    def test_good_in_my_favourite(self):
        '''验证我的关注页面的第一个拍品信息'''
        info = self.mb.good_in_list("关注")
        assert info == {"good_name":"拍品1","good_status":"进行中","good_price":"￥205.00","good_bid_n":"58次出价","my_status_of_good":"领先"}
    def test_good_in_all_bid(self):
        '''验证我的全部竞买页面的第一个拍品信息'''
        info = self.mb.good_in_list("全部竞买")
        info_2 = self.mb.good_in_list("全部竞买","二")
        info_3 = self.mb.good_in_list("全部竞买","三")
        assert info_3 == {"good_name":"拍品2","good_status":"流拍","good_price":"￥10.00","good_bid_n":"2次出价","my_status_of_good":"出局"}
        assert info_2 == {"good_name":"拍品3","good_status":"已结束","good_price":"￥1000.00","good_bid_n":"4次出价","my_status_of_good":"中标"}
        assert info == {"good_name":"拍品1","good_status":"进行中","good_price":"￥205.00","good_bid_n":"58次出价","my_status_of_good":"领先"}

    def test_remind_001(self):
        '''验证流拍的拍品，点击开启提醒'''
        self.mb.remind(l="全部竞买",n="三")
        assert self.mb.is_displayed_remind_tip() == 0
    def test_remind_002(self):
        '''验证已结束的拍品，点击开启提醒'''
        self.mb.remind(l="全部竞买", n="二")
        assert self.mb.is_displayed_remind_tip() == 0
    @pytest.mark.skip('页面元素定位有异常')
    def test_remind_003(self):
        '''验证进行中的拍品，点击关闭提醒'''
        self.mb.remind(l="全部竞买", n="一")
        is_displayed = self.mb.is_displayed_remind_tip()
        self.mb.close_remind_tip(i=0)
        assert is_displayed == 1

    @pytest.mark.skip('页面元素定位有异常')
    def test_remind_004(self):
        '''验证进行中的拍品，点击提醒按钮-确定关闭提醒'''
        self.mb.remind(l="全部竞买", n="一")
        msg = self.mb.tip()
        self.mb.close_remind_tip(i=1)
        assert msg == "确定要关闭提醒功能吗"

    @pytest.mark.skip('页面元素定位有异常')
    def test_remind_005(self):
        '''验证进行中的拍品，开启提醒信息'''
        self.mb.remind(l="全部竞买", n="一")
        msg = self.mb.tip()
        self.mb.close_remind_tip(i=2)
        assert msg == "开启提醒设置后，将在拍品结拍前5分钟，通过短信和站内信的形式通知您"

    def test_pay(self):
        '''验证在中标页面选择拍品后，去支付'''
        self.mb.swith_to_list("中标记录")
        self.mb.select("一")
        assert self.mb.num_of_select() == "共1项"
        assert self.mb.all_to_pay() == "￥1,100.00"
        self.mb.select("一","取消")
        assert self.mb.all_to_pay() == "￥0.00"
