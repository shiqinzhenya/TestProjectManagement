import pymysql.cursors


#连接数据库
connection = pymysql.connect(
    host='localhost',  #数据库IP地址或连接域名
    user='root',  #用户名
    passwd='root', #密码
    database='TPMDatas', #数据库名
    charset='utf8mb4', #编码格式
    cursorclass=pymysql.cursors.DictCursor #结果作为字典返回游标
)
try:
    conn = pymysql.connect(host='localhost', user='root', password='root', db='TPMDatas')

    with conn.cursor() as cursor:
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        if result == (1,):
            print("Successfully connected to the database.")
        else:
            print("Something went wrong.")
except pymysql.MySQLError as e:
    print(f"An error occurred: {str(e)}")