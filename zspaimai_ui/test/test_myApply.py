import time
import unittest
from selenium import webdriver
from page.myApplyP import MyApplyp
import test.init as init




class ATestMyApply001(init.TestMyApplyInit001, MyApplyp):
    def test_001(self):
        self.login()
        self.click_entrust()

    def test_002(self):
        self.click_applyNow()
    def test_003(self):
        self.click_settlementList
    def test_004(self):
        self.click_collection()


class TestMyApply002():

    def test_001(self):
        self.login()
        self.click_entrust()

    def test_002(self):
        self.click_applyNow()
    def test_003(self):
        self.click_settlementList()
    def test_004(self):
        self.click_collection()