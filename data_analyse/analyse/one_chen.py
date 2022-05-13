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
    """从用户贴，读取用户的信息
    f: 文件列表
    f[0] :  用户信息文件保存的位置
    f[1] : 有电话号码的用户信息保存位置
    f[2] : 无电话号码的用户信息保存位置"""
    file_path = f[0]
    raw = pd.read_csv(file_path, names=["content","contact","url"]) # 读用户贴
    raw.dropna(subset=["contact"],axis=0,inplace=True) #  删除没有联系方式的行
    raw.reset_index(drop=True,inplace=True) # 重新设置索引，后续需要根据索引查找数据
    customers = raw["contact"].str.split("<br/>",expand=True) #将用户贴中 用户信息根据 换行标签 进行分列，保存为一个新的dataframe
    del(customers[0])  #删除第一列信息，为用户在一尘网的级别
    phones = []
    names = []
    name_list = ["姓名", "姓 名", "真名", "名", "联系人"]
    phone_list = ["电话", "电 话", "电微", "联系方式", "固话", "宅电"]
    for i in range(customers.shape[0]): # 总用户数量，dataframe 行数
        customer = customers.iloc[i].dropna() # 一个用户的基本信息，读取dataframe 的一行，series 类型
        for j in range(len(customer)): #一个用户的总信息量
            if any(name in customer.iloc[j] for name in name_list): #在seriers 中找到带有名字信息的列，添加到names 中
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
    customers_info["name"] = customers_info["name"].str.split("（", expand=True)[0].str.replace("（", "") #提取名字
    customers_info["phone"] = customers_info["phone"].str.findall(r"[0-9]{11}") #提取电话号码
    customers_info_1 = split_col(customers_info,"phone") #电话号码分列
    customers_info_2 = pd.concat([customers_info_1[customers_info_1["phone0"].isnull()==True]["name"],customers],axis=1,join="inner") # 没有找到电话号码的数据
    del(customers_info_1["phone"])
    customers_info_1.to_csv(f[1])
    customers_info_2.to_csv(f[2])






if __name__ == "__main__":
    # f1 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖贴.csv"
    # f2 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖家_分列.csv"
    # f3 = "/Users/yuanyuanhe/Desktop/评级币评级钞_卖家_无电话号码.csv"
    # f = [f1,f2,f3]
    # get_customer_info(*f)
    concat_phone1()