from base.webpage import Web
from common.readelement import Element
from selenium.common.actions.key_actions import KeyActions
import KeyActions
bidp = Element("bid")
class Bid(Web):
    def good_name(self):
        return self.element_text(bidp["拍品名称"])
    def good_status(self):
        return self.element_text(bidp['拍品状态'])
    def good_price(self):
        return self.element_text(bidp['拍品价格'])
    def bid(self):
        self.is_click(bidp["竞买"])
    def click_button(self,b="前翻页按钮"):
        self.is_click(bidp[b])
    def go_to_page(self,page):
        self.input_text(bidp['页数填写'],page)
        #输入enter

