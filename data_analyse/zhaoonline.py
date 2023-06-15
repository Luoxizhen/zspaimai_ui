import numpy as np
import time
import matplotlib.pyplot as plt
import csv
from collections import Counter

import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime
def zhao_onling_drop_duplicates():
    """删除重复拍品"""
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_中国近代机制币.csv"
    products = pd.read_csv(file_d)
    products=products.drop_duplicates()
    products.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_中国近代机制币_去重.csv")
def zhao_online_data_sort():
    """对新中国纸钞的拍品按照名称进行分类"""
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_新中国纸钞.csv"
    products = pd.read_csv(file_d)
    # print(products)
    good_names=products['拍品名称']
    good_indexs =[]
    print(type(good_names))
    print(len(good_names))
    for i in range(len(good_names)):
        if "第一版" in good_names[i]:
            good_indexs.append('一')
        elif "第二版" in good_names[i]:
            good_indexs.append('二')
        elif "第三版" in good_names[i]:
            good_indexs.append('三')
        elif "第四版" in good_names[i]:
            good_indexs.append('四')
        else:
            good_indexs.append('o')
    products['版本'] = good_indexs
    print(products)

    products.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_新中国纸钞_分类.csv")



def zhao_online_data_analyse():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_连体钞纪念钞.csv"
    products = pd.read_csv(file_d, names=['拍品id', '拍品图片', '拍品名称', '品相', '价格', '日期'])
    products_unique = products[0:9820]
    analyse_result = {}


    analyse_result['总成交价'] = products_unique['价格'].sum()


    write_result = pd.DataFrame(data=analyse_result.values(),index=analyse_result.keys(),columns=['分析结果'])
    write_result.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果.csv",mode="a")
    analyse_result['最大'] = products_unique.reindex(([products_unique['价格'].argmax()]))
    analyse_result['最小'] = products_unique.reindex(([products_unique['价格'].argmin()]))

    analyse_result['最大'].to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果.csv",mode="a")
    analyse_result['最小'].to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果.csv", mode="a")

def zhao_online_data_analyse1():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_连体钞纪念钞.csv"
    products = pd.read_csv(file_d, names=['拍品id', '拍品图片', '拍品名称', '品相', '价格', '日期'])
    products_unique = products[0:9820]
    # print(products_unique['拍品名称'].str.contains(r'第三版',na=True))
    print(products_unique.filter(like="第三版").columns())
    products_unique.filter()



def zhao_online_market():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_新中国纸钞_分类.csv"

    prices = []
    names = []
    appearances = []
    product = []
    prices_cp = []
    # df = pd.read_csv(file_d, names=['拍品图片', '拍品名称', '拍品价格', '拍品等级'])
    df = pd.read_csv(file_d)
    # print(df['拍品价格'].value_counts())
    # print(df['拍品价格'].value_counts().index)
    # print(df['拍品价格'].value_counts()[1])


    price_d = np.array([0, 50, 100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 200000])
    labels = pd.cut(df.价格, price_d)
    print(labels)
    grouped = df.groupby(['价格', labels])

    print(grouped.size().unstack(0))
    g_s = grouped.价值.sum().unstack(0)
    print(g_s)
    # grouped1=df.groupby([labels]).count()
    grouped1 = df.groupby([labels]).count()
    print(grouped1)
    # plt.plot(grouped1.index,grouped1['价值'])
    # plt.show()
    print(grouped1.index)
    print(grouped1['拍品图片'].values)
    a = np.asarray(grouped1['拍品图片'].values)
    axies = ['0-50', '100', '500', '1000', '2000', '5000', '10000', '20000', '50000', '200000']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('product_price')
    # plt.tick_params(labelsize=8)
    # plt.ylabel('product_number')
    # plt.title('product_count in different price')
    # plt.bar(axies,a)
    #
    # plt.show()

    prices = np.asarray(df['价值'])
    print(prices.argmax())
    print(df.loc[prices.argmax()])

    print(df.loc[prices.argmin()])

    print(prices.sum())

def zhao_online_paimai():
    '''拍品列表数据统计'''
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_中国近代机制币_去重.csv"
    df = pd.read_csv(file_d, names=['拍品序号','拍品id','拍品图片', '拍品名称',  '拍品等级','价格','日期'])
    # df = pd.read_csv(file_d)
    price_d = np.array([0, 50, 100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 200000,200000000])
    labels = pd.cut(df.价格, price_d)
    grouped = df['价格'].groupby([labels])
    sum_price = grouped.sum()
    product_count=grouped.count()
    print(df['价格'].max())
    print(df['价格'].min())
    print(df['价格'].count())
    print(df['价格'].sum())
    sum_price.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果_汇总.csv",mode='a')
    product_count.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果_汇总.csv", mode='a')

def zhao_online_paimai_time():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_新中国纸钞_分类.csv"
    # df = pd.read_csv(file_d, names=['拍品序号', '拍品id', '拍品图片', '拍品名称', '拍品等级', '价格', '日期'])
    df = pd.read_csv(file_d)
    time_strs = df['日期']
    s_time = []
    for a_time in time_strs:
        s_time.append(datetime.strptime(a_time, '%Y-%m-%d %H:%M:%S'))


    product_new = pd.DataFrame({"拍品名称":df["拍品名称"].values,"价格":df["价格"].values,"版本":df['版本'].values},index=s_time)
    product_new_1 = product_new[product_new['版本'] == "四"]
    print(product_new_1.index.min())
    print(product_new_1.index.max())
    p_n = product_new_1.to_period('M')

    grouped = p_n.groupby(level=0)




    grouped.count().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果_t.csv",mode="a")
    grouped.sum().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_分析结果_t.csv",mode="a")

def zsonline_paimai_time():
    file_d = "/Users/yuanyuanhe/Desktop/订单.csv"
    # df = pd.read_csv(file_d, names=['拍品序号', '拍品id', '拍品图片', '拍品名称', '拍品等级', '价格', '日期'])
    df = pd.read_csv(file_d)
    time_strs = df['o.create_time']
    s_time = []

    df['o.create_time'] = pd.to_datetime(df['o.create_time'],unit='s')







    df.to_csv("/Users/yuanyuanhe/Desktop/订单_new.csv",mode="a")





if __name__ == "__main__":
    # zhao_onling_drop_duplicates()
    # zhao_online_paimai()
    zsonline_paimai_time()




