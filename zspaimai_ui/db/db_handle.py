# encoding = utf-8
import csv
from collections import namedtuple
import pymysql as mysql
from utils import times,log
from common.readconfig import ini
''''charset':'utf8mb4','''
'''host': '115.159.111.166    'host': '81.71.30.169','''
host_url = ini.host_url
config={
    'host': host_url,
    'port': 3306,
    'user': 'luckgirl',
    'database': 'pm2.0',
    'password': '2lc2g6rl',
    'charset': 'utf8'
}

csv_filename = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币_数据库.csv"
table_name = "t_note_type"

def  get_data_not_headings(file_name):
    '''从文件中获取数据
    with open('Population.csv','a+',encoding='utf8') as csvfile:
      fieldnames=['openname','sqlname']#表头·
      writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
      writer.writerow({'openname':filtes,'sqlname':data})#数据'''
    with open(file_name, mode='r', encoding='utf-8') as f:
        fieldnames=["cert_display","cert_comments","noteNumber","serial","special","special_no","buyer_premium","did",
                    "is_clinch","price","parities","currency","dealTime","volamount"]
        print("读数据1")
        f_csv = csv.reader(f)
        headings = fieldnames
        Row = namedtuple('Row', headings)
        print("读数据")
        for r in f_csv:
            yield Row(*r)
def  get_data(file_name):
    with open(file_name, mode='r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        print(headings)
        Row = namedtuple('Row', headings)
        print("读数据")
        for r in f_csv:
            yield Row(*r)
def show_db():
    '''显示数据库服务器中的数据库'''
    conn = mysql.connect(**config)
    mycur = conn.cursor()
    mycur.execute("show databases")
    for x in mycur:
        print(x)

def show_t():
    '''显示数据库中的所有表，Tables_in_pm2.0
    description:(('Tables_in_pm2.0', 253, None, 64, 64, 0, False),)'''
    conn = mysql.connect(**config)
    mycur = conn.cursor()
    mycur.execute("show tables")
    print(mycur.rowcount)
    # print(mycur.description)
    for x in mycur:
        print( x)
def desc_t(table_name):
    '''显示数据库中表的各个列， 类似describe  '''
    conn = mysql.connect(**config)
    mycur = conn.cursor()
    sql = "show columns from " + table_name
    mycur.execute(sql)
    data = mycur.fetchall()
    # print(data)
    for x in data:
        print(x)



def delete_data(sql):

    '''delect from p_note_detail where rid=3 and nid=74'''
    try:
        conn = mysql.connect(**config)
        print("连接成功")
        mycur =conn.cursor()
        mycur.execute(sql)
        # result = mycur.fetchall() #从最后执行的语句中获取所有行，结果值赋给 result
        # for data in result:
        #     print(times.time_to_str(data[0]))
        # print(result)
        # print(mycur.rowcount)
    except Exception as e:
        print(e)



def select_data(sql):
    '''查询数据
    sql : 数据库查询语句
    sql = "select * from  t_note_type limit 4 offset 1"
    '''
    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        mycur =conn.cursor()
        mycur.execute(sql)
        conn.commit()
        conn.close()
        result = mycur.fetchall() #从最后执行的语句中获取所有行，结果值赋给 result
        for data in result:
            print(data)
            # print("{0},{1},{2},{3},{4},{5},{6},{7}".format(data[2],data[4],data[5],data[7],data[8],data[10],times.time_to_str(data[10]),data[12]))
    except Exception as e:
        print(e)
def alter_talbe():
    try:
        conn = mysql.connect(**config)
        print("连接成功")
        mycur =conn.cursor()
        sql = "alter table p_note_detail modify serial varchar(50) null"
        mycur.execute(sql)
        result = mycur.fetchall() #从最后执行的语句中获取所有行，结果值赋给 result
        for data in result:
            print(times.time_to_str(data[0]))
        print(result)
        print(mycur.rowcount)
    except Exception as e:
        print(e)

def create_table(table_name,sql):
    '''创建数据库
    table_name : 表名
    sql ： sql 语句
    sql = "create table {}(" \
              "id tinyint AUTO_INCREMENT PRIMARY KEY," \
              "name varchar(20)," \
              "parities double)".format(table_name)
    '''
    try:
        conn = mysql.connect(**config)
        conn.autocommit(1)
        print("连接成功")
        mycur = conn.cursor()
        mycur.execute("drop table if exists {} ".format(table_name))
        mycur.execute(sql)
    except Exception as e:
        print(e)
        print("连接失败")

def put_data():
    '''在表中插入数据'''
    csv_filename = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/抖音11-22-1.csv"
    log.log.info(csv_filename)
    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        sql_format = "insert into p_note_detail (note_number,serial,special_no,cert_display,cert_comments,special_pattern,price,buyer_premium,currency_type,deal_time,from_id,is_clinch,is_history) " \
                     "values('{0}','{1}','{2}','{3}','{4}','{5}',{6},{7},{8},{9},{10},{11},{12})"
        # sql_format ="insert into p_note_from (did,name) values({0},'{1}')"
        # print(sql_format)
        i = 1
        for nt in get_data_not_headings(csv_filename):
            # print(nt)
            print(i)
            log.log.info("插入{}".format(i))
            # "cert_display", "cert_comments", "noteNumber", "serial", "special", "special_no", "buyer_premium", "did",
            # "is_clinch", "price", "parities", "currency", "dealTime", "volamount"
            sql = sql_format.format(nt.noteNumber, nt.serial,nt.special_no,nt.cert_display.strip(),nt.cert_comments.replace("'"," "),nt.special,
                                    nt.price,nt.buyer_premium,1 if nt.currency=='RMB' else 2 if nt.currency=='HKD' else 3, nt.dealTime if type(nt.dealTime) == int else times.str_to_time(nt.dealTime.lstrip()), int(nt.did), nt.is_clinch, nt.volamount)

            # sql = sql_format.format(nt.noteNumber, nt.serial, nt.special_no, nt.cert_display.strip(),
            #                         nt.cert_comments.replace("'", " "), nt.special,
            #                         nt.price, nt.buyer_premium,
            #                         1 if nt.currency == 'RMB' else 2 if nt.currency == 'HKD' else 3,
            #                         nt.dealTime , int(nt.did), nt.is_clinch, nt.volamount)

            # sql = sql_format.format(nt.did,nt.name)
            log.log.info(sql)

            # if int(nt.dealTime) > 1665920116:
                # times.str_to_time("2022-07-01 00:00:00"):
            r = conn.cursor().execute(sql)
            i = i+1
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("连接失败")


def put_data2():
    '''在表中插入数据'''
    csv_filename = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/20221017/钞票编号_数据库.csv"
    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        sql_format = "insert into p_note_type (title,title_name,title_money,rid,nid,note_number,is_specimen) " \
                     "values('{0}','{1}','{2}',{3},{4},'{5}',{6})"
        print(sql_format)
        i = 1
        for nt in get_data(csv_filename):
            print(i)
            sql = sql_format.format(nt.title.replace('\xa0',''), nt.title_name.replace('\xa0',''),nt.title_money.replace('\xa0',''),nt.rid, nt.nid,nt.note_number, nt.is_specimen)
            r = conn.cursor().execute(sql)
            i = i+1
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("连接失败")
def put_data3(sql):
    '''在表中插入数据'''

    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        r = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("连接失败")
if __name__ == '__main__':

    sql = "select  distinct user_id  from p_goods_browse where id > ((select max(id) from p_goods_browse ) -74 )"
    select_data(sql)














