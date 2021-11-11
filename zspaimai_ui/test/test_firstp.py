import time
import unittest
import pytest
from selenium import webdriver
from page.firstp import Firstp
from test.init import Init2, Init3, Init4, Init5, Init

class TestFirstp001(Init3,Firstp):
    '''检查页面主要元素显示'''
    def test_title(self):
        '''验证首页标题'''
        #self.assertEqual('慧眼识宝，悦享收藏-中晟在线', self.driver.title)
        assert self.driver.title == '慧眼识宝，悦享收藏-中晟在线'

    def test_searchBoxInfo(self):
        '''验证搜索框的提示文本信息为： 藏品名称 '''
        #self.assertEqual('藏品名称', self.get_infoOfSearchBox())
        assert '藏品名称', self.get_infoOfSearchBox()
    def test_click_searchBox001(self):
        '''验证点击搜索框，显示搜索历史框'''
        self.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_historyBoxP())
        assert self.get_historyBoxP() == 1
    def test_click_searchBox002(self):
        '''验证点击搜索框，历史框包含搜索历史文本'''
        self.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_historyTextP())
        assert self.get_historyTextP() == 1
    def test_click_searchBox003(self):
        '''验证点击搜索框，历史框包含删除按钮'''
        self.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_deleteIcon())
        assert self.get_deleteIcon() == 1
    def test_qrcode(self):
        '''验证页面底部显示 中晟在线 小程序二维码'''
        #self.assertEqual("http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg", self.get_qrcodeP())
        assert self.get_qrcodeP() == "http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg"


class TestFirstp002(Init4, Firstp):
    '''页面顶部及页面中的链接验证'''
    def test_click_help(self):
        '''验证点击页面顶部 帮助中心 ，页面正确跳转'''
        self.click_helpB()
        self.assertEqual('中晟在线-帮助', self.driver.title)
    def test_click_contact(self):
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        self.click_contactB()
        self.assertEqual('中晟在线-联系我们', self.driver.title)
    @unittest.skip('点击首页功能未实现')
    def test_click_firstPage(self):
        '''验证点击页面中间导航栏 首页 ，页面正确跳转'''
        self.click_bid()
        self.click_firstPage()
        self.assertEqual("中晟在线", self.driver.title)
    def test_click_bid(self):
        '''验证点击页面中间导航栏 竞买 ，页面正确跳转'''
        self.click_bid()
        self.assertEqual("中晟在线-竞买", self.driver.title)
    def test_click_specialP(self):
        '''验证点击页面中间导航栏 专场 ，页面正确跳转'''
        self.click_specialP()
        self.assertEqual('中晟在线-拍品专场列表', self.driver.title)
    def test_click_moreCollection(self):
        '''验证点击热卖拍品底部 更多拍品 ，页面正确跳转'''
        self.click_moreCollection()
        self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)
    def test_click_moreCollectionID(self):
        '''验证点击热卖拍品底部 更多拍品后的标识 ，页面正确跳转'''
        self.click_moreCollectionID()
        self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)

class TestFirstp003(Init5, Firstp):
    '''页面中需要先登陆才能进行页面跳转'''
    def test_click_login(self):
        '''验证点击页面顶部 未登录 ，页面弹出登录窗口'''
        self.click_loginB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_apply(self):
        '''验证未登录情况下，点击页面中间导航栏 委托 ，页面弹出登录框'''
        self.click_apply()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_myBid(self):
        '''验证未登录情况下，点击页面顶部 我的竞买 按钮，弹出登录框'''
        self.click_myBidB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_myMsg(self):
        '''验证未登录情况下，点击页面顶部 消息 按钮，弹出登录框'''
        self.click_myMsgB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    @unittest.skip('异常用例')
    def test_click_myApplyB(self):
        '''验证未登录情况下， 点击页面中间 我要申请委托 半隐藏按钮，页面弹出登录框'''
        self.click_myApplyB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))


@unittest.skip('用户未登陆')
class TestFirstp004(Init, Firstp):
    '''用户登陆后的操作'''
    def test_click_login(self):
        '''验证点击页面顶部 未登录 ，页面弹出登录窗口'''
        self.click_loginB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_help(self):
        '''验证点击页面顶部 帮助中心 ，页面正确跳转'''
        self.click_helpB()
        self.assertEqual('中晟在线-帮助', self.driver.title)
    def test_click_contact(self):
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        self.click_contactB()
        self.assertEqual('中晟在线-联系我们', self.driver.title)
    def test_click_firstPage(self):
        '''验证点击页面中间导航栏 首页 ，页面正确跳转'''
        self.click_bid()
        self.click_firstPage()
        self.assertEqual("中晟在线", self.driver.title)
    def test_click_bid(self):
        '''验证点击页面中间导航栏 竞买 ，页面正确跳转'''
        self.click_bid()
        self.assertEqual("中晟在线-竞买", self.driver.title)
    def test_click_apply(self):
        '''验证未登录情况下，点击页面中间导航栏 委托 ，页面弹出登录框'''
        self.click_apply()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_specialP(self):
        '''验证点击页面中间导航栏 专场 ，页面正确跳转'''
        self.click_specialP()
        self.assertEqual('中晟在线-拍品专场列表', self.driver.title)

    def test_click_myBid(self):
        '''验证未登录情况下，点击页面顶部 我的竞买 按钮，弹出登录框'''
        self.click_myBidB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_myMsg(self):
        '''验证未登录情况下，点击页面顶部 消息 按钮，弹出登录框'''
        self.click_myMsgB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))
    def test_click_myApplyB(self):
        '''验证未登录情况下， 点击页面中间 我要申请委托 半隐藏按钮，页面弹出登录框'''
        self.click_myApplyB()
        self.assertIsNotNone(self.driver.find_element(*self.loginBox))

    def test_click_moreCollection(self):
        '''验证点击热卖拍品底部 更多拍品 ，页面正确跳转'''
        self.click_moreCollection()
        self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)
    def test_click_moreCollectionID(self):
        '''验证点击热卖拍品底部 更多拍品后的标识 ，页面正确跳转'''
        self.click_moreCollectionID()
        self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)








