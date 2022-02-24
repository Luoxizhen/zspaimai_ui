import logging
from config.cfg import cm
class Log:
    def __init__(self):
        self.logger = logging.getLogger()
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

        # 创建一个handle 写入文件
        fh = logging.FileHandler(cm.log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 创建一个handle 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        # 定义输出到格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 添加到handle
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def fmt(self):
        return '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'
log = Log().logger
if __name__ == "__main__":
    log.info('helloworld')