import csv
from collections import namedtuple
import pymysql as mysql
config={
    'host': '115.159.111.166',
    'port': 3306,
    'user': 'luckgirl',
    'database': 'pm2.0',
    'password': '2lc2g6rl'

}

csv_filename = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/钞票编号_数据库.csv"
table_name = "t_note_type"

def  get_data(file_name):
    with open(file_name, mode='r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for r in f_csv:
            yield Row(*r)
def execute_sql(conn,sql):
    with conn.cursor() as cur:
        cur.execute(sql)


def put_data():
    try:

        conn = mysql.connect(**config)
        conn.autocommit(True)
        print("连接成功")


        sql_format = "insert into t_note_type(rid,nid,note_number,title,is_specimen) values({0},{1},'{2}','{3}','{4}')"
        for nt in get_data(csv_filename):


            sql = sql_format.format(nt.rid, nt.nid, nt.note_number, nt.title.replace('\xa0\xa0','&nbsp'), nt.is_specimen)

            r= conn.cursor().execute(sql)
            conn.commit()



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


        sql_format = "insert into t_note_type(rid,nid,note_number,title,is_specimen) values({0},{1},'{2}','{3}','{4}')"



        sql = sql_format.format(1, 1, 'ddd','dd' , 0)

        conn.cursor().execute(sql)
        conn.commit()
        print(sql)


        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        print("连接失败")
def get_data_from_db():
    try:

        conn = mysql.connect(**config)
        print("连接成功")


        sql = "select * from  t_note_type"

        result  = execute_sql(conn, sql)
        print(result)

        conn.close()


    except Exception as e:
        print(e)
        print("连接失败")

def create_table():
    try:

        conn = mysql.connect(**config)
        conn.autocommit(1)
        print("连接成功")
        mycur = conn.cursor()

        sql = "create table t_note_type(id INT AUTO_INCREMENT PRIMARY KEY, rid INT NOT NULL,nid INT NOT NULL, " \
              "note_number VARCHAR(20) NOT NULL, title VARCHAR(100) NOT NULL, is_specimen TINYINT NOT NULL DEFAULT 0)"
        mycur.execute(sql)




    except Exception as e:
        print(e)
        print("连接失败")

def show_db():
    conn = mysql.connect(**config)
    mycur = conn.cursor()
    mycur.execute("show databases")
    for x in mycur:
        print(x)
if __name__ == '__main__':
    show_db()



