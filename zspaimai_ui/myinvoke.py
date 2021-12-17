# content of myinvoke.py
import pytest
import pyhtml
from utils import times
# from pyhtml import *deff_links(ctx): fortitle, page in[('Home','/home.html'),('Login','/login.html')]:yield li(a(href=page)(title)) t=html(head(title('Awesome website'),script(src="http://path.to/script.js")),body(header(img(src='/path/to/logo.png'),nav(ul(f_links))),div(lambdactx:"Hello %s"%ctx.get('user','Guest'),'Content here'),footer(hr,'Copyright 2013'))) print t.render(user='Cenk')
python_file = "test/test_firstp.py"

class MyPlugin(object):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls,*args,**kwargs)

    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


'''pytest 生成报告的4种方法
1、生成junitxml 报告，--juint-xml=report/test.xml
2、生成resultlog 文件，--result-log=report/test.log
3、生成allure报告，--alluredir= ,先安装 pip install allure-pytest
4、生成html 报告, --html=reports/report.html,现在安装pip install pytest-html'''


'''默认报生成方式'''
#pytest.main(["-x", "test/test_firstp.py::test_111", "--junitxml=reports/result1.xml"], plugins=[MyPlugin()])
'''html 报告格式生成方式'''
if __name__ == "__main__":
    pytest.main(["test/test_firstp.py",
                 "test/test_detail.py",
                 "test/test_mybid.py",
                 "test/test_order_detail.py",
                 "--html=reports/中晟在线web端自动化测试报告.html"])

#pytest.main(["test/test_detail.py"], plugins=[MyPlugin()])