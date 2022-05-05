import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from collections import Counter
from datetime import datetime
import pandas as pd
from utils import times
from pandas import Series,DataFrame
from datetime import datetime
class DataAnalyse():
    def __init__(self,f1,f2):

        # self.father_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/"
        # self.result_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/"
        self.father_dir = f1
        self.result_dir = f2
        self.file_list = self.get_child_file(self.father_dir)

    def get_child_file(self,father_path):
        '''获取文件夹中的所有文件'''
        file_list = os.listdir(father_path)
        for f in file_list:
            if (f[0]=='.'):
                file_list.remove(f)
        return (file_list)

    def zhao_describe(self):
        '''统计每类拍品的概要信息，总数，价格统计等'''
        result_t = pd.DataFrame()
        result_p = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'time'],index_col='id')
            df = df_raw.drop_duplicates()
            df_price_dsc = df['price'].describe() #series
            df_time_dsc1 = df['time'].describe()
            df_time_dsc = pd.to_datetime(df['time']).describe()
            #reating datetime data as categorical rather than numeric in `.describe` is deprecated and will be removed in a future version of pandas. Specify `datetime_is_numeric=True` to silence this warning and adopt the future behavior now.
            # df_time_dsc = df['time'].describe()
            df_price_dsc.name = file_name + 'p' #series 的name
            df_time_dsc.name = file_name + 't'
            result_t = pd.concat([result_t,df_time_dsc],axis=1)
            result_p = pd.concat([result_p, df_price_dsc], axis=1)
        result = pd.concat([result_p, result_t]) #横向链接
        result_p.to_csv(self.result_dir + '各类钱币交易信息科学分析结果.csv')
        result_t.to_csv(self.result_dir + '各类钱币交易信息科学分析结果.csv',mode="a")
    def zhao_4_month(self,f_out=[]):
        '''从拍品表中爬取 一定时间段内交易的拍品信息,并合并成一个总表'''
        result = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            if file_name not in f_out:
                df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'])
                df = df_raw.drop_duplicates()
                df['key']=file_name
                df['d_time'] = pd.to_datetime(df['d_time'])
                df_4_month = df[df['d_time']>datetime(2021,10,23)]
                # df['d_time'] = pd.to_datetime(df['d_time']) 根据时间提取字表的方式
                # df1 = df.set_index('d_time')
                # df2 = df1['2021-09-09':]
                result = pd.concat([result,df_4_month])
        result.drop_duplicates().to_csv(self.result_dir + '4个月的数据分析.csv')

    def zhao_group_describe(self,f):
        '''对拍品总表进行每类拍品的交易概况分析
        先分组，再对每一组数据进行分析'''
        # file_name ='4个月的数据分析.csv'
        file_name = f
        file_path = self.result_dir +file_name
        df = pd.read_csv(file_path)
        group1 = df.groupby('key') #按照拍品类型进行分组，group1 的数据类型为 [group_name,DataFrame]
        price_dsc = group1['price'].describe()
        print(price_dsc)
        # price_dsc.to_csv(self.result_dir + '4个月的数据分析结果.csv')

    def zhao_active(self):
        '''获取每类拍品名字出现最多次的拍品名称'''

        result = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
            df = df_raw.drop_duplicates()
            active_good_name = df['name'].value_counts().idxmax() # series = value_counts,idxmax 获取series 的index 索引，即拍品名称
            # df_top5 = df.sort_values(by='price',ascending=False)
            df_top = df[df['name'] == active_good_name] #获取字表，条件获取
            df_top['keys'] = file_name # 字表添加类型

            result = pd.concat([result,df_top]) #轴向链接
        result.to_csv(self.result_path + '每类钱币交易最活跃的信息.csv')



    def zhao_price_top5(self):
        '''获取每类拍品交易价格拍品前5的拍品信息'''
        # father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/"
        # father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/"
        # file_list = get_child_file(father_dir)
        result = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
            df = df_raw.drop_duplicates()
            df_top5 = df.sort_values(by='price',ascending=False).head(5) #根据价格进行倒序排序
            df_top5['keys'] = file_name
            result = pd.concat([result,df_top5])
        result.to_csv(self.result_path + '每类钱币交易价格top5.csv')


    def zhao_price_more_than(self,min_price):
        '''获取拍品价格>10000 的拍品信息'''
        result = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
            df = df_raw.drop_duplicates()
            # df_top5 = df.sort_values(by='price',ascending=False)
            df_top100 = df[df['price'] > min_price]
            df_top100['keys'] = file_name
            result = pd.concat([result,df_top100])
        result.drop_duplicates().to_csv(self.result_path + '每类钱币交易价格top100.csv')


    def zhao_max_min(self):
        '''获取最小最大成交价的拍品信息'''
        result = pd.DataFrame()
        for f in self.file_list:
            file_name = f.removesuffix('.csv')
            df_raw = pd.read_csv(self.father_dir + f, names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
            df = df_raw.drop_duplicates()
            df_max = df[df['price'] == df['price'].max()]
            df_min = df[df['price'] == df['price'].min()]
            df_top = pd.concat([df_max,df_min])
            df_top['keys'] = file_name
            result = pd.concat([result,df_top])
        result.to_csv(self.father_dir_result + '每类钱币交易最大最小成交价信息.csv')

    def zhao_mulit_describe(self):
        '''将多个表合成一个表，然后获取总表的基本概况'''
        names = ["纪念系列","熊猫系列","生肖系列"]
        df = pd.DataFrame()
        # 将3个表的数据合并
        for name in names:
            file_path = self.father_dir + "中国现代金银币-" + name + ".csv"
            df_c = pd.read_csv(file_path,names=['id', 'name', 'quantity', 'price', 'd_time'],index_col='id')
            df = pd.concat([df,df_c]) # 多表链接
        df = df.drop_duplicates() #金银币表去重
        # df.to_csv(self.result_dir +'中国现代金银币.csv')
        print(df.describe())

        # df.describe().to_csv(self.result_dir + '中国现代金银币分析概况.csv')

    def zhao_active_analyse(self):
        '''赵涌在线交易活跃信息分析,根据名字进行分组，对分组数据进行分析'''
        father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/每类钱币交易最活跃的信息.csv"
        df = pd.read_csv(father_dir_result)
        group = df.groupby([df['keys'],df['name']])

        # group['price'].describe().to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/" + "活跃交易钱币分析_1.csv")
        good_time_dsc = pd.DataFrame()
        for good in group:
            good_time = good[1]['d_time']
            good_time_d = pd.to_datetime(good_time).describe()
            good_time_d.name = good[0]
            good_time_dsc = pd.concat([good_time_dsc,good_time_d],axis=1)

        # print(good_time_dsc.T)
        good_time_dsc.T.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/" + "活跃交易钱币分析_1.csv",mode='a')

    def zhao_swa(self):
        '''赵涌在线交易最活跃的拍品价格分析,对单一拍品进行价格分析,按照天及按照月采样分析'''
        father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/苏维埃二百文.csv"
        df = pd.read_csv(father_dir_result)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df2 = df.set_index('datetime').resample('M')
        df3 = df.set_index('datetime').resample('D')
        df4 = df3.count()

        # pd.concat([df2.count(),df2.mean()],axis=1).to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/苏维埃二百文价格1.csv")


        pd.concat([df3.count(),df3.mean()], axis=1).dropna().to_csv(
            "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/苏维埃二百文价格2.csv")
    def zhao_time(self,f):
        '''按照时间进行分析'''

        file_path = self.result_dir + f
        df = pd.read_csv(file_path)
        df['d_time'] = pd.to_datetime(df['d_time'])
        df_temp = df.set_index('d_time')
        df_temp1 = df_temp['price'].resample('M')

        df1 = pd.concat([df_temp1.count(),df_temp1.sum()],axis=1,join='inner')
        df1[df1['price']>0].dropna().to_csv(self.result_dir + '4个月数据时间.csv',mode='a')

    def zhao_time1(self):
        '''按照时间进行分析'''
        df_all = pd.DataFrame()
        for f in self.file_list:
            file_path = self.father_dir + f
            df = pd.read_csv(file_path,names=['id', 'name', 'quantity', 'price', 'time'],index_col='time')
            df.index = pd.to_datetime(df.index)
            # df_temp = df.set_index('d_time')
            df_all = pd.concat([df_all,df])
        df_all = df_all['price'].resample('Y')
        df1 = pd.concat([df_all.count(), df_all.sum()], axis=1, join='inner')
        df1[df1['price'] > 0].dropna().to_csv(self.result_dir + '华宇拍卖_10年数据时间.csv', mode='a')

def get_child_file(self,father_path):
    '''获取文件夹中的所有文件'''
    file_list = os.listdir(father_path)
    for f in file_list:
        if (f[0]=='.'):
            file_list.remove(f)
    return (file_list)





def zhao_desc1():
    father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/中国现代金银币.csv"
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/"
    df = pd.read_csv(father_dir)
    df['d_time'] = pd.to_datetime(df['d_time'])
    df1 = df.set_index('d_time')
    df2 = df1['2021-09-09':]

    d_time1 = df2.index.max()

    d_time2 = df2.index.min()
    df_dscrb = df2['price'].describe()
    df_dscrb['总拍品类目'] = len(df2['name'].value_counts().index.value_counts())
    df_dscrb['总成交额'] = round(df2['price'].sum(), 2)
    df_dscrb['开始成交日'] = d_time1
    df_dscrb['结束成交日'] = d_time2
    df_dscrb['总拍卖天数'] = times.dif_days(str(d_time2), str(d_time1))
    df_dscrb.to_csv(father_dir_result + '金银币20210909.csv')



def zhao_top():
    '''赵涌在线、华宇拍卖高端市场分析'''
    files = [["中国现代金银币-纪念系列","中国现代金银币-生肖系列","中国现代金银币-熊猫系列","中国流通纪念币1","外国纪念币"],["新中国金银币","清代钱币","明国钱币","新中国流通币"]]
    father_dir_z = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/"
    father_dir_h = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币/"
    df_10000 = pd.DataFrame()
    for i in range(2):
        for f in range(len(files[i])):
            if i == 0:

                file_path = father_dir_z + files[i][f] + '.csv'
            else:
                file_path = father_dir_h + files[i][f] + '.csv'
            if files[i][f]=="中国现代金银币":
                df = pd.read_csv(file_path)
            else:
                df = pd.read_csv(file_path,names=['id', 'name', 'quantity', 'price', 'd_time'],encoding='utf-8')
            print(files[i][f])
            df1 = df[df['price']>10000]

            df1['key1'] = files[i][f]
            if i == 0:
                df1['key2'] = "赵涌在线"
            else :
                df1['key2'] = "华宇拍卖"
        df_10000 = pd.concat([df_10000,df1]).set_index('id')
    df_10000.to_csv("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/" + "高端市场产品.csv")


def zhao_top10000_analys():
    father_dir = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/高端市场数据/"
    father_dir_result = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/"
    filename= '每类钱币交易价格top100.csv'
    filepath = father_dir_result+ filename
    df = pd.read_csv(filepath)
    result = df.sort_values(by='price',ascending=False).head(100)


    result.drop_duplicates().to_csv(father_dir_result + '每类钱币交易价格top100_分析结果_top100.csv')


def zhao_top_active():
    file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/高端市场活跃数据.csv"
    result_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/高端市场活跃数据_分析.csv"
    df = pd.read_csv(file_path,names=['id','name','grade','price','time']).drop_duplicates()
    # df['name'] = df['name'].str.replace("第（1）组","第1组").str.replace("第（2）组","第2组").str.replace("第（3）组","第3组").str.replace("第（4）组","第4组").str.replace("第（4）组","第4组")
    # df['name'] = df['name'].str[:df['name'].str.rfind('（')]
    str_places = df['name'].str.rfind('（').values
    names = []
    for (name,str_place) in zip(df['name'].values,str_places):
        name = name[:str_place]
        names.append(name)
    df['name'] = names
    groups = df.groupby([df['name']])
    df_g = pd.DataFrame({'time':[],"price":[]})


    for group in groups:
        df_n = group[1][['time']]
        df_n[group[0]] = group[1]['price']

        df_g = pd.merge(df_g, df_n,how='outer',on='time')

    df_g.to_csv(result_path)

    # for group in groups:
    #     df_n = group[['time','price']]
    #     pd.merge([df_g,df_n])
    # print(df_g)


def zhao_top_active1():
    file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/高端拍品成交表1.csv"
    result_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/高端拍品成交表_分析.csv"
    df = pd.read_csv(file_path)

    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df=df.groupby(level=0).mean()

    df.to_csv(result_path)
def zhao_top_active2():
    result_path= "/Users/yuanyuanhe/Desktop/成交表/"
    file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/高端拍品成交表_分析.csv"

    df = pd.read_csv(file_path)

    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    d = df.iloc[:,1]
    print(d.name)

    for i in range(38):
        d = df.iloc[:,i+1].dropna()
        pd.DataFrame(d).to_csv(result_path + d.name.replace('/','之') + '.csv')












if __name__ == "__main__":
    f1 = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币/"
    f2 = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/2022年2月25日钱币分析结果"
    # f2 = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果20220318/"
    data_a = DataAnalyse(f1,f2)
    f = '4个月的数据分析.csv'
    # data_a.zhao_time(f)
    # data_a.zhao_swa()
    data_a.zhao_time1()










