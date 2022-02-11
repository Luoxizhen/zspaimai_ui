from bs4 import BeautifulSoup

import re    #正则表达式模块
# import urlparse    #用来拼接url
from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log

class HtmlParser(object):
    def parser(self, page_url, html_cont):
        '''
        解析器主函数
        parm page_url:一个url
        parm html_cont:网页内容，格式为字符串
        return: urls, 数据；格式为 set, dict
        '''
        if page_url is None or html_cont is None:
            print ("page_url is None")
            return
        #建立bs对象，使用html.parser进行解析
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        print ("soup established")
        #接下来分别调用两个私有函数返回urls和data
        new_urls = self._get_new_urls(page_url, soup)
        print ("new_urls get")
        new_data = self._get_new_data(page_url, soup)
        print ("new_data get")
        return new_urls, new_data

    def parser1(self, html_cont):
    # def parser1(self,html_cont):
        '''解析页面数据，并保存到csv 文件中'''
        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        # print(soup.ul)
        # return soup.ul
        """开始解析数据"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')


        c = soup.find_all('div',class_='list-item cf')
        goods=[]

        for i in range(int(len(c))):
            # print(i)
            # print(40 * '*')
            # print(c[i])
            # print(goods[2*i+1])
            good_info = BeautifulSoup(markup=str(c[i]), features='html.parser')
            # print(good_info)
            # print(b.ul.contents[1])
            # good_info = BeautifulSoup(markup=str(b.ul.contents[1]))
            good_link = good_info.a['href'].removesuffix('.shtml').removeprefix('/') #拍品链接 https://www.zhaoonline.com/auction-detail.shtml?id=5574544

            n = good_link.find('/')+1
            good_id = good_link[n::]







            good_picture = good_info.img['src']

            good_name = good_info.find("a",class_="item-title")['title'] #拍品名称
            good_px = good_info.span.text #品相
            good_price = good_info.strong.text
            good_t = good_info.find("span",class_="time").text #成交时间


            # good = [good_link,good_picture, good_name, good_px,good_price,good_t,good_index]
            good = [good_id,good_picture, good_name, good_px, good_price, good_t]

            goods.append(good)
        return goods






    def _get_new_data(self, page_url, soup):
        '''
        提取想要的数据
        parm page_url: 当前页面url
        parm soup: beautifulsoup对象
        return: dict
        '''
        #声明字典
        data = {}
        data['url'] = page_url
        data['title'] = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()
        data['summary'] = soup.find('div', class_='lemma-summary').get_text()

        return data


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
        fout=codecs.open('baike.html', 'w', encoding='utf-8')
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



class UrlManager(object):
    '''网址管理'''
    def __init__(self):
        #初始化的时候就生成两个url仓库
        self.new_urls = set()
        # self.new_urls = ["http://www.huabid.com/auctionList/all/fixedPrice/selling?pageNo=3"]
        self.old_urls = set()

    #判断新url仓库中是否还有没有爬取的url
    def has_new_url(self):
        return len(self.new_urls)

    #从new_url仓库获取一个新的url
    def get_new_url(self):
        return self.new_urls.pop()

    def add_new_url(self, url):    #这个函数后来用不到了……
        '''
        将一条url添加到new_urls仓库中
        parm url: str
        return:
        '''
        if url is None:
            return
        #只需要判断old_urls中没有该链接即可，new_urls在添加的时候会自动去重
        if url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将多条url添加到new_urls仓库中
        parm url: 可迭代对象
        return:
        '''
        print ("start add_new_urls")
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def add_old_url(self, url):
        self.old_urls.add(url)
        print ("add old url succefully")

    #获取已经爬取过的url的数目
    def old_url_size(self):
        return len(self.old_urls)
class HtmlDownloader(object):
    #获取页面的数据
    def download(self, url):
        # print ("start download")
        if url is None:
            return None
            print ("url is None")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        cookie = "mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; UM_distinctid=17dd6e9b9113dc-0ab66b8981522a-36657407-1fa400-17dd6e9b91212b3; _ga=GA1.2.694729881.1639988182; gr_user_id=b36b3074-4e0a-4e35-a09d-d69782e673ea; xn_dvid_kf_20165=1AA723-A175E4EE-3D55-4201-8243-D6E9BEB0C2B9; login=zhaoonline; ZHAOONLINE_WEB_LOGIN_ID=8324480; _z_tk=ywVKwriMlbf9dmdi2lu; _z_uid=8324480; _z_nickname=%E5%86%B7%E6%9C%88%E8%91%AC%E8%8A%B1%E9%AD%82; _gid=GA1.2.1815622103.1641980891; OZ_1U_2263=vid=v1dea3d54e2f82.0&ctime=1641980965&ltime=1641980959; SHOW_TYPE_1=1; Hm_lvt_215283b3bd0039735d53164b641338ee=1639988182,1641980589,1641980723,1642036213; Qs_lvt_119022=1639988181%2C1641980589%2C1642036212; CNZZDATA1279827027=139960794-1639979805-https%253A%252F%252Fwww.baidu.com%252F%7C1642030404; indexRegisterDate=2022-01-13; xn_sid_kf_20165=1642036216923455; gr_session_id_8add9b5e848122aa=6aec208e-7e47-445e-91cd-26e47d7d3ed4; gr_session_id_8add9b5e848122aa_6aec208e-7e47-445e-91cd-26e47d7d3ed4=true; 8add9b5e848122aa_gr_session_id=b12342b3-23a0-42f9-bd15-289a5b10aab8; 8add9b5e848122aa_gr_session_id_b12342b3-23a0-42f9-bd15-289a5b10aab8=true; mediav=%7B%22eid%22%3A%22387955%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22Q%3AbOZbNIAn8jY2y%23.aT%5B%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; _gat=1; Qs_pv_119022=845512252248835600%2C2689890490271608300%2C2947498737325360000%2C2038782173727266000%2C770664525083711900; Hm_lpvt_215283b3bd0039735d53164b641338ee=1642039142; JSESSIONID=4D7111B3A89D38A27CE6A19E99AB1B4F; SERVERID=1b7e9fe4fd3e0a2219856c58b6f51133|1642039142|1642038899"
        body = "q.categoryHtml=%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A+++%09%0D%0A%09%09%3Cli+class%3D%22zhengge%22%3E%3Ci+class%3D%22mb5%22%3E%0D%0A%09%09%09%3Cinput+type%3D%22checkbox%22+id%3D%22category_157%22+value%3D%22157%22+checked%3D%22checked%22+class%3D%22check_all+root+hack%22%3E%3Clabel+for%3D%22category_157%22+class%3D%22toolong+w100+label-cr%22+title%3D%22%E9%92%B1%E5%B8%81%E7%B1%BB%22%3E%E9%92%B1%E5%B8%81%E7%B1%BB%3C%2Flabel%3E%3C%2Fi%3E%0D%0A%09%09%3C%2Fli%3E%0D%0A%09%09%0D%0A%09%09%09%3Cli+class%3D%22pl30+pt5%22%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+type%3D%22checkbox%22+name%3D%22q.categoryIds%22+id%3D%22category_731%22+rel%3D%22category_157%22+value%3D%22731%22+checked%3D%22checked%22+class%3D%22hack%22%3E%3Clabel+for%3D%22category_731%22+class%3D%22toolong+w100+label-cr%22+title%3D%22%E7%AC%AC%E4%B8%80%E7%89%88%E4%BA%BA%E6%B0%91%E5%B8%81+%2816678%29%22%3E%E7%AC%AC%E4%B8%80%E7%89%88%E4%BA%BA%E6%B0%91%E5%B8%81+%2816678%29%3C%2Flabel%3E%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09%0D%0A%09&q.characterHtml=%0D%0A%09%0D%0A%09%0D%0A+++%09%09%3Cli+class%3D%22zhengge%22%3E%3Ci%3E%3Cinput+type%3D%22checkbox%22+id%3D%22all_choice_character%22+class%3D%22check_all+hack%22+checked%3D%22checked%22%3E%3Clabel+for%3D%22all_choice_character%22+class%3D%22label-cr%22%3E%E5%85%A8%E9%80%89%3C%2Flabel%3E%3C%2Fi%3E%3C%2Fli%3E%0D%0A%09%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2220%22+id%3D%22character_20%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_20%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E9%87%91%E9%93%B6%E5%B8%81%E7%B1%BB+-+%E6%97%A0%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2222%22+id%3D%22character_22%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_22%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E5%8D%81%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2223%22+id%3D%22character_23%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_23%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E4%B9%9D%E4%BA%94%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2224%22+id%3D%22character_24%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_24%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E4%B9%9D%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2225%22+id%3D%22character_25%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_25%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E5%85%AB%E4%BA%94%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2226%22+id%3D%22character_26%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_26%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E5%85%AB%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2227%22+id%3D%22character_27%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_27%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E4%B8%83%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2228%22+id%3D%22character_28%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_28%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E5%85%AD%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2229%22+id%3D%22character_29%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_29%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E4%BA%94%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2230%22+id%3D%22character_30%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_30%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E6%99%AE%E5%93%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2240%22+id%3D%22character_40%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_40%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E7%BA%B8%E5%B8%81%E7%B1%BB+-+%E6%97%A0%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%220%22+id%3D%22character_0%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_0%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E4%B8%80%E5%8F%A3%E4%BB%B7+-+%E6%97%A0%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A%09%09%09%3Cli%3E%0D%0A%09%09%09%09%3Ci%3E%3Cinput+autocomplete%3D%22off%22+type%3D%22checkbox%22+name%3D%22q.characterIds%22+value%3D%2252%22+id%3D%22character_52%22+checked%3D%22checked%22+class%3D%22hack%22%3E%0D%0A%09%09%09%09%09%3Clabel+for%3D%22character_52%22+class%3D%22label-cr%22%3E%0D%0A%09%09%09%09%09%09%E8%AF%84%E7%BA%A7%E5%B8%81%0D%0A%09%09%09%09%09%3C%2Flabel%3E%0D%0A%09%09%09%09%3C%2Fi%3E%0D%0A%09%09%09%3C%2Fli%3E%0D%0A%09%0D%0A++++%0D%0A++++&q.formHtml=&q.periodHtml=&q.textureHtml=&q.factionHtml=&keyword=&channelModuleBackup="
        headers = {'User-Agent':user_agent,
                   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                   "Cookie": cookie}
        # print ("start requests")
        r = requests.post(url, headers=headers)
        #判断响应状态
        if r.status_code == 200:
            r.encoding = 'utf-8'
            # print ("该页面下载成功！{}".format(url))

            return r.text
        else:
            print ("该页面下载失败！{}".format(url))
            log.info("该页面下载失败！{}".format(url))
        return None





class SpiderMan(object):
    def __init__(self):
        #调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        print("ppp")
    def spider(self):
        s1 = "8-8-N-N-00-N-0-N-1-N-N-N-N-0-N-N-"
        s2 = ".htm"
        base_url = "https://www.zhaoonline.com/trade/zhongguojindaijizhibi/"
        for i in range(1,1001):
            url = base_url + s1 + str(i) + s2
            self.manager.add_new_url(url)
            while (self.manager.has_new_url()):
                try:
                    new_url = self.manager.get_new_url()
                    html = self.downloader.download(new_url)
                    try:
                        data = self.parser.parser1(html)
                        self.output.store_data(data)
                        fn = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_中国近代机制币.csv"
                        self.output.output_csv(fn)
                    except Exception as e:
                        print(e)
                        log.info(e)
                except Exception as e:
                    print(e)
                    log.info(e)
    def spider1(self):
        s1 = "8-8-N-N-00-N-0-N-1-N-N-N-N-0-N-N-"
        s2 = ".htm"
        with open("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线.csv",'r') as f:
            lines = csv.reader(f)
            for line in lines:
                base_url = line[1]
                page_num = int(line[2]) + 1
                collection_index = line[0]
                for p in range(1,page_num+1):
                    url = base_url + s1 + str(p) + s2
                    self.manager.add_new_url(url)
                while (self.manager.has_new_url()):
                    try:
                        new_url = self.manager.get_new_url()
                        html = self.downloader.download(new_url)
                        try:
                            data = self.parser.parser1(html,collection_index)
                            self.output.store_data(data)
                            fn = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表.csv"
                            self.output.output_csv(fn)


                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)








if __name__== "__main__":
    SpiderMan().spider()






