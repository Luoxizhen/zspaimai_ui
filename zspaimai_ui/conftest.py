'''conftest.py测试框架pytest的胶水文件，里面用到了fixture的方法，封装并传递出了driver。
全局用例共用'''
import pytest
from py.xml import html
from selenium import webdriver
from interface_test import goods_test,topic_test
from utils import times,util
from common.readpagedata import Pagedata
from interface_base.topic import add_topic_goods

#
# driver = None
#
#
# @pytest.fixture(scope='session', autouse=True)
# def drivers(request):
#     global driver
#     if driver is None:
#         driver = webdriver.Chrome()
#         driver.maximize_window()
#
#     def fn():
#         driver.quit()
#
#     request.addfinalizer(fn)
#     return driver
# #

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        # xfail = hasattr(report, 'wasxfail')
        # if (report.skipped and xfail) or (report.failed and not xfail):
        #     file_name = report.nodeid.replace("::", "_") + ".png"
        #     # screen_img = _capture_screenshot()
        #     if file_name:
        #         html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
        #                'onclick="window.open(this.src)" align="right"/></div>' % screen_img
        #         extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


# def _capture_screenshot():
#     '''
#     截图保存为base64
#     :return:
#     '''
#     return driver.get_screenshot_as_base64()
def pytest_configure(config):
    # 添加接口地址和项目名称
    config._metadata['项目名称'] = '中晟在线'
    config._metadata['接口地址'] = 'http://home.online.zspaimai.cn/'

@pytest.fixture(scope='session',autouse=True)
def add_goods():
    '''将原首页推荐的拍品取消推荐，并创建8个拍品，逐个开拍，逐个结拍'''
    goods_test.goods_unrecommend()
    # goods_test.goods_add_recommend()
    pd = Pagedata('firstp')
    new_goods_info = pd.data['goods']
    #拍品的时间
    now = round(times.timestamp())
    good_ids = []
    for i in range(1,9):
        name = 'good' + str(i)
        begin_time = now + 3600 * (i-1)
        end_time = begin_time + 86400 * i
        new_goods_info[name]['begin_time'] = begin_time
        new_goods_info[name]['end_time'] = end_time
        good_info = new_goods_info[name]
        good_id = goods_test.goods_add_recommend(**good_info)
        new_goods_info[name]['begin_time'] = times.time_to_str(begin_time)
        new_goods_info[name]['end_time'] = times.time_to_str(end_time)
        good_ids.append(good_id)
    info = pd.data['info']
    info['good_ids'] = good_ids
    info['time'] = now
    pd.setitem('goods',new_goods_info)
    pd.setitem('info',info)
@pytest.fixture(scope='session',autouse=True)
def add_topic():
    '''将首页推荐的专场取消推荐，并创建2个专场，并首页推荐'''
    topic_test.list_unrecommend()
    pd = Pagedata('firstp')
    time = pd['info']['time']
    new_topics_info = pd.data['topics']
    topic_ids = []
    for i in range(1, 6):
        name = 'topic' + str(i)
        begin_time = time + 3600 * (i - 1)
        end_time = begin_time + 86400 * i
        new_topics_info[name]['begin_time'] = begin_time
        new_topics_info[name]['end_time'] = end_time
        topic_info = new_topics_info[name]
        topic_id = topic_test.add_recommend(**topic_info)
        new_topics_info[name]['begin_time'] = times.time_to_str(begin_time)
        new_topics_info[name]['end_time'] = times.time_to_str(end_time)
        topic_ids.append(topic_id)
    info = pd.data['info']
    info['topic_ids'] = topic_ids
    pd.setitem('topics', new_topics_info)
    pd.setitem('info', info)
@pytest.fixture(scope='session',autouse=True)
def topic_add_goods():
    '''在首页推荐的第一个专场中添加首页推荐的8个拍品'''
    info = Pagedata('firstp')['info']
    good_ids = info['good_ids']
    topic_ids = info['topic_ids']
    goods = []
    for i in range(8):
        good_info = {'goods_id':good_ids[i],'is_recommended':1}
        goods.append(good_info)
    print(goods)
    str1 = util.object_to_str(*goods)
    topic_good_info = {"topic_id": topic_ids[0],'goods':str1}
    print(topic_good_info)
    print(add_topic_goods(**topic_good_info).json())