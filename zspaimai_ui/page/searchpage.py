from base.webpage import Web, sleep
from common.readelement import Element

search = Element('search')

def p():
    print("www")
class SearchPage(Web):
    """搜索类"""


    def input_search(self, content):
        """输入搜索"""
        self.input_text(search['搜索框'], txt=content)
        sleep()

    @property
    def imagine(self):
        """搜索联想"""
        return [x.text for x in self.find_elements(search['候选'])]

    def click_search(self):
        """点击搜索"""
        self.is_click(search['搜索按钮'])

if __name__ == "__main___":
    p()