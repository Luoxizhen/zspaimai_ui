import time
import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
from urllib import request
import urlparse
import re
class HtmlDownloader(object):
    #获取页面的数据
    def download(self, url):
        print ("start download")

        if url is None:
            print("url is None")
            log.info("{} 为none ，请传入网址".format(url))
            return None



        # print ("start requests")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        cookie = "mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; UM_distinctid=17dd6e9b9113dc-0ab66b8981522a-36657407-1fa400-17dd6e9b91212b3; _ga=GA1.2.694729881.1639988182; gr_user_id=b36b3074-4e0a-4e35-a09d-d69782e673ea; xn_dvid_kf_20165=1AA723-A175E4EE-3D55-4201-8243-D6E9BEB0C2B9; login=zhaoonline; ZHAOONLINE_WEB_LOGIN_ID=8324480; _z_tk=ywVKwriMlbf9dmdi2lu; _z_uid=8324480; _z_nickname=%E5%86%B7%E6%9C%88%E8%91%AC%E8%8A%B1%E9%AD%82; _gid=GA1.2.1815622103.1641980891; OZ_1U_2263=vid=v1dea3d54e2f82.0&ctime=1641980965&ltime=1641980959; SHOW_TYPE_1=1; Hm_lvt_215283b3bd0039735d53164b641338ee=1639988182,1641980589,1641980723,1642036213; Qs_lvt_119022=1639988181%2C1641980589%2C1642036212; CNZZDATA1279827027=139960794-1639979805-https%253A%252F%252Fwww.baidu.com%252F%7C1642030404; indexRegisterDate=2022-01-13; xn_sid_kf_20165=1642036216923455; gr_session_id_8add9b5e848122aa=6aec208e-7e47-445e-91cd-26e47d7d3ed4; gr_session_id_8add9b5e848122aa_6aec208e-7e47-445e-91cd-26e47d7d3ed4=true; 8add9b5e848122aa_gr_session_id=b12342b3-23a0-42f9-bd15-289a5b10aab8; 8add9b5e848122aa_gr_session_id_b12342b3-23a0-42f9-bd15-289a5b10aab8=true; mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; _gat=1; Qs_pv_119022=845512252248835600%2C2689890490271608300%2C2947498737325360000%2C2038782173727266000%2C770664525083711900; Hm_lpvt_215283b3bd0039735d53164b641338ee=1642039142; JSESSIONID=4D7111B3A89D38A27CE6A19E99AB1B4F; SERVERID=1b7e9fe4fd3e0a2219856c58b6f51133|1642039142|1642038899"

        headers = {'User-Agent': user_agent,
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Cookie": cookie}

        r = requests.get(url, headers=headers)
        # 判断响应状态

        if r.status_code == 200:

            r.encoding = 'gb2312'
            # log.info("该页面下载成功！{}".format(url))


            return r.text

        else:
            print("该页面下载失败！{}".format(url))
            log.error("该页面下载失败！{}".format(url))

            return None



if __name__ == "__main__":
    HtmlDownloader().download("http://www.lc0011.net/dispbbs.asp?boardID=11&ID=28933380&page=32")
