import time

import numpy as np
import os
import re
import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
from copy import deepcopy
import pandas as pd
from utils import times


def get_child_file(father_path):
    '''获取文件夹中的所有文件
    f1 = "/Users/yuanyuanhe/Desktop/竞拍分析/一尘/客户信息"'''
    file_list = os.listdir(father_path)
    for f in file_list:
        if (f[0] == '.'):
            file_list.remove(f)
    return (file_list)
def buyer_analyse(sell_fp):
    sell_f = pd.read_csv(sell_fp,names=["title","url"])
    sell_f["title"] = sell_f["title"].str.split("\n")
    sell_f_title = split_col(sell_f,"title")
    sell_group_size = sell_f_title.groupby(sell_f_title['title1']).size() #根据发帖人的名字进行分组，计算发帖人所发的帖子总数
    sell_group_size.name = "size"
    sell_sort = pd.merge(sell_f_title,sell_group_size,left_on="title1",right_index=True,how="inner") #总表增加发帖人所发贴总数
    # sell_sort.sort_values(by="size",ascending=False).to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买_买家排序.csv")
    #sell_sort[sell_sort["title1"]=="作者：SYG5999"].sort_values(by=["title0","title2"]).to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买_最活跃买家.csv")
    # sell_index = sell_sort[sell_sort["title1"] == "作者：SYG5999"]['title0'].drop_duplicates().index
    # sell_sort.loc[sell_index].to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买_最活跃买家的帖子去重.csv")
    # 更加发帖人及发帖的标题，去重
    sell_sort.loc[sell_sort[["title0","title1"]].drop_duplicates().index].sort_values(by="size",ascending=False).to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买_所有买家帖子根据名字去重.csv")
def buyer_info_analyse(fp):
    paths = get_child_file(fp)
    sell_info = pd.DataFrame()
    print(paths)
    for path in paths:
        df = pd.read_csv(fp+path,names=["detail","contact","url"])
        sell_info = pd.concat([sell_info,df])
    sell_info.drop_duplicates().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买家信息分析/买家帖子.csv")
def get_phone_buyer():
    fp = "/Users/yuanyuanhe/Desktop/卖家联系方式-2.csv"
    buyer_info = pd.read_csv(fp)
    buyers = pd.DataFrame()

    buyers["name"] = buyer_info["name"].str.replace("(", "（").str.split("（", expand=True)[0].str.replace("（","").str.replace("姓名","").str.replace("：","").str.replace(":","").str.replace("真名","").str.replace("联系人","")
    buyers["phone"]= buyer_info["phone"].str.findall(r"[0-9]{11}")
    buyers.to_csv("/Users/yuanyuanhe/Desktop/卖家联系方式_整理-2.csv")

