#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import pytest
from utils.log import log
from common.readconfig import ini
from page.searchpage import SearchPage
from selenium import webdriver

class TestSearch:
    # @pytest.fixture(scope='function', autouse=True)
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('https://www.baidu.com/')

    def teardown_class(self):
        self.driver.quit()
    def open_baidu(self):
        """打开百度"""
        search = SearchPage(self.driver)
        search.get_url(ini.url)

    def test_001(self):
        """搜索"""
        search = SearchPage(self.driver)
        search.input_search("selenium")
        search.click_search()
        result = re.search(r'selenium', search.get_source)
        log.info(result)
        assert result

    def test_002(self):
        """测试搜索候选"""
        search = SearchPage(self.driver)
        search.input_search("selenium")
        log.info(list(search.imagine))
        assert all(["selenium" in i for i in search.imagine])


if __name__ == '__main__':
    pytest.main(['test/test_search.py'])