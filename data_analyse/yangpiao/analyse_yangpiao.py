import base64

import pandas as pd
import numpy as np
import os
from io import BytesIO
import plotly as py
import plotly.express as px
import jinja2
import matplotlib.pyplot as plt
from utils.rwyaml import get_yaml_data
#读取文件

def con_form():
    """合并表格"""
    yd = get_yaml_data('web_data','yangpiao.yml')
    item_n = yd['item_name']
    file_p = yd['file_path']
    file_n = yd['file_names']
    file_t = yd["file_name_of_target"]
    file_names = [file_p+x for x in file_n]
    i = 0
    for f in file_names:
        df_temp = pd.read_csv(f, encoding='utf-8', names=item_n)
        if i == 0:
            df = df_temp
            i =1
        else:
            df = pd.concat([df,df_temp])
    df.to_csv(file_t)




def a_yangpiao():
    """统计每周交易数据"""

    yp = get_yaml_data('web_data', 'yangpiao.yml') #读取配置数据
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))

    template = env.get_template('Template.html') #读取报告模版
    file_path = yp['analyse_data']["file_path"]

    fn_nt = yp["note_type_f"] #从配置数据中读取钞票类型文件路径
    fn_nd = yp['analyse_data']["file"] #从配置文件中读取文件路径
    fn_nd = [file_path + x for x in fn_nd]
    if yp['analyse_data']["include_item"] == 0:
        item_n = yp["item_name"]  # 从配置数据中读取表头
        df_detail = pd.read_csv(fn_nd[0], encoding='utf-8', names= item_n)
    else:
        df_detail = pd.read_csv(fn_nd[0], encoding='utf-8')
    zero_rows = df_detail[df_detail["price"]==0].index
    df_detail.drop(zero_rows,inplace=True) #删除落槌价为0的行
    df_detail["deal_price"] = df_detail.apply(lambda x:  x["price"]*(1+x["buyer_premium"]/100) * x["parities"] if x["parities"] else x["price"]*(1+x["buyer_premium"]/100), axis=1) #计算交易数据
    # 成交价分析
    df_notetype = pd.read_csv(fn_nt, encoding='utf-8', index_col='id')
    df = pd.merge(df_detail,df_notetype,on="note_number",how="left") # 合并两个表的数据
    df.to_csv(fn_nd[1]) #保存合并的数据
    # 一二三版币总成交表
    df_1 = df["deal_price"].describe()
    # 一二三版各自统计表
    df_2 = df[["deal_price", "rid"]].groupby(["rid"]).describe()
    # 合并 df_1 和 df_2
    df_2.columns = yp["analyse_data"]["analyse_item"]
    df_3 = pd.DataFrame(np.insert(df_2.values,0,values=df_1.values,axis=0))
    df_3.index = ["总数","一版","二版","三版"]
    df_3.columns = yp["analyse_data"]["analyse_item"]
    table1 = df_3.round(2).to_html()
    table_did_num = df_3["count"][1:]
    print(df_3)

    df_3["deal_price"] = df_3["count"] * df_3["mean"]
    table_price = df_3["deal_price"][1:]

    # 调节图形大小fig = plt.figure(figsize=(6,9))
    fig = plt.figure()
    # 设置字体大小
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # plt.rcParams['axes.unicode_minus'] = False

    plt.rcParams["font.size"] = 15
    #定义标签
    lable_pie = ["1版", "2版", "3版"]
    plt.pie(table_did_num,labels=lable_pie,autopct="%3.1f%%")
    fig.savefig('fig1.png')
    plt.close()
    plt.rcParams["font.size"] = 15
    # 定义标签
    lable_pie = ["1版", "2版", "3版"]
    fig = plt.figure()
    plt.pie(table_price, labels=lable_pie, autopct="%3.1f%%")
    fig.savefig('fig2.png')




    plt.close()

    # 最高、最低价纸币表格
    p_max = df[df["deal_price"] == df["deal_price"].max()][["title","note_number","cert_display","cert_comments","serial","deal_price"]]
    p_max.name = "最高成交价纸币"
    # 最低价格的纸币
    p_min = df[df["deal_price"] == df["deal_price"].min()][["title","note_number","cert_display","cert_comments","serial","deal_price"]]
    p_max.name = "最低成交价纸币"
    # 最高、最低价纸币合并
    p_mm = pd.concat([p_max,p_min])
    p_mm.rename(columns={"title":"品种","note_number":"钞票编号","cert_display":"评级分数","cert_comments":"背标","serial":"号码","deal_price":"成交价"},inplace=True)

    p_r1_max = df[(df["deal_price"] == df_3.iat[1, 7]) & (df["rid"] == 1)]
    p_r1_min = df[(df["deal_price"] == df_3.iat[1, 3]) & (df["rid"] == 1)]
    p_r2_max = df[(df["deal_price"] == df_3.iat[2, 7]) & (df["rid"] == 2)]
    p_r2_min = df[(df["deal_price"] == df_3.iat[2, 3]) & (df["rid"] == 2)]
    p_r3_max = df[(df["deal_price"] == df_3.iat[3, 7]) & (df["rid"] == 3)]
    p_r3_min = df[(df["deal_price"] == df_3.iat[3, 3]) & (df["rid"] == 3)]
    p_mm = pd.concat([p_r1_max,p_r1_min,p_r2_max,p_r2_min,p_r3_max,p_r3_min])[["title","note_number","cert_display","cert_comments","serial","deal_price"]]
    p_mm.rename(
        columns={"title": "品种", "note_number": "编号", "cert_display": "评级分数", "cert_comments": "背标", "serial": "号码",
                 "deal_price": "成交价"}, inplace=True)
    p_mm.reset_index(drop=True,inplace=True)
    print(p_mm)
    # p_mm.index = ["一版最高","一版最低","二版最高","二版最低", "三版最高", "三版最低"]


    table2= p_mm.to_html().replace("NaN","")
    deal_t = data_yp["deal_time"]
    html_str = """
    <div>交易时间：{}</div>
    <h1>一、成交概览</h1>
    <h2>1、具体数据</h2>
    {}
    <h2>2、三个版本成交数量对比</h2>
    <div>
    <img src=/Users/yuanyuanhe/PycharmProjects/data_analyse/yangpiao/fig1.png />
    </div>
    <h2>3、三个版本总成交价对比</h2>
    <div>
    <img src=/Users/yuanyuanhe/PycharmProjects/data_analyse/yangpiao/fig2.png />
    </div>
    <h2>4、三个版本的最高最低成交价</h2>
    <div>
    {}
    </div>
    """.format(deal_t,table1,table2)




    

    html = template.render(summary=html_str)
    with open(fn_nd[2], 'w') as f:
        f.write(html)