def get_phone():
    fp = "/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买家信息分析/买家帖子.csv"
    sell_info = pd.read_csv(fp)
    sellers_info = pd.DataFrame()
    sellers = sell_info["contact"].drop_duplicates().dropna().str.replace(":", "：")
    sellers_1 = sellers.str.split("姓名|真名|姓 名", expand=True)  # 用户的会员级别
    sellers_info["level"] = sellers_1[0]
    sellers_2 = sellers_1[1].str.split("地址", n=1, expand=True)
    sellers_info["name"] = sellers_2[0]
    # .str[0:6].str.findall(r"[\u4e00-\u9fa5]{3}") 匹配中文
    sellers_3 = sellers_2[1].str.split(r"邮编|邮政编码", n=1, expand=True)
    sellers_info["address"] = sellers_3[0]
    sellers_info["code"] = sellers_3[1].str[0:10].str.findall(r"[0-9]{6}")
    sellers_4 = sellers.str.split(r"电话", n=1, expand=True)
    sellers_5 = sellers.str.split(r"手机", n=1, expand=True)
    sellers_6 = sellers.str.split(r"微信", n=1, expand=True)
    sellers_info["phone_1"] = sellers_4[1].str[0:30].str.findall(r"[0-9]{11}")
    # sellers_info["phone_2"] = sellers_5[1].str[0:28].str.findall(r"[0-9]{11}")
    sellers_info["phone_2"] = sellers_5[1].str[0:30].str.findall(r"[0-9]{11}")
    # sellers_info["phone_2"] = sellers_5[1].str[0:28].str.findall(r"^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$")
    sellers_info["wechat"] = sellers_6[1].str[0:30].str.findall(r"[0-9]{11}")
    # print(sellers_info["level"])
    sellers_info.to_csv("/Users/yuanyuanhe/Desktop/买家联系方式_1.csv")

    # print(sellers_info["address"])

    # sellers_1 =sellers.str.split("手机：",expand=True)
    # sellers_2 = sellers.str.split("姓名：",expand=True)
    # sellers_3 = sellers.str.split("微信：", expand=True)
    # sellers_4 = sellers.str.split("电话：", expand=True)
    # print(sellers_1[1].str.slice(0,12))
    # print(sellers_2[1].str.slice(0, 3))
    # print(sellers_3[1].str.slice(0, 12))
    #
    # print(sellers_1[1].str.slice(12, 24))
    # sellers_5 = pd.DataFrame({"name":sellers_2[1].str.rstrip().str.slice(0, 3),"phone1":sellers_1[1].str.rstrip().str.slice(0,11),"phone2":sellers_1[1].str.rstrip().str.slice(11, 24),"wechat":sellers_3[1].str.rstrip().str.slice(0, 11)}).dropna(how="all")
    # sellers_5.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买家信息分析/买家联系方式_3.csv")
    # sellers_df = pd.DataFrame({"contact":sellers.values})
    #
    #
    #
    # sellers_df["name"]= sellers_df["contact"].str.slice
    # sellers_df["contact"] = sellers_df["contact"].str.split("：")
    # data = split_col(sellers_df,"contact")
    # data.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币/买家信息分析/买家联系方式_1.csv")


def user_info_good():
    sellers_info = pd.read_csv("/Users/yuanyuanhe/Desktop/买家联系方式_1.csv")[["name","phone_1","phone_2","wechat"]].dropna(how="all")
    # sellers_info["name"] = sellers_info["name"].str.findall(r"[\u4e00-\u9fa5]{2,3}（")
    sellers_info["name"] = sellers_info["name"].str.split("（", n=1, expand=True)[0].str.findall(r"[\u4e00-\u9fa5]{2,3}")
    sellers_info["name"] = sellers_info["name"].fillna(method="ffill")

    # sellers_info["phone"] = sellers_info["phone_1"] +sellers_info["phone_2"] + sellers_info["wechat"]
    names = []
    for i in sellers_info["name"]:
        print(i[0])
        names.append(i[0])

    print(names)



    # sellers_info[["name","phone_1","phone_2","wechat"]].to_csv("/Users/yuanyuanhe/Desktop/买家联系方式_2.csv")



def read_data(sell_fp):
    sell_f = pd.read_csv(sell_fp,names=['con'])
    contents = sell_f['con']
    for content in contents:
        print(content)

        while 1:
            if content.find("<") != -1:
                start_s = content.find("<")
                print(start_s)
                end_s = content.find(">")+1
                print(end_s)
                temp_s = content[start_s:end_s]
                print(temp_s)
                content = content.replace(temp_s,"")
                print(content)

            else:
                break

        print(content)





def split_col(data,column):
    '''拆分 Series：
    data 原始数据
    column 拆分的列明'''
    data = deepcopy(data)
    max_len = max(list(map(len,data[column].values))) # 最大长度
    new_col = data[column].apply(lambda x:x + [None]*(max_len - len(x)))
    new_col = np.array(new_col.tolist()).T

    for i,j in enumerate(new_col):
        data[column+str(i)] = j
    return data

