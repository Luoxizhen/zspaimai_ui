import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
import re
import pandas as pd
from utils import times
def zsonline():
    file_dir_base = "/Users/yuanyuanhe/Desktop/货/成交记录/"
    file_names = [{"name1": "成交表_快递.csv", "name2": "成交表详情_快递.csv"}, {"name1": "成交表_快递到付.csv", "name2": "成交表详情_快递到付.csv"}]
    file_name = "总成交表.csv"

    df = pd.DataFrame()

    for i in range(len(file_names)):

        file_path_1 = file_dir_base + file_names[i]['name1']
        file_path_2 = file_dir_base + file_names[i]['name2']
        df1 = pd.read_csv(file_path_1).set_index('id')
        df2 = pd.read_csv(file_path_2).set_index('id')

        file_path_out = file_dir_base + file_name
        df3 = pd.merge(df2,df1['pay_time'],left_index=True,right_index=True)
        df = pd.concat([df,df3])
    df.to_csv(file_path_out)
def zsonline_1():
    file_dir_base = "/Users/yuanyuanhe/Desktop/货/成交记录/"
    file_name = "总成交表.csv"
    file_name1 = "总成交表_名字排序_1.csv"
    file_path = file_dir_base + file_name
    file_path1 = file_dir_base + file_name1

    df = pd.read_csv(file_path)
    pay_times = []
    for i in range(len(df['pay_time'])):
        pay_times.append(times.time_to_str(df['pay_time'].values[i]))
    df['pay_time'] = pay_times

    df3 = df.set_index(['u_phone']).sort_index()

    df3.to_csv(file_path1)
def zsonline_2():
    file_dir_base = "/Users/yuanyuanhe/Desktop/货/成交记录/"

    file_name = "总成交表_名字排序_1.csv"
    file_name1 = "总成交表_成交金额排序_1.csv"
    file_path = file_dir_base + file_name
    file_path1 = file_dir_base + file_name1

    df = pd.read_csv(file_path).set_index('u_phone')

    df1 = df['total_price'].groupby(level=0).sum()
    df1.name = "sum"
    print(type(df1))




    df4 = pd.merge(df,df1,left_index=True,right_index=True)


    # df4.sort_values(by='sum',ascending=False).to_csv(file_path1)
    df5 = df[['pay_time','total_price','buyer_service_price','total_coupon','price']]
    print(df5)
    df5['pay_time']=pd.to_datetime(df5['pay_time'])
    df6 = df5.set_index('pay_time')

    df6.resample('M').sum().to_csv(file_dir_base + '月份盈利统计.csv')

def zsonline_3():
    file_dir_base = "/Users/yuanyuanhe/Desktop/货/成交记录/总成交表_成交金额排序_1.csv"

    df=pd.read_csv(file_dir_base)
    df1 = df[["user_name","phone","address","u_phone"]].drop_duplicates()
    file_dir= "/Users/yuanyuanhe/Desktop/货/成交记录/中晟在线春拍图录寄送名单.csv"
    df1.to_csv(file_dir)

def zsonline_4():
    file_1 = "/Users/yuanyuanhe/Desktop/货/成交记录/中晟在线春拍图录寄送名单.csv"
    file_2 = "/Users/yuanyuanhe/Desktop/货/成交记录/总成交表_成交金额排序.csv"
    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)
    df3 = pd.concat([df1,df2],keys=["u_phone","user_name"],axis=1)
    print(df3)
    file_dir= "/Users/yuanyuanhe/Desktop/货/成交记录/中晟在线春拍图录寄送名单-2.csv"
    df3.to_csv(file_dir)
def zsonline_5():
    file_1 = "/Users/yuanyuanhe/Desktop/钞票编号.csv"
    df1 = pd.read_csv(file_1)
    df2 = df1["name"].str.split(r"[^\x00-\xff]+",expand=True)
    df3 = df1["name"].str.split(r"[a-zA-Z0-9*]+",expand=True)

    file_dir= "/Users/yuanyuanhe/Desktop/钞票编号-2.csv"
    df4= pd.concat([df1,df3[0],df3[1],df2[1]],axis=1)
    print(df4)
    df4.to_csv(file_dir)
def zsonline_6():
    file_1 = "/Users/yuanyuanhe/Desktop/二版币.csv"
    df1 = pd.read_csv(file_1)
    df1[["name","rid","nid","name1","name2"]].dropna().to_csv(file_1)
def zsonline_7():
    file_1 = "/Users/yuanyuanhe/Desktop/钞票编号-2.csv"
    df = pd.read_csv(file_1)
    name_l = []
    name_s = ""
    df5 = pd.DataFrame()
    for i in range(df.shape[0]):
        if type(df.loc[i]["name2"])==str :
            name_l.append(df.loc[i]["name3"])
            name_s = df.loc[i]["name3"]
        else:
            name_l.append(name_s + df.loc[i]["name3"])
    df5["name"] = name_l
    df5["rid"]=df["rid"]
    df5["nid"]=df["nid"]
    df5["noteNumber"] = df["noteNumber"]
    df5.to_csv("/Users/yuanyuanhe/Desktop/钞票编号_数据库.csv")

def zsonline_8():
    file_1 = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币角币.csv"
    file_2 = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币元币.csv"
    # file_3 = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/一版币二百元.csv"
    df1 = pd.read_csv(file_1,names=["cert_display","cert_comments","lot","noteNumber","title","serial","i",
                                    "special_no","is_specimen","buyer_premium","did","is_clinch","price",
                                    "parities","currency","volamount","dealTime"])
    df2 = pd.read_csv(file_2,names=["cert_display","cert_comments","lot","noteNumber","title","serial","i",
                                    "special_no","is_specimen","buyer_premium","did","is_clinch","price",
                                    "parities","currency","volamount","dealTime"])
    # df3 = pd.read_csv(file_3,names=["cert_display","cert_comments","lot","noteNumber","title","serial","i",
    #                                 "special_no","is_specimen","buyer_premium","did","is_clinch","price",
    #                                 "parities","currency","volamount","dealTime"])

    df1.drop(["lot","title","did","is_clinch","volamount","is_specimen"],axis=1,inplace=True)
    df2.drop(["lot", "title", "did", "is_clinch", "volamount","is_specimen"], axis=1, inplace=True)
    # df3.drop(["lot", "title", "did", "is_clinch", "volamount","is_specimen"], axis=1, inplace=True)
    df4=pd.concat([df1,df2])

    df4.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币_数据库.csv")

def zsonline_9():
    file_1 = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币_数据库.csv"

    df1 = pd.read_csv(file_1)
    serial_nums = []
    serial_num_temps = df1["serial"]
    for i in range(df1.shape[0]):

        serial_num = serial_num_temps[i]
        if type(serial_num) == str:
            while serial_num.find("<") != -1:  # 去掉格式
                start_s = serial_num.find("<")
                end_s = serial_num.find(">") + 1
                temp_s = serial_num[start_s:end_s]
                serial_num = serial_num.replace(temp_s, "")
        serial_nums.append(serial_num)
    df1["serial"] = serial_nums
    df1.to_csv(file_1)

def zsonline_10():
    file_1 = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/钞票编号_数据库.csv"

    df1 = pd.read_csv(file_1)
    is_specimen = []

    df1["is_specimen"] = df1["name"].str.contains("票样").astype(int)
    df1.to_csv(file_1)





if __name__ == "__main__":
    zsonline_10()
