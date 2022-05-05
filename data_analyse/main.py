import numpy as np

import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
import pandas as pd
from pandas import Series,DataFrame
# file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇商城1.csv"
# file_d1 = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表.csv"
# prices = []
# names = []
# appearances = []
# product = []
# prices_cp = []

def huayu_market():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇商城1.csv"
    file_d1 = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表.csv"
    prices = []
    names = []
    appearances = []
    product = []
    prices_cp = []
    df = pd.read_csv(file_d, names=['拍品图片', '拍品名称', '拍品价格', '拍品等级'])
    # print(df['拍品价格'].value_counts())
    # print(df['拍品价格'].value_counts().index)
    # print(df['拍品价格'].value_counts()[1])
    product_prices = df['拍品价格']
    for i in range(len(product_prices)):
        product_prices[i] = round(float(product_prices[i].removeprefix('¥')))
    df['价值'] = product_prices
    price_d = np.array([0, 50, 100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 200000])
    labels = pd.cut(df.价值, price_d)
    print(labels)
    grouped = df.groupby(['价值', labels])

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
# with open(file=file_d,mode="r",encoding="utf-8") as f:
#     data = csv.reader(f)
#     for l in data:
#         prices.append(float(l[2].removeprefix('¥')))
#         names.append(l[1])
#         appearances.append(l[3])
#         product.append([float(l[2].removeprefix('¥')),l[1],l[3]])
#
#
#     f.close()
#
# with open(file=file_d1,mode="r",encoding="utf-8") as f:
#     data = csv.reader(f)
#     for l in data:
#         prices_cp.append(float(l[3].removeprefix('¥')))
#     f.close()
# # print(prices)
# # print(names)
# # print(appearances)
# p = np.array(prices)
# n = np.array(names)
# a = np.array(appearances)
# pd = np.array(product)


#print(np.sort(prices,axis=0))
# print(np.max(prices))
# print(np.min(prices))
# print(np.average(prices))
#
# print(np.sum(prices))
# print(np.ptp(prices))
# print(np.median(prices))
# print(np.argmax(prices))
# print(prices[67])
# print(names[67])
# print(appearances[67])
# Counter(prices)
#
# arr = np.asarray([0.25656927, 0.31030828, 0.23430803, 0.25999823, 0.20450112, 0.19383106, 0.35779405, 0.36355627, 0.16837767, 0.1933686,  0.20630316, 0.17804974, 0.06902786, 0.26209944, 0.21310201, 0.12016498, 0.14213449, 0.16639964, 0.33461425, 0.15897344, 0.20293266, 0.14630634, 0.2509769,  0.17211646, 0.3922994,  0.14036047, 0.12571093, 0.25565785, 0.18216616, 0.0728473, 0.25328827, 0.1476636,  0.1873344,  0.12253726, 0.16082433, 0.20678088, 0.33296013, 0.03104548, 0.14949016, 0.05495472, 0.1494042,  0.32033417, 0.05361898, 0.14325878, 0.16196126, 0.15796155, 0.10990247, 0.14499696])
# arr = np.asarray(prices)
# print((arr < 100).sum())
# print((arr < 1000).sum()-(arr < 100).sum())
# print((arr < 10000).sum()-(arr < 1000).sum())
# print((arr < 20000).sum()-(arr < 10000).sum())
# print((arr < 30000).sum()-(arr < 20000).sum())
# print((arr < 40000).sum()-(arr < 30000).sum())
# print((arr < 50000).sum()-(arr < 40000).sum())
# print(prices_cp)
# print(np.argmax(prices_cp))



# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C,S = np.cos(X), np.sin(X)
#
# plt.plot(X,C)
# plt.plot(X,S)
#
# plt.show()

# from pylab import *
#
# def f(x,y): return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)
#
# n = 256
# x = np.linspace(-3,3,n)
# y = np.linspace(-3,3,n)
# X,Y = np.meshgrid(x,y)
#
# contourf(X, Y, f(X,Y), 8, alpha=.75, cmap='jet')
# C = contour(X, Y, f(X,Y), 8, colors='black', linewidth=.5)
# show()
def huayu_paimai():

    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表.csv"
    prices = [] #成交价
    names = [] #名称
    quantities = [] #品相
    d_times = [] #订单生成日期
    ids = [] #id
    df = pd.read_csv(file_d, names=['id', 'name', 'quantity', 'price','d_time'])

    prices = df['price']
    ids = df['id']
    names = df ['name']
    quantities = df['quantity']
    d_times = df['times']
    price_sum = prices.sum() # 总销售额
    collections_count = prices.count() # 总销售数量





    # price_d = np.array([0, 50, 100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 200000,200000000])
    # labels = pd.cut(df.价值, price_d)
    # p_group = df['价值'].groupby([df['拍品类别'],labels])
    # p_max = p_group.max()
    # p_min = p_group.min()
    # p_count = p_group.count()
    # p_sum = p_group.sum()
    # p_max.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv',mode='a')
    #
    # p_min.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv',mode='a')
    # p_sum.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv',mode='a')
    # p_count.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv',mode='a')

    p_group = df['价值'].groupby([df['拍品类别']])
    p_max = p_group.max()
    p_min = p_group.min()
    p_max.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv', mode='a')
    p_min.to_csv('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍品_分析结果.csv',mode='a')

def huayu_paimai_time():
    file_d = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表.csv"
    df = pd.read_csv(file_d, names=['照片', '名称', '品相', '价格', '日期', '版本'])
    product_prices = df['价格'].values
    time_strs = df['日期']
    s_time = []
    product_prices_1 = []
    for a_time in time_strs:
        s_time.append(datetime.strptime(a_time, '%Y-%m-%d %H:%M:%S'))
    for i in range(len(product_prices)):
        product_prices_1.append(float(product_prices[i].removeprefix('¥')))

    product_new = pd.DataFrame({"价格":product_prices_1,"版本":df['版本'].values},index=s_time)
    # for p_name in ("一版币","二版币","三版币","四版币","新中国流通币","新中国纪念章","新中国金银币","民国硬币"):
    #     product_new_1 = product_new[product_new['版本'] == p_name]
    #     print(p_name)
    #     print(product_new_1.index.min())
    #     print(product_new_1.index.max())
    #     p_n = product_new_1.to_period('M')
    #     grouped = p_n.groupby(level=0)
    #     grouped.count().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表_分析结果_t.csv",mode="a")
    #     grouped.sum().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表_分析结果_t.csv",mode="a")

    product_new_1 = product_new[product_new['版本'].str.contains("一版币")]
    print(product_new_1)

    print(product_new_1.index.min())
    print(product_new_1.index.max())
    p_n = product_new_1.to_period('M')
    grouped = p_n.groupby(level=0)
    grouped.count().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表_分析结果_t.csv", mode="a")
    grouped.sum().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表_分析结果_t.csv", mode="a")
if __name__ == "__main__":
    huayu_paimai_time()





