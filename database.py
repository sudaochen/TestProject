#pymysql   纯python工具，连接mysql，查找，执行  connect  cursor  execute fetch
import pymysql
db=pymysql.connect(
    host='stuq.ceshiren.com',
    user='hogwarts_python',
    password='hogwarts_python',
    db='hogwarts_python',
    charset='utf8mb4'
)

def test_conn():
    with db.cursor() as cursor:
        sql='show tables;'
        cursor.execute(sql)
        print(sql)
        print(cursor.fetchall())