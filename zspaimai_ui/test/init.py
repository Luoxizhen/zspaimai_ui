import time
import unittest
from selenium import webdriver
from config.readCfg import ReadCfg
#url='http://home.online.zspaimai.cn/'
url = ReadCfg().readCfg()

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