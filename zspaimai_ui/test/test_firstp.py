import time
import unittest
import pytest
from selenium import webdriver
from page.firstp import Firstp
from test.init import Init2, Init3, Init4, Init5, Init
from common.readconfig import ini

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
        self.assertEqual('中晟在线-联系我们1', self.driver.title)
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
class TestFirstp0021:
    url = "http://home.online.zspaimai.cn"
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('http://home.online.zspaimai.cn')

    def teardown_class(self):
        self.driver.quit()
    # @pytest.mark.skip()

    # def test_click_moreCollection(self):
    #     '''验证点击热卖拍品底部 更多拍品 ，页面正确跳转'''
    #     self.click_moreCollection()
    #     self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)
    # def test_click_moreCollectionID(self):
    #     '''验证点击热卖拍品底部 更多拍品后的标识 ，页面正确跳转'''
    #     self.click_moreCollectionID()
    #     self.assertEqual('http://home.online.zspaimai.cn/auction?category_id=0', self.driver.current_url)
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
@pytest.mark.skip()
class TestFirstp201:
    '''检查页面主要元素显示'''
    '''http://home.online.zspaimai.cn'''

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        print(ini.url)
        self.driver.get(ini.url)

    def teardown_class(self):
        self.driver.quit()

    def test_title(self):
        '''验证首页标题'''
        assert self.driver.title == '慧眼识宝，悦享收藏-中晟在线'


    def test_searchBoxInfo(self):
        '''验证搜索框的提示文本信息为： 藏品名称 '''
        fp = Firstp(self.driver)
        #self.assertEqual('藏品名称', self.get_infoOfSearchBox())
        assert '藏品名称' == fp.info_of_search_box()
    def test_show_search_history_box(self):
        '''验证点击搜索框，显示搜索历史框'''
        fp = Firstp(self.driver)
        fp.click_search_box()
        time.sleep(5)
        #self.assertTrue(self.get_historyBoxP())
        assert fp.is_display_search_history_box() == 1

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
    def test_qrcode_app(self):
        '''验证页面底部显示 中晟在线 小程序二维码'''
        fp = Firstp(self.driver)
        #self.assertEqual("http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg", self.get_qrcodeP())
        assert fp.src_qrcode_app() == "http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg"
    def test_qrcode_zsonline(self):
        '''验证页面底部显示 中晟在线 二维码'''
        fp = Firstp(self.driver)
        src = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wgARCAFYAVgDAREAAhEBAxEB/8QAHQABAQEAAgMBAQAAAAAAAAAAAAkBAggDBAcGBf/EABQBAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhADEAAAAO1IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABhoAAAMNAMNAABhoAAAAAJVgAAFVACVYKqAEqwCqhKwqmSrKqErCqZKsFVACVYAABVQAAEqyqgABKsqoSrKqErSqQAJVgqoCVhVMlWCqhKsAqoSrKqEqyqgABKsqoAACVZVQlYAVTJVlVCVZpVIErjDTDCqhK0qiSuOJpVI0lWCqhKsqoSrKpkrQCqZKsqoAACVZVQlWAVUJVlVCVZpVI0AlaYVTJWFUiVpVMErQVSJVnIqiStKpkqyqhKsAqoSrKqAAAlWVUJVgFVCVZVQlWVUAJVlVASsKpgErCqYAJVgqoACVZVQlWAVUJVlVAAASrKqAAErSqRKsqoCVYBVQAlWAVUJVlVAAASrKqErSqQABKsqoAACVZoABpVIlWVUJWlUSVhVQlaVRJXFUiVpVElcVSJWlUSVpVMlaVSJVlVCVhpgBoKpAAAAw0AAEqyqgJVlVCVhVI0ErQcSqhhpKsqoCVphVMw0AAAAAAErCqYJVgAFVASrKqEqzSqZKs0qmSrBVQEqyqgAJVlVCVYABVQAAAEqwVUJVgqoSsKpglWCqhKsAqoSrKqAlWVUJWlUiVZVQErCqYJVgqoSrKqAlWVUAAMJWmAqmaSsNKokriqRKwGlUgStKpErDSqRKs0FUwASsKpkrDTCqYMJXHEqoAACVZVQErCqYMBpKw0qkCVhVIErSqZK0HEAqmaCVpVIAAEqyqhhK4qkAACVZVQErCqYJWFUyVYKqEqwVUBKsAqoSrABpVMAAlWCqgJVlVCVYKqAAAlWVUBKwqmSrKqAEqyqgBKw+sHfk6cg7jHTk7kHTU/HnyYqmSrKqAlWAVUAJWlUiVZVQAAEqzSqQNBK4qiAStKokrj6wd5z2gAAD1T+icgYSuOIOQKpErDSqRKsqoAAYStMOQKpErCqRK4qkSsNMMOxR3BPZAAAPVOoB11KpkrSqJK4wqkaCVhVIGgAAAlWCqhKsAqoASrAKpHqHuGmGnhPMYeucyWJVQEqwVUJWlUgASsKpgAAAEqwAVUJWFUyVZpVMHA/Bnpn6E+Vn2w+bn0Q+fHtn0UlkCqhKsAAqoCVZVQlWVUAAAJWGmGA5FUTQStBVI4H5A909U/LH7A/EH7w/gnpnwM7kglacQDQVTBK0qkSrKqAAAAlaVSJVmlUjQCVphVM4H8k/MnI9o9c08Z/ZMP75LQqkYSuOJpVEleYYVUJWgqkAACVYORVIlWVUJVgqoSrKqAHA9c8wOBpyOJp4jyHnJVlVASrKqErSqQJVlVCVhVMAAAEqyqhKwqmACVZVQErDDsWdwD2QAAD1jp+ddAVUJWFUyVYBVQlWCqgAAABKsqoYStKpkrQDDQVSPGege0AAAeqdGD5KaaCqQJWgwqmDCVxVIAAwlcYaVRJWgqkaCVZVQlaVSOB/MPVOq52nOrB2mNB5D+secGErQDQVSJWFUSWBVEAAAAErCqZKsAAqoASrBVIAAA00lWCqgAJWFUyVZVQlWAVUAAAAJWFUyVZVQlYVTBKsqoSrAKqEqyqhKwqmAStKpEqyqhKsFVCVZVQlYVTJVlVCVYKqAAGErjDQVSBK0FUgStKpEqyqgJWgqkYaCVhpVIlWaVRJXlUiVZVQlYVTBK0qiSuKpAAAAlaCqRKwqkCVxVIwlccTQaVSJVlVACVZVQlaYVTJWg4lVCVpVIErCqRK4wqmAACVYNKpglWCqgBKwqmSrKqAAlWVUBKsFVAACVYAAKqAAAAAAAAAlWVUJWlUiVZVQlYVTABKsFVCVpVIlWCqgJVlVACVYKqEqwVUAAMJWgAAFUyVZpVIlcVSBhK4wqmACVhVElecQVUBKsqoStKpEqwciqJK0qmAACVZVQAAlYVSJWlUyVpVElcVSMBK4w0qiaDASuKpErTDCqgBKs0qkStKpgAAEqyqhKsAqoSrKqAlWVUJWFUwSrABVQEqwVUJVgqoSrAAAKqAlYVTAAAJVlVCVYBVQlWVUBKsAAqoSsKpglaVSJVlVAAAAASsKpkqwVUJVlVAAASrKqErTiCqhKsqmSuMKpAlaVTJWgqkSsKokrwYaYAVSNJWAqkCVoKpErgVSAABKsqoAAStKpAErQVSBhK4wGgqkSrBVQAlaVRJWFVACVZVQAAAAEqwAAciqQBKs0wqoSsKpgAlYVTJVgqoASrAKqEqwAVUBKsqoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/xABGEAABAgMDBQgNDAMBAAAAAAABAgMABBEFEhMUITFRYgcyQVCBkrHSBhAXMzVCQ1NVdKGiwhUWIiMwUmFwcYCRwSAkQLL/2gAIAQEAAT8B/eOPz6sHc1t63mEzKGkSrC9C5g0rydruJ2z6RkPe6sdxO2fSMh73V7XcUtn0jIe91e13FLZ9IyHv9WLd3NbesJhUwtpuaYRpWxnpycRbmtgtW92SoRMpvsS6C+tB4c+b2wkGYKlFSggGgAzRgI2+cYwEbfOMYCNvnmMBG3zzGAjb55jARt88xk6NrnGLplyCCooJAKVGv8cRbinh+e9V+IRL975VdJ+wf73yjpjdr8PyPqvxK4h8aG1pbZUpRupBUSTwZzA7Ve0VpBCSQCdH49t/vfKnpjynJxD40TM3Ous2lKol2FtoCheU5TMRqpElPz7TVlM40jddCEkCpXdux2RKuWU7RdxVU3TepwwuZaVOIZecU+L6FKOJfFK7NYcfdMviyraXCdAWq5/UOzFpTkw1af8Aq4LK8FoCqwSo0vjREoibQF5VMtvnguN3LvtMO2q7Ov2izgTC0LaKbh+jhppmOfWeiLCtFUyN/VtxLd1F9S7h4c9M0eU5OIfGiasiRWxNzbkslbpQupUK6KxY0jLsWfKlEs0heCipCKGtItdp6fWmXabWUtHFUd7U8CQYTZc+vBfwnhc7+kufTcF68Ej9IaC7Yl1Y6HmG75BbIulafxhuSyuzm202dOH6yt29dRS/qrFmtGWvNIs7JWt9vwamDZqg+t/5NDmIu8UvLvlR/wDKYlZKasl766XxsRaQ2preMpK86af3G7X4fkfVfiV/1D/PxofmhJSS5haSUoJKqar0fOpGT4+RvXa3KcNaV6I+dKMRpvJHSp7Oj9DvTyw/2RNtTDrTaW3sNIVeS6IV2UNBsrDFQEXqX8+9vaNWbTBt1zKkNYVwZ0qGnxkdaPnSkMhwyqhWhAv8BBP9Q7bDaJwSyQk/RvE36a9GvRElaPylLleDhUwzStcxoY8pycQ+NDIq0QdaukxcTqEXE/dEYLXm0fxGEj7idFNHBGGn7ojCQRS6n+Iw0VrdFf0h1IS3m1p6Y8pycQ7ifh+e9V+IRL7zlPT9g/3vlHTG7X4fkfVfiPEJN2Eky5IKVFBNQU54yhG1zTGOjb5hjHRt8wxjo2+YYx0bfMMY6NvmGMoRt8wwpRmCAEqCAQSoilY3SbdZt7slWqWXfYl0BhC9emvt4hULwhWO1vM41GMrnPNNx3a7Z9HSHvdaMrnPNtx3a7Y9HSHvdaMsnPNte2MsnPNtRlc55tuBlD2ZZujZhtFxNOI7o1RdGoRdGoRdGqKDUIujUIujUIp+84fmT//EACsQAQACAQMDAwMFAAMAAAAAAAEAERAgMFEhMdFAQfBhgfFQcZHB4WBwsf/aAAgBAQABPxD/AIybRekyaDYL/QL0X6+zY59VesqAm5WDaIeiGMMe14ohCc6AuGKPVgGaxzqrVR6+zYs9SNYvXZppwyzLPpD0tZMVoMGl0qywxUqVLhs3umbfUWa+Zz+h1pIaag1qNBLwFGecDWDf50kMEqENFGtn1hisGjrvXo50UaOdJivSWStizBANVbtfJRanWryMMGJgoxIViLe18qBlOyNm4QJUMmbMlZqA1UAeRUcEF9TSiqUvUQOhRPk88+bzz5PLPk8s+Tyz5PLPj88UPixS2hTb3Sy0riocOGBqIYvXegqEMkI3UvO4pbFC/n7cTcx0ELhghg1UbIUagB0xAAuV7BEJYlMsiAtSEdyaFQUFtHvR1xYCyj8XbHt+O7itmiXvcys04Gyf0Y6K69i1KK37keiKnTXVtAaKUGOsnBBVClKgP3If/riLuoJqVSXAZXFYU+6qROElZQNgyv3tNBHRIiHFLsq5+7DBWspJFdAWX6E0JLMEiglUtd1ajGuu+39nPPoiN1K2LKceX/pG3aWHoJQ2DHu9DERtULVgH0XqkNwJatrVEu5lq22Ee1M7qXDMC9wugW6g23VXGp0KdctQRBqwalcTXYe9FIK3R3udRd7Twg0tAAXahACivWjGwiA2lMDEZZoqVovYI6CW0USsf0Z7lx8Fwte9FtSvpRu6OiGV97KSVqlKXpHiC7ileq0AVa81cfI4wOsVBFoKPYMaIO2Y7AEehSO+kV/rwaQiqANMBliFCSrUUOqhVglS/EkKNxNsD2QSP+33cOOmCGioW2+kCif0YZARJEuyXSr3r7HequB8gANHQOwftO97xT0/x27Tqj1Cjo6cIW31Ds0WdvBG0MFUITp26fSXXqLpRZfen6zoxXF9AEfl+7uc7fOxTl+i/n17Hw/p0787Fm3TshUKirwsW8c5pbaIdTqrdJTPj8c+Twz5PDPk8M+Twz5PDPi8MU8dqwbAGnuCtVUM6WFVVX8lg0OC6nO9eCEqVmisGpOsGewKh+yIxCwo+/nEx/nvnG3xvKfhnzD/AD3zH0z2UCCfVVffmGXAhPZx98GAIQhbg1UaOdfOAoy8L+J+En4CfQQnfhJ+EgDYvcs0c55nO3XoOd+zTeLwZrhyTrLwQs0XOdthHFFOCGgdRoMVsmDctwFGaM3qCjVzmtmjYs369JzsVsGCBDpcNZggQelanBvEqVKJewXkxcME666yQ9yc+i5nP6dzOdsSWZsnPpSGWWZIENRDJCU4IblStgYNVGTWS8mD0t6ef+lv/8QAFBEBAAAAAAAAAAAAAAAAAAAAoP/aAAgBAgEBPwBnP//EABQRAQAAAAAAAAAAAAAAAAAAAKD/2gAIAQMBAT8AZz//2Q=="
        assert fp.src_qrcode_zsonline() == src
    def test_qrcode_phone(self):
        '''验证页面顶部显示 中晟在线 小程序二维码'''
        fp = Firstp(self.driver)
        #self.assertEqual("http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg", self.get_qrcodeP())
        assert fp.src_qrcode_phone() == "http://home.online.zspaimai.cn/assets/img/mini-qrcode.563407c6.jpg"
    @pytest.mark.header
    def test_qrcode_phone_show(self):
        '''验证点击移动端，显示小程序二维码'''
        fp = Firstp(self.driver)
        fp.click_mobile()
        assert fp.is_display_qrcode_phone() == 1

    @pytest.mark.header
    def test_click_help(self):
        '''验证点击页面顶部 帮助中心 ，页面正确跳转'''
        fp = Firstp(self.driver)
        fp.click_help_button()
        title = self.driver.title
        fp.back()
        assert '中晟在线-帮助' == title

    @pytest.mark.header
    def test_click_contact(self):
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        fp = Firstp(self.driver)
        fp.click_contact_button()
        title = self.driver.title
        fp.back()
        assert '中晟在线-联系我们' == title

    @pytest.mark.header
    def test_click_login(self):
        '''验证点击页面顶部 登陆，页面显示登陆框'''
        fp = Firstp(self.driver)
        fp.click_login()
        is_dispaly = fp.is_display_login_box()
        fp.close_login_box()
        assert is_dispaly == 1


    @pytest.mark.skip()
    @pytest.mark.nav
    def test_click_firstPage(self):
        '''验证点击页面中间导航栏 首页 ，页面正确跳转'''
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        fp = Firstp(self.driver)
        fp.click_first_page()
        title = self.driver.title

        assert '慧眼识宝，悦享收藏-中晟在线' == title

    # @pytest.mark.skip()
    @pytest.mark.nav
    def test_click_bid(self):
        '''验证点击页面中间导航栏 竞买 ，页面正确跳转'''
        '''验证点击页面顶部 联系我们 ，页面正确跳转'''
        fp = Firstp(self.driver)
        fp.click_bidding()
        title = self.driver.title
        fp.back()
        assert '中晟在线-竞买' == title

    # @pytest.mark.skip()
    @pytest.mark.nav
    def test_click_specialP(self):
        '''验证点击页面中间导航栏 专场 ，页面正确跳转'''
        fp = Firstp(self.driver)
        fp.click_special()
        title = self.driver.title
        fp.back()
        assert '中晟在线-拍品专场列表' == title

    @pytest.mark.nav
    def test_click_apply(self):
        '''验证点击页面中间导航栏 专场 ，在未登陆情况下，页面显示登陆框'''
        fp = Firstp(self.driver)
        fp.click_applying()
        is_display = fp.is_display_login_box()
        fp.close_login_box()
        assert is_display == 1
    @pytest.mark.login
    def test_click_my_bid(self):
        '''验证点击我的竞买按钮，弹出登陆框'''
        fp = Firstp(self.driver)
        fp.click_my_bid_button()
        is_display = fp.is_display_login_box()
        fp.close_login_box()
        assert is_display == 1

    @pytest.mark.login
    def test_click_msg(self):
        '''验证点击消息按钮，弹出登陆框'''
        fp = Firstp(self.driver)
        fp.click_message()
        is_display = fp.is_display_login_box()
        fp.close_login_box()
        assert is_display == 1
    @pytest.mark.login
    def test_login_title(self):
        '''验证登陆框标题： 中晟在线'''
        fp = Firstp(self.driver)
        fp.click_login()
        title = fp.login_title()
        fp.close_login_box()
        assert title == "中晟在线"


@pytest.fixture(scope='class',name="setup")
def firstp_setup():
    driver = webdriver.Chrome()
    driver.maximize_window()

    return driver





@pytest.mark.usefixtures("setup")
class TestLogin:
    '''登陆登出'''
    @pytest.fixture(scope="function")
    def open(self):
        fp = Firstp(firstp_setup)
        fp.get_url(ini.url)


    def test_login(self):
        fp = Firstp(firstp_setup)
        fp.click_login()
        time.sleep(5)




    def login_num(self):
        pass







if __name__ == '__main__':
    unittest.main(verbosity=2)
