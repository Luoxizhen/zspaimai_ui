import unittest

import os
import sys
import time

import test.test_login
from test.test_myApply import TestMyApply001
from test.test_apply import TestApply001
from test.test_firstp import TestFirstp001
import test.test_firstp as tc
from BeautifulReport import BeautifulReport
timestamp = time.strftime('%Y%m%d%H%M%S')

curpath = os.path.dirname(os.path.realpath(__file__))
casepath = os.path.join(curpath, 'test')
reportpath = curpath + '/reports/首页基本功能测试' +timestamp + '.txt'
reportDir = os.path.join(curpath, 'reports')

def allcases():
    disc = unittest.defaultTestLoader.discover(casepath, 'test_f*.py')
    return disc
def fp():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestMyApply001)
    return suit
if __name__ == '__main__':
    runner = unittest.runner.TextTestRunner(verbosity=2)
    runner.run(fp())
    # result = BeautifulReport(fp())
    # result.report(description='中晟拍卖微信登陆测试报告', report_dir=reportDir, filename='中晟拍卖微信登陆 测试报告')

