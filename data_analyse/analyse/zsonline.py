import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
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





if __name__ == "__main__":
    zsonline_2()
