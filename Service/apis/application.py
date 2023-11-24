from flask import Blueprint, request
from dbutils.pooled_db import PooledDB
from configs import config
import pymysql.cursors
from configs import format
import json

#使用数据库连接池的方法连接数据库，提高资源利用率
pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database = config.MYSQL_DATABASE, cursorclass=pymysql.cursors.DictCursor)
#cursorclass=pymysql.cursors.DictCursor 查询结果返回一个字典，否则返回的元组
#定义蓝图
app_application = Blueprint("app_application", __name__)

#查询所有的应用
@app_application.route("/api/application/product", methods=["GET"])
def getProduct():
    connection = pool.connection()

    with connection.cursor() as cursor:
        sql = "SELECT id, keyCode, title FROM `products` WHERE `status`=0 ORDER BY `update` DESC " 
        cursor.execute(sql)
        data = cursor.fetchall()
    #按照返回模版进行json返回
    response = format.resp_format_success
    response['data'] = data
    return response

#按条件查询，并实现分页查询
@app_application.route("/api/application/search", methods=["POST"])
def searchBykey():

    # 获取POST的body
    body = request.get_data()
    body = json.loads(body)
    print(body)

    #基础语句
    sql = ""

    #获取pagesize
    pagesize = 10 if body['pageSize'] is None else body['pageSize']
    currentPaege = 1 if body['currentPage'] is None else body['currentPage']

    #拼接
    if 'appId' in body and body['appId']:
        sql = sql + " AND `appId` = '{}'".format(body['appId'])
    if 'productId' in body and body['productId']:
        sql = sql + " AND `productId` = '{}'".format(body['productId'])
    if 'note' in body and body['note']:
        sql = sql + " AND `note` = '{}'".format(body['note'])
    if 'developer' in body and body['developer']:
        sql = sql + " AND `developer` = '{}'".format(body['developer'])
    if 'tester' in body and body['tester']:
        sql = sql + " AND `tester` = '{}'".format(body['tester'])
    if 'producer' in body and body['producer']:
        sql = sql + " AND `producer` = '{}'".format(body['producer'])
    
    #排序和页数拼接
    sql_all = sql + ' ORDER BY `updateDate` DESC LIMIT {},{}'.format((currentPaege-1)*pagesize, pagesize)

    print(sql)

    #使用连接池连接数据库
    connection = pool.connection()
    with connection:
        with connection.cursor() as cursor:
            sql_total = "SELECT COUNT(*) as `count` FROM `apps` WHERE `status`=0" + sql
            print(sql_total)
            cursor.execute(sql_total)
            total = cursor.fetchall()
            # print(total)
        
        with connection.cursor() as cursor:
            sql_search = 'SELECT P.title, A.* FROM apps AS A,products AS P WHERE A.productId = P.id and A.`status`=0' + sql_all
            # print(sql_search)
            cursor.execute(sql_search)
            data = cursor.fetchall()

        response = format.resp_format_success
        print(total)
        response['total'] = total[0]['count']
        response['data'] = data
    return response
