'''所有的目录配置信息写在这个文件里面'''
import os
from selenium.webdriver.common.by import By
from utils.times import dt_strftime

class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')
    # 测试数据路径
    WEB_DATA_PATH = os.path.join(BASE_DIR, 'data')
    # 接口数据路径
    INTERFACE_DATA_PATH = os.path.join(BASE_DIR, 'interface_data')
    # 接口包头文件路径
    INTERFACE_HEADER_PATH_OFFLINE = os.path.join(BASE_DIR,'interface_headers_offline')
    INTERFACE_HEADER_PATH_ONLINE = os.path.join(BASE_DIR, 'interface_headers_online')
    # 报告文件
    report_name = "report_" + dt_strftime(fmt="%Y%m%d_%H%M%S") + '.html'
    REPORT_FILE = os.path.join(BASE_DIR, 'report', report_name)
    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link': By.LINK_TEXT
    }
    # 邮件信息
    EMAIL_INFO = {
        'username': '1084502012@qq.com',  # 切换成你自己的地址
        'password': 'QQ邮箱授权码',
        'smtp_host': 'smtp.qq.com',
        'smtp_port': 465
    }
    # 收件人
    ADDRESSEE = [
        '1084502012@qq.com',
    ]
    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime(fmt="%Y%m%d_%H%M%S")))
    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'cfg.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file
cm = ConfigManager()
if __name__ == '__main__':
    print(cm.INTERFACE_HEADER_PATH_ONLINE)