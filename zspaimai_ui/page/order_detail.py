from base.webpage import Web
from common.readelement import Element
od = Element("order_detail")
class OrderDetail(Web):
    '''订单支付详情'''
    def deliver_type(self,d="快递支付"):
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
        self.input_text(od["输入密码"],  "123456")
    def good_info(self):
        name = self.element_text(od["拍品名称"])
        pay_money = self.element_text(od["支付金额"])
        service = self.element_text(od["服务费"])
        info = {"name":name,"pay_money":pay_money,"service":service}
        return info