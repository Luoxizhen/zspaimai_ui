import unittest

import os
import sys
import time

import test.test_login
from test.test_firstp import TestFirstp001
import test.test_firstp as tc
from BeautifulReport import BeautifulReport
timestamp = time.strftime('%Y%m%d%H%M%S')

curpath = os.path.dirname(os.path.realpath(__file__))
casepath = os.path.join(curpath, 'test')
reportpath = curpath + '/reports/首页基本功能测试' +timestamp + '.txt'
reportDir = os.path.join(curpath, 'reports')
print(curpath)

print(reportpath)
def allcases():
    disc = unittest.defaultTestLoader.discover(casepath, 'test_f*.py')
    return disc
def fp():
    suit = unittest.TestLoader().loadTestsFromTestCase(test.test_login.TestLogin_005)
    return suit
if __name__ == '__main__':
    # runner = HtmlTestRunner.HTMLTestRunner(verbosity=2,report_name='首页测试报告')
    # runner.run(allcases())
    result = BeautifulReport(fp())
    result.report(description='中晟拍卖微信登陆测试报告', report_dir=reportDir, filename='中晟拍卖微信登陆 测试报告')

    # with open(file=reportpath, mode='a', encoding='utf-8') as file:
    #     result = BeautifulReport(fp())
    #     result.report()



    #     runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=2)
    #     runner.run(allcases())
        # runner1 = HTMLReport.TestRunner()
        # runner1.run(allcases)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/