import time

from page.firstp import Firstp
from page.mybid import MyBid
from page.order_detail import OrderDetail
from common.readconfig import ini
from selenium import webdriver
import pytest
from common.readpagedata import Pagedata
user_info = Pagedata('detail')['user1']
n = user_info['phone']
p = user_info['password']
class TestOrderDetail:
    '''验证订单详情页信息'''
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get(ini.url)
        self.driver.maximize_window()
        self.fp = Firstp(self.driver)
        self.fp.login_num_password(num=n,password=p)
        self.fp.click_my_bid_button()
        self.mb = MyBid(self.driver)
        self.mb.go_to_pay(n="一")
        self.od = OrderDetail(self.driver)
    def teardown_class(self):
        self.driver.quit()
    def test_good_info(self):
        good_info = self.od.good_info()
        assert good_info == {"name":"拍品3","pay_money":'￥1,100.00\n(含服务费￥100.00)',"service":"(含服务费￥100.00)"}
    @pytest.mark.skip("用户未设置密码")
    def test_delivery_info(self):
        delivery_info = self.od.delivery_info()
        assert delivery_info == {"name":"收货人：张生","elephone":"联系方式：18023038634","address":"收货地址：广东省广州市萝岗区我家"}
    @pytest.mark.skip("")
    def test_change_delivery_info_001(self):
        self.od.change_delivery_info()
        #self.fp = Firstp(self.driver)
        is_display_of_dialog = self.fp.is_display_of_dialog()
        self.fp.close_dialog()
        assert is_display_of_dialog == 1
    @pytest.mark.skip("支付流程测试用例设置在其他类")
    def test_pay_order(self):
        '''验证微信支付订单详情显示准确'''
        self.od.deliver_type("上门自提")

        self.od.pay_type("微信支付")
        self.od.change_delivery_day()
        tip_of_wechat_pay = self.od.tip_of_wechat_tip()
        all_to_pay = self.od.all_to_pay()

        self.od.pay()
        assert tip_of_wechat_pay == "1000元以上收取６‰手续费"
        assert all_to_pay == "1,106.63元"

        #assert self.driver.current_url == "http://home.online.zspaimai.cn/order/pay?type=pay"
    def test_all_to_pay(self):
        '''验证选择不同的支付方式，订单合计金额显示准确'''
        self.od.pay_type('微信支付')
        tip_of_wechat_pay = self.od.tip_of_wechat_tip()
        all_to_pay = self.od.all_to_pay()
        assert tip_of_wechat_pay == "1000元以上收取６‰手续费"
        assert all_to_pay == "1,106.63元"
        self.od.pay_type('银行转账')
        tip_of_wechat_pay = self.od.tip_of_wechat_tip()
        all_to_pay = self.od.all_to_pay()
        assert tip_of_wechat_pay == "建议2万元以上大额付款使用"
        assert all_to_pay == "1,100.00元"
    def test_delivery_type(self):
        '''验证选择不同的提货方式，页面显示准确'''
        self.od.deliver_type('上门自提')
        time.sleep(1)
        is_display = self.od.is_display_of_map()

        tip = self.od.tip_of_delivery()
        address = self.od.address_of_zs()
        assert is_display == 1  # 显示地图
        assert address == "中晟在线（广州）信息技术有限公司"
        assert tip == ('1、本人办理，请携带身份证','2、委托他人办理，请携带双方证件和授权书','3、预约时间要在支付期限内')
    @pytest.mark.skip('div 提示框后续样式确定后再做')
    def test_money_pay(self):
        '''验证用户未设置密码，点击余额支付时，弹窗'''
        pass








