import configparser
import os






class ReadCfg():
    def __init__(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        cfgpath = os.path.join(curpath, "cfg.ini")

        self.conf = configparser.ConfigParser()
        self.conf.read(cfgpath, encoding="utf-8")
    def readCfg(self):
        print(self.conf.get('sys_variables','url'))
        return self.conf.get('sys_variables','url')