def split_phone():
    filepath = "/Users/yuanyuanhe/Desktop/竞拍分析/一尘/客户信息/评级币评级钞_卖家.csv"
    data = pd.read_csv(filepath).dropna(subset=["phone"])

    data["phone"] = data["phone"].str.replace("[","").str.replace("]","").str.replace("'","")
    data1 = pd.concat([data,data["phone"].str.split(",",n=3,expand=True)],axis=1)
    del data1["phone"]
    data1.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/一尘/客户信息/评级币评级钞_卖家1.csv")

def sell():
    file_path = "/Users/yuanyuanhe/Desktop/卖.csv"
    df = pd.read_csv(file_path,names=["title","url"])

    df["title"].str.split("作者：|发表于：|最后发贴：|",n=4,expand=True)
    df_titles = df["title"].str.split("\n",n=3,expand=True)

    df_titles['url'] = df["url"]
    df_titles.to_csv("/Users/yuanyuanhe/Desktop/卖_title 分列.csv")
def sell_info():
    file_path = "/Users/yuanyuanhe/Desktop/卖_title 分列.csv"
    df = pd.read_csv(file_path)
    df_seller = pd.DataFrame()
    df_seller["seller"] = df["1"].drop_duplicates() #卖家名字去重复
    df_seller = pd.concat([df_seller,df["url"]],axis=1,join="inner")
    # del(df_seller["0"])
    # del(df_seller["1"])
    # del(df_seller["2"])
    # del(df_seller["3"])
    # del (df_seller["Unnamed: 0"])
    df_seller["seller"] = df_seller["seller"].str[3:]

    df_seller.to_csv("/Users/yuanyuanhe/Desktop/卖家.csv")
def drop_duplicate_by_name(*f):
    '''将爬取的title 进行分列，按照发表的作者进行去重复去空，让后与 url 进行内连接
    *f 为文件夹位置，
    f[1] :  从一尘爬取到的title 文件 所在位置
    f[2] :  对f[1] 处理后的文件存放位置'''
    print(f)
    file_path = f[0]
    df_raw = pd.read_csv(file_path,names=["title","url"])
    df_split = df_raw["title"].str.split("\n",n=3,expand=True)


    df_customer = df_split[1].drop_duplicates().dropna()
    df_customer.name ="name"
    df_info = pd.concat([df_customer,df_raw],axis=1,join="inner")
    df_info.to_csv(f[1])
def get_customer_info(*f):
    file_path = f[0]
    raw = pd.read_csv(file_path, names=["content","contact","url"]) # 读用户贴

    raw.dropna(subset=["contact"],axis=0,inplace=True) #  删除没有联系方式的行
    raw.reset_index(drop=True,inplace=True)



    customers = raw["contact"].str.split("<br/>",expand=True) #将用户贴中 用户信息进行分列

    del(customers[0])  #删除第一列
    phones = []
    names = []
    name_list = ["姓名", "姓 名", "真名", "名", "联系人"]
    phone_list = ["电话", "电 话", "电微", "联系方式", "固话", "宅电"]
    for i in range(customers.shape[0]): # 总用户数量


        customer = customers.iloc[i].dropna() # 一个用户的基本信息


        for j in range(len(customer)): #一个用户的总信息量

            if any(name in customer.iloc[j] for name in name_list):
                names.append(customer.iloc[j])
                break
            elif j == len(customer)-1:
                names.append("")
    for i in range(customers.shape[0]): #2550
        customer = customers.iloc[i].dropna()

        for j in range(len(customer)):

            if "手机" in customer.iloc[j] or "手 机" in customer.iloc[j]:
                phones.append(customer.iloc[j])
                break
            elif j == len(customer)-1: # 重新查找一遍用户的信息
                for j in range(len(customer)):

                    if any(name in customer.iloc[j] for name in phone_list) :
                        phones.append(customer.iloc[j])
                        break
                    elif j == len(customer)-1:
                        phones.append("")
    customers_info = pd.DataFrame()
    names = [name.replace("(", "（").replace("姓名", "").replace("：", "").replace(":", "").replace("真名", "").replace("联系人", "") for name in names]
    customers_info["name"] = names
    customers_info["phone"] = phones
    customers_info["name"] = customers_info["name"].str.split("（", expand=True)[0].str.replace("（", "")
    customers_info["phone"] = customers_info["phone"].str.findall(r"[0-9]{11}")
    customers_info_1 = split_col(customers_info,"phone")

    customers_info_2 = pd.concat([customers_info_1[customers_info_1["phone0"].isnull()==True]["name"],customers],axis=1,join="inner") # 没有找到电话号码的数据
    del(customers_info_1["phone"])
    customers_info_1.to_csv(f[1])
    customers_info_2.to_csv(f[2])