def shangping(f,score):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))

    template = env.get_template('Template.html')
    item_n = ["id",	"note_number",	"serial",	"special_no",	"cert_display",	"cert_comments",	"special_pattern",	"price",	"buyer_premium",	"currency_type",	"deal_time",
              "from_id","is_1","is_2"]
    file_path = "/Users/yuanyuanhe/Desktop/"+f+".csv"
    df1 = pd.read_csv(file_path, encoding='utf-8', names=item_n)
    df1["did_price"] = df1["price"] * (1+df1["buyer_premium"]/100)

    df1["deal_time"] = pd.to_datetime(df1["deal_time"],unit="s")

    # 筛选某个分数
    df_1 = df1[df1["cert_display"]==score]["did_price"].describe()
    # 合并 df_1 和 df_2

    df_1.columns = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]



    print(df1[df1["cert_display"]==score][["note_number","serial","special_no","cert_display","cert_comments", "special_pattern", "did_price","deal_time"]])

    table1 = df1[df1["cert_display"]==score][["note_number","serial","special_no","cert_display","cert_comments", "special_pattern", "did_price","deal_time"]].sort_values(by="did_price").to_html().replace("NaN","")
    # table2 = df_1.to_html()



    # 调节图形大小fig = plt.figure(figsize=(6,9))
    fig = plt.figure()
    # 设置字体大小
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # plt.rcParams['axes.unicode_minus'] = False

    plt.rcParams["font.size"] = 10
    # 定义标签

    plt.plot(df1["deal_time"],df1["did_price"],"*")
    fig.savefig('fig1.png')
    plt.close()


    html_str = """
       <div></div>
       <h1>一、{}成交概览</h1>
       <h2>1、具体数据</h2>
       {}
       <h2>2、成交活跃性</h2>
       <div>
       <img src=fig1.png />
       </div>
      
       
      
       """.format(f,table1)
    return html_str
    # html = template.render(summary=html_str)
    # with open('Report.html', 'w') as f:
    #     f.write(html)




# 画一个箱型图。
#     fig = px.box(data_frame=df, x='one', y='two')
#     chart = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

def shangping_1(f):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))

    template = env.get_template('Template.html')
    item_n = ["id", "note_number", "serial", "special_no", "cert_display", "cert_comments", "special_pattern", "price",
              "buyer_premium", "currency_type", "deal_time",
              "from_id", "is_1", "is_2"]
    file_path = "/Users/yuanyuanhe/Desktop/" + f + ".csv"
    df1 = pd.read_csv(file_path, encoding='utf-8', names=item_n)
    df1["did_price"] = df1["price"] * (1 + df1["buyer_premium"] / 100)

    # df1["时间"] = pd.to_datetime(df1["time"], unit="s")
    # df1["完成时间"] = pd.to_datetime(df1["完成时间"], unit="s")
    df1.to_csv("/Users/yuanyuanhe/Desktop/" + f + "-1.csv")

def time_changge():
    file_path = "/Users/yuanyuanhe/Desktop/推广订单-业务员.csv"
    df1 = pd.read_csv(file_path, encoding='utf-8')


    df1["时间"] = pd.to_datetime(df1["时间"], unit="s")
    df1["完成时间"] = pd.to_datetime(df1["完成时间"], unit="s")
    df1.to_csv("/Users/yuanyuanhe/Desktop/推广订单-业务员-1.csv")

# 画一个箱型图。
#     fig = px.box(data_frame=df, x='one', y='two')
#     chart = py.offline.plot(fig, include_plotlyjs=False, output_type='div')
if __name__ == "__main__":
    # f = ["红二平","蓝三平",""]
    # s_877f = ["PMG 66EPQ","PMG 67EPQ","PMG 68EPQ"]
    # str_877f_1 = shangping(f877,s_877f[0])
    # str_877f_2 = shangping(f877, s_877f[1])
    # str_877f_3 = shangping(f877, s_877f[1])
    #
    #
    # with open('Report.html', 'w') as f:
    #     f.write(html)
    a_yangpiao()
    # shangping_1("123版币20230306")



