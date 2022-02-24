import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re
from config.cfg import cm
import os
'''
DataOutput
'''
class DataOutput(object):
    def __init__(self):
        self.datas = []  #可以将数据暂存在这个列表里


    #每个循环调用一次此函数，暂存数据
    def store_data(self, data):
        if data is None:
            print ("data is None")
            return

        self.datas.extend(data)
    #全部页面爬取结束后调用此函数，写入文件
    def output_html(self):
        f = os.path.join(cm.DATA_OUTPUT,'baike.html')
        try:
            fout=codecs.open('baike.html', 'w', encoding='utf-8')
        except FileNotFoundError:
            fout = open('baike.html', 'w', encoding='utf-8')
        fout.write("<html><head><meta charset='utf-8'></head><body><table>")
        #将data中的三个数据写成表格的一行
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data["url"])
            fout.write("<td>%s</td>" % data["title"])
            fout.write("<td>%s</td>" % data["summary"])
            fout.write("</tr>")
        fout.write("</table></body></html>")
        fout.close()
        self.datas = []

    def output_csv(self,file_name):
        f = open(file_name, mode='a', encoding='utf-8')
        writer = csv.writer(f)
        try:
            writer.writerows(self.datas)
            self.datas=[]
        except Exception as e:
            print(e)
            log.info(e)

