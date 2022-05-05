import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
import pandas as pd
from utils import times
from pandas import Series,DataFrame


def get_child_file(father_path):
    file_list = os.listdir(father_path)
    for f in file_list:
        if (f[0]=='.'):
            file_list.remove(f)
    return (file_list)

def huayu_paimai():
    father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币/"
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果/"
    file_list = get_child_file(father_dir)
    '''
    products_analysis_result = {}
    for f in file_list:
        file_d = father_dir + f #文件路径
        file_name = f.removeprefix('.csv') # 文件名
        df = pd.read_csv(file_d, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id') # 将拍品信息解析为dataframe
        file_d_result = father_dir_result + file_name + '.csv'
        products_desc = {}
        d_time1 = df['d_time'].max()
        d_time2 = df['d_time'].min()
        products_desc['开始成交日'] = d_time1
        products_desc['结束成交日'] = d_time2
        products_desc['总拍卖天数'] = times.dif_days(d_time2,d_time1)
        products_desc['总成交量'] = df.name.count()
        products_desc['总拍品类目'] = len(df['name'].value_counts().index.value_counts())
        products_desc['最大成交价'] = round(df['price'].max(),2)
        products_desc['最小成交价'] = round(df['price'].min(),2)
        products_desc['总成交额'] = round(df['price'].sum(),2)
        products_desc['平均成交价'] = round(df['price'].mean(),2)
        products_analysis_result[file_name] = products_desc
    df_result = pd.DataFrame(products_analysis_result)
    df_result.to_csv(father_dir_result + '钱币分析概况.csv')
    '''
    result = pd.DataFrame()

    for f in file_list:
        file_name = f.removesuffix('.csv')
        df = pd.read_csv(father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
        product_name = df['name'].value_counts().idxmax()
        # df_top5 = df.sort_values(by='price',ascending=False)
        df_top = df[df['name'] == product_name]
        df_top['keys'] = file_name

        result = pd.concat([result,df_top])
    result.to_csv(father_dir_result + '每类钱币交易最活跃的信息.csv')





def huayu_desc():
    father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币/"
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果/"
    file_list = get_child_file(father_dir)
    result = pd.DataFrame()
    for f in file_list:
        file_name = f.removesuffix('.csv')
        df_raw = pd.read_csv(father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
        df = df_raw.drop_duplicates()
        df_dscrb = df['price'].describe()
        df_dscrb.name = file_name
        d_time1 = df['d_time'].max()
        d_time2 = df['d_time'].min()
        df_dscrb['总拍品类目'] = len(df['name'].value_counts().index.value_counts())
        df_dscrb['总成交额'] = round(df['price'].sum(), 2)
        df_dscrb['开始成交日'] = d_time1
        df_dscrb['结束成交日'] = d_time2
        df_dscrb['总拍卖天数'] = times.dif_days(d_time2, d_time1)
        result = pd.concat([result, df_dscrb],axis=1)
        result.to_csv(father_dir_result + '每类钱币交易信息科学分析结果.csv')



def huayu_desc_top():
    father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币/"
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果/"
    file_list = get_child_file(father_dir)
    result = pd.DataFrame()
    for f in file_list:
        file_name = f.removesuffix('.csv')
        df_raw = pd.read_csv(father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
        df = df_raw.drop_duplicates()
        df_top = df[df['price']>10000]
        df_top['key'] = file_name
        result = pd.concat([result,df_top])
    result.to_csv(father_dir_result + "高端拍品.csv")
    group = result.groupby('key')
    result2 = pd.concat([group['price'].describe(),group['price'].sum()],axis=1)
    result2.to_csv(father_dir_result + "高端拍品概况.csv")
    result3 = result.sort_values(by='price',ascending=False).head(100)
    result3.to_csv(father_dir_result + "高端拍品top100.csv")




def huayu_active_top():
    '''华宇拍卖交易活跃信息分析'''
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果/每类钱币交易最活跃的信息.csv"
    df = pd.read_csv(father_dir_result)
    group1 =df['name'].groupby(df['keys'])#每一类拍品的交易次数

    group2 = df['price'].groupby(df['keys']) # 每一类拍品的交易价格分析

    group3 = df['d_time'].groupby(df['keys'])
    df_name_keys = df[['name','keys']].drop_duplicates().set_index('keys')

    result = pd.concat([df_name_keys,group1.count(),group2.mean(),group2.max(),group2.min(),group3.min(),group3.max()],axis=1)

    result.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果/"+"活跃交易钱币分析.csv")




if __name__ == "__main__":
    huayu_desc_top()





