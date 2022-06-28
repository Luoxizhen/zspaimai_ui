import pymysql as mysql

user_name = ""
password = ""
database = ""
port = ""
host = ""



try:
    con = mysql.connect(host="")
    print("连接成功")
    mycur = con.cursor()
    sql = "select * from "
    result = pd.
except Exception as e:
    print(e)
    print("连接失败")


