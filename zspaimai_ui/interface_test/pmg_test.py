from bs4 import BeautifulSoup
from interface_base.pmg import get_class_of_paper,get_detail
import csv
from html_parser import HtmlParser_pmg
from utils.html_outputer import data_m
from interface_base.html_downloader import html_d
from utils.rwyaml import get_yaml_data
class Test_pmg():
    def test_get_data(self):
        the_parser = HtmlParser_pmg()
        url = "https://www.pmg.cn/Class/"+ "8"
        pmg_data = get_yaml_data("interface_data","html_url.yml")["pmg"]
        url = pmg_data["url_class"]+"8"
        class_info = html_d.download(url)
        class_papers = the_parser.parser_html(class_info)

        for a_class_paper in class_papers:
            num = a_class_paper[0]
            url_d = pmg_data["url_detail"] + num
            the_papers_of_num = html_d.get_detail(url_d)
            the_papers_of_num_info = the_parser.get_child(the_papers_of_num)
            for a_paper in the_papers_of_num_info:
                a_paper[2] = a_class_paper[2] + a_paper[2]
                a_paper[3] = a_class_paper[3]
            data_m.store_data(the_papers_of_num_info)
        data_m.store_data(class_papers)
        f = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/钞票编号_外汇券.csv"
        data_m.output_csv(f)
        data_m.clear_data()












