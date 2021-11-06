import time
import unittest
from selenium import webdriver
from utils.rwcfg import ReadCfg

from page.firstp import Firstp
from page.zslogin import Login
#url='http://home.online.zspaimai.cn/'
url = 'http://home.online.zspaimai.cn/'

class Init(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get(url)
        self.driver.find_element_by_xpath('//img[@class="cursor close"]').click()

    def tearDown(self) -> None:
        self.driver.quit()
class Init2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

class Init3(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
class Init4(unittest.TestCase):
    def tearDown(self) -> None:
        time.sleep(3)
        #self.driver.back()
    def setUp(self) -> None:
        self.driver.get(url)
        time.sleep(3)
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//img[@class="cursor close"]').click()
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
class Init5(unittest.TestCase):
    def setUp(self) -> None:
        time.sleep(2)
    def tearDown(self) -> None:
        time.sleep(1)
        self.driver.find_element_by_xpath('//img[@class="login-title-close"]').click()
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//img[@class="cursor close"]').click()
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
class TestLoginInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//div[text()="未登录"]').click()
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
class TestLoginInit002(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//div[text()="未登录"]').click()
    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
class TestApplyInit001(unittest.TestCase,Firstp,Login):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//img[@class="cursor close"]').click()
        # cls.click_loginB()
        # cls.click_loginTypeNo()
        # cls.send_phone('15622145010')
        # cls.send_pw('123456')
        # cls.click_lb()
        # cls.click_myApplyB()


    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
    def setUp(self) -> None:
        self.click_loginB()
        self.click_loginTypeNo()
        self.send_phone('15622145010')
        self.send_pw('123456')
        self.click_lb()
        time.sleep(5)
        self.click_myApplyB()

    def switch_window(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
class TestMyApplyInit001(unittest.TestCase,Firstp,Login):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.driver.get(url)
        cls.driver.find_element_by_xpath('//img[@class="cursor close"]').click()



    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
    def login(self) -> None:
        self.click_loginB()
        self.click_loginTypeNo()
        self.send_phone('15622145010')
        self.send_pw('123456')
        self.click_lb()
        time.sleep(5)

        self.click_myApplyB()

    def switch_window(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