def sell_info_detail():
    file_path = "/Users/yuanyuanhe/Desktop/卖家帖子.csv"
    seller_raw = pd.read_csv(file_path,names=["content","contact","url"])
    seller = seller_raw["contact"].str.split("<br/>",expand=True)
    del(seller[0])
    seller.to_csv("/Users/yuanyuanhe/Desktop/卖家信息_raw.csv")

def get_sell_info():
    file_path = "/Users/yuanyuanhe/Desktop/一二三版币卖家信息/卖家信息_raw.csv"
    seller_raw = pd.read_csv(file_path)
    phones=[]
    names=[]
    name_list = ["姓名","姓 名","真名","名","联系人"]
    phone_list = ["电话", "电 话", "电微", "联系方式", "固话", "宅电"]
    for i in range(2550): #2550
        seller_info = seller_raw.iloc[i]

        for j in range(1,24):

            if any(name in str(seller_info[j]) for name in name_list):
                names.append(seller_info[j])
                break
            elif j == 23:
                names.append("")
    for i in range(2550): #2550
        seller_info = seller_raw.iloc[i]

        for j in range(1,24):

            if "手机" in str(seller_info[j]) or "手 机" in str(seller_info[j]):
                phones.append(seller_info[j])
                break
            elif j == 23:
                for j in range(1, 24):

                    if any(name in str(seller_info[j]) for name in phone_list) :
                        phones.append(seller_info[j])
                        break
                    elif j == 23:
                        phones.append("")
    seller = pd.DataFrame()
    seller["name"] = names
    seller["phone"] = phones

    seller.to_csv("/Users/yuanyuanhe/Desktop/卖家联系方式-2.csv")
def sell_info_no_phone():
    phone_list = [104,330,448,549,672,738,819,1046,1442,1555,1750,1870,2084,2169,2444]
    file_path = "/Users/yuanyuanhe/Desktop/卖家信息_raw.csv"
    seller_raw = pd.read_csv(file_path)
    seller_phone = pd.DataFrame()
    for phone in phone_list:
        seller_phone = pd.concat([seller_phone,(seller_raw[seller_raw["no"] == phone])])

    # seller_phones = pd.DataFrame(seller_phone)
    seller_phone.to_csv("/Users/yuanyuanhe/Desktop/卖家联系方式-无号码1.csv")
    # with open("/Users/yuanyuanhe/Desktop/卖家联系方式-无号码.csv",'a') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerows(seller_phone)
    # csv.writer(seller_phone,"/Users/yuanyuanhe/Desktop/卖家联系方式-无号码.csv")
def concat_phone1():
    f1 = "/Users/yuanyuanhe/Desktop/竞拍分析/一尘/客户信息/"
    # file_list = get_child_file(f1)
    file_list = ["评级币评级钞_买家.csv","评级币评级钞_卖家.csv"]
    df = pd.DataFrame()

    for f in file_list:
        df_temp = pd.read_csv(f1+f)
        df = pd.concat([df,df_temp])
    all = df.dropna(subset=["name","phone0"]).drop_duplicates(subset=["phone0"])

    all  .to_csv(f1 + "/评级币所有用户.csv")

    

if __name__ == "__main__":
    # f1 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖贴.csv"
    # f2 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖家_分列.csv"
    # f3 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖家_无电话号码.csv"
    # f = [f1,f2,f3]
    # get_customer_info(*f)
    concat_phone1()