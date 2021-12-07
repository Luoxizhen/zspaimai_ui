from base.webpage import Web
from common.readelement import Element
from selenium.webdriver.common.actions.key_actions import KeyActions
from utils import times
od = Element("order_detail")
class OrderDetail(Web):
    '''订单支付详情'''
    def deliver_type(self,d="快递到付"):
        self.is_click(od[d])
    def pay_type(self,p="余额"):
        self.is_click(od[p])
    def select_union(self):
        self.is_click(od["优惠劵"])
        self.is_click(od["第一个优惠劵"])
        self.is_click(od["确认所选优惠劵"])
    def all_to_pay(self):
        self.element_text(od["合计"])
    def pay(self):
        self.is_click(od["提交订单"])
    def input_password(self):
        self.input_text(od["输入密码"],  "246810")
        KeyActions().send_keys("Enter")
        times.sleep(5)

    def good_info(self):
        name = self.element_text(od["拍品名称"])
        pay_money = self.element_text(od["支付金额"])
        service = self.element_text(od["服务费"])
        info = {"name":name,"pay_money":pay_money,"service":service}
        return info
    def delivery_info(self):
        name = self.element_text(od["收货人"])
        elephone = self.element_text(od["联系方式"])
        address = self.element_text(od["收货地址"])
        info = {"name":name,"elephone":elephone,"address":address}
        return info
    def change_delivery_info(self):
        self.is_click(od["修改收货信息"])