class TestFirstp005(Init4,  Firstp):
    '''验证页面底部链接功能'''


    def test_click_guide(self):
        '''验证点击页面底部 新手指南 ，页面正确跳转'''
        self.click_guildL()
        self.assertEqual('中晟在线-帮助', self.driver.title)
        time.sleep(1)
    def test_click_biddingInfo(self):
        '''验证点击页面底部 竞买须知 ，页面正确跳转'''
        self.click_biddingInfo()
        #self.assertEqual('竞买须知', self.driver.title)
        self.assertEqual('http://home.online.zspaimai.cn/article?keywords=bidding_information',self.driver.current_url)
    def test_click_aboutUs(self):
        '''验证点击页面底部 关于我们 ，页面正确跳转'''
        self.click_aboutUs()
        self.assertEqual('http://home.online.zspaimai.cn/article?keywords=about_us', self.driver.current_url)
    def test_click_serviceA(self):
        '''验证点击页面底部 服务协议 ，页面正确跳转'''
        self.click_serviceA()
        self.assertEqual('http://home.online.zspaimai.cn/article?keywords=user_agreement', self.driver.current_url)
    def test_click_collectionGuarantee(self):
        '''验证点击页面底部 藏品保障 ，页面正确跳转'''
        self.click_collectionGuarantee()
        self.assertEqual('http://home.online.zspaimai.cn/article?keywords=collection_guarantee', self.driver.current_url)

    def test_click_contactUs(self):
        '''验证点击页面底部 联系我们 ，页面正确跳转'''
        self.click_contactUs()
        self.assertEqual('http://home.online.zspaimai.cn/article/contact', self.driver.current_url)
        time.sleep(3)


    def test_click_ipL(self):
        '''验证点击页面底部的 粤ICP备2021041206号 链接，正确打开页面'''
        self.click_ipL()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        self.assertEqual('https://beian.miit.gov.cn/#/Integrated/index', self.driver.current_url)

class TestFirstp007(Init,  Firstp):
    '''验证页面底部链接功能'''
    def test_click_ipL(self):
        '''验证点击页面底部的 粤ICP备2021041206号 链接，正确打开页面'''
        self.click_ipL()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        self.assertEqual('https://beian.miit.gov.cn/#/Integrated/index', self.driver.current_url)
        self.driver.close()


@unittest.skip('搜索功能代码暂未完成')
class TestFirstp006(Init5, Firstp):
    '''验证搜索功能'''
    def test_search_001(self):
        '''验证搜索功能'''
        self.send_search_info('一张图片')
        self.click_searchButton()
        self.assertEqual('中晟在线-搜索结果', self.driver.title)
    def test_search_002(self):
        '''验证搜索结束后，关键字保存到搜索历史中'''
        self.click_searchBox()
        self.assertEqual('一张图片', self.get_lastReco())
    def test_search_000(self):
        '''验证点击历史框中到 删除按钮，删除历史数据'''
        pass






@pytest.fixture
def order():
    return []


@pytest.fixture
def outer(order, inner):
    order.append("outer")


class TestOne:
    @pytest.fixture
    def inner(self, order):
        order.append("one")

    def test_order(self, order, outer):
        assert order == ["one", "outer"]


class TestTwo:
    @pytest.fixture
    def inner(self, order):
        order.append("two")

    def test_order(self, order, outer):
        assert order == ["two", "outer"]



# @pytest.fixture(scope='function', autouse=True, name='s')
# def init(drivers):
#     """打开百度"""
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get('http://home.online.zspaimai.cn')


# @pytest.mark.usefixtures("s")
class TestFirstp010:
    '''检查页面主要元素显示'''
    '''http://home.online.zspaimai.cn'''

    # def test_title(self):
    #     '''验证首页标题'''
    #     #self.assertEqual('慧眼识宝，悦享收藏-中晟在线', self.driver.title)
    #     assert self.driver.title == '慧眼识宝，悦享收藏-中晟在线'
    # fp = Firstp()
    #
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('http://home.online.zspaimai.cn')

    def teardown_class(self):
        self.driver.quit()







    def test_searchBoxInfo(self):
        '''验证搜索框的提示文本信息为： 藏品名称 '''
        fp = Firstp(self.driver)
        #self.assertEqual('藏品名称', self.get_infoOfSearchBox())
        assert '藏品名称'== fp.get_infoOfSearchBox()
    def test_click_searchBox001(self):
        '''验证点击搜索框，显示搜索历史框'''
        fp = Firstp(self.driver)
        fp.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_historyBoxP())
        assert fp.get_historyBoxP() == 1
    def test_click_searchBox002(self):
        '''验证点击搜索框，历史框包含搜索历史文本'''
        fp = Firstp(self.driver)
        fp.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_historyTextP())
        assert fp.get_historyTextP() == 1
    def test_click_searchBox003(self):
        '''验证点击搜索框，历史框包含删除按钮'''
        fp = Firstp(self.driver)
        fp.click_searchBox()
        time.sleep(5)
        #self.assertTrue(self.get_deleteIcon())
        assert fp.get_deleteIcon() == 1
    def test_qrcode(self):
        '''验证页面底部显示 中晟在线 小程序二维码'''
        fp = Firstp(self.driver)
        #self.assertEqual("http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg", self.get_qrcodeP())
        assert fp.get_qrcodeP() == "http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg"


if __name__ == '__main__':
    unittest.main(verbosity=2)
