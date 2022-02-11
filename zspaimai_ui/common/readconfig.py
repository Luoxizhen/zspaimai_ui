#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
from config.conf import cm

# HOST = 'HOST_ONLINE'


class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def host(self):
        """接口url """
        sys_inv = self.env
        if sys_inv == 'offline':
            HOST = 'HOST_OFFLINE'
        else:
            HOST = 'HOST_ONLINE'

        return self._get(HOST, 'HOST')
    @property
    def env(self):
        """读环境配置"""
        return self._get('SYS_INVIRONMENT','SYS_INVIRONMENT')


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.host)
