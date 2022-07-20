import csv
import json
import re

from requests import request
import pandas as pd
regex = re.compile("[0-9]")
def get_deal_data(**data_info):
    gname = "人民币"
    gname = gname.encode('utf-8')
    start_time = data_info["start_time"]
    end_time = data_info["end_time"]
    cid = data_info["cid"]
    page_num = data_info["page_num"]

    json = {
        "cid":cid,
        "gname":gname,
        "startingPrice":0,
        "closingPrice":"",
        "startTime":start_time,
        "endTime":end_time,
        "pageNum":page_num,
        "pageSize":51,
        "sortType":2,
        "sort": ""
    }
    url = "https://qgrading.huaxiaguquan.com/priceSearch/solrQueryCoin"
    headers ={
        "Accept":"*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_bebaa23800c0becb7424462f06559519=1657614102; HXSSOID=nDyKiF2i5h9W5HQ/7tkSPEKhL5oViC8RxEVVqf7MGIASOOB9D90KZXOsBhi6GZ+lTU+dUsGeD6uvaA3LLbF+cG9jlwNw7Qi5; acw_tc=3ccdc14216577010393054944e10ae821958afd7ffc9378fcb782b0ff2f69d; HXSESSIONID=7288D4D53429E0038197D8607E7B24B9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    r = request(url=url, method= "get", params= json,headers= headers )
    return r


def save_data():
    """保存数据
    https://imgali.huaxiaguquan.com/pic/"""
    pic_pre = "https://imgali.huaxiaguquan.com/pic/"
    file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/交易数据/华夏古泉.csv"
    data_info = {
        "start_time": "2022-06-16",
        "end_time": "2022-07-18",
        "cid": "710d4d87c3014b70a8e9f2cf02ad9f4c",
        "page_num":1
    }
    r = get_deal_data(**data_info)

    page_t = r.json()["totalPage"]
    deal_datas = []
    for i in range(1,page_t+1):
        data_info["page_num"] = i
        deal_datas_in_page = get_deal_data(**data_info).json()["data"]
        for j in range(len(deal_datas_in_page)):
            a_deal_data = deal_datas_in_page[j]
            deal_datas.append([a_deal_data["gname"],a_deal_data["gcontent"],a_deal_data["gprice"],a_deal_data["gdate"],pic_pre + json.loads(a_deal_data["pics"])[0]])
    with open(file_path,mode="w",encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(deal_datas)



def data_analyse(file_path,file_path1):
    df = pd.read_csv(file_path)
    df["cert_display"] = df["name"]
    cert_display = []
    for i in range(len(df["cert_display"])):
        good_name = df["cert_display"][i].replace("（","(").replace("）",")").replace("-","")


        if "(" in good_name:
            start = good_name.find("(")+1
            end = good_name.find(")")
            temp = good_name[start:end].replace("-"," ")
            if temp.find(" ") == -1:
                n = regex.findall(temp)

                if len(n) > 0:
                    i = temp.find(n[0])
                    temp = temp[:i] + " " + temp[i:]

        elif "PMG" in good_name:
            start = good_name.find("PMG")
            end = good_name.find(" ")
            temp = good_name[start:end]
        elif "保粹" in good_name:
            start = good_name.find("保粹")
            end = good_name.find(" ")
            temp = good_name[start:end]
        else:
            temp = ""
        cert_display.append(temp)
    df["cert_display"] = cert_display
    df["i"] = df["i"].str.replace(",","，").str.replace("售出不退，不包评级，出价请慎重！","").str.replace(" 后附评级官网图，请仔细核对后出价.","")
    df["is_four"] = df["name"].str.find("第四套")
    df["is_four1"] =df["name"].str.find("第四版")

    df[df["is_four"]==-1][df["is_four1"]==-1].to_csv(file_path1)









if __name__ == "__main__":
    file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/交易数据/华夏古泉.csv"
    file_path1 = "/Users/yuanyuanhe/Desktop/竞拍分析/交易数据/华夏古泉1.csv"
    data_analyse(file_path,file_path1)




