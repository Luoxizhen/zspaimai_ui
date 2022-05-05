import os
from selenium.webdriver.common.by import By
from utils.times import dt_strftime
class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 网络爬取数据保存位置
    WEB_DATA_DIR = os.path.join(BASE_DIR, 'web_data')
    DATA_OUTPUT = os.path.join(BASE_DIR, 'data_output')
    # 元素定位类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link': By.LINK_TEXT
    }
    @property
    def log_file(self):
        '''日志目录'''
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime(fmt="%Y%m%d")))
cm = ConfigManager()
if __name__ == '__main__':
    print(cm.WEB_DATA_DIR)