#encoding=utf-8
import csv
from collections import namedtuple
import pymysql as mysql
from utils import times
''''charset':'utf8mb4','''
config={
    'host': '115.159.111.166',
    'port': 3306,
    'user': 'luckgirl',
    'database': 'pm2.0',
    'password': '2lc2g6rl',
    'charset': 'utf8'

}

csv_filename = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币_数据库.csv"
table_name = "t_note_type"

def  get_data(file_name):
    '''从文件中获取数据'''
    with open(file_name, mode='r', encoding='utf-8') as f:
        print("读数据1")
        f_csv = csv.reader(f)
        headings = next(f_csv)
        print(headings )
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
    print(mycur.description)
    for x in mycur:
        print( x)
def desc_t(table_name):
    '''显示数据库中表的各个列， 类似describe  '''
    conn = mysql.connect(**config)
    mycur = conn.cursor()
    sql = "show columns from " + table_name
    mycur.execute(sql)
    data = mycur.fetchall()
    print(data)

def execute_sql(conn,sql):
    with conn.cursor() as cur:
        cur.execute(sql)



def select_data(sql):
    '''查询数据
    sql : 数据库查询语句
    sql = "select * from  t_note_type limit 4 offset 1"
    '''
    try:
        conn = mysql.connect(**config)
        print("连接成功")
        mycur =conn.cursor()
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
    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        sql_format = "insert into t_note_detail(note_number,serial,special_no,cert_display,cert_comments,special_pattern,price,buyer_premium,currency_type,deal_time) " \
                     "values('{0}','{1}','{2}','{3}','''{4}''','{5}',{6},{7},{8},{9})"
        print(sql_format)
        i = 1
        for nt in get_data(csv_filename):
            print(i)
            sql = sql_format.format(nt.noteNumber, nt.serial,nt.special_no, nt.cert_display, nt.cert_comments, nt.i,nt.price, nt.buyer_premium, 1 if nt.currency=='RMB' else 2 if nt.currency=='HKD' else 3,nt.dealTime)
            r= conn.cursor().execute(sql)
            i = i+1
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        print("连接失败")
def put_data1():
    try:
        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")
        sql_format = "insert into t_note_currency(name,parities) values('{0}',{1})"
        sql_values = [
            ("RMB",0),
            ("HKD",0.85502),
            ("USD",6.6177)
        ]
        for val in sql_values:
            sql = sql_format.format(val[0],val[1])

            conn.cursor().execute(sql)


        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        print("连接失败")

if __name__ == '__main__':
    sql = "select max(deal_time) from t_note_detail "
    select_data(sql)





