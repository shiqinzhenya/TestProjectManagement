from flask import Blueprint, request
from dbutils.pooled_db import PooledDB
from configs import config
import pymysql.cursors
from configs import format
import json

pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database = config.MYSQL_DATABASE, cursorclass=pymysql.cursors.DictCursor)

app_request = Blueprint("app_request", __name__)

# 查询所有的提测信息
@app_request.route("/api/testmanager/product", methods=["POST"])
def searchBykey():
    body = request.get_data()
    body = json.loads(body)
    print(body)
    response = format.resp_format_success

    sql = ""

    pagesize = 10 if body['pageSize'] is None else body['pageSize']
    currentPage = 1 if body['currentPage'] is None else body['currentPage']

    if 'productId' in body and body['productId']:
        sql = sql + " AND A.productId LIKE '%{}%'".format(body['productId'])
    if 'appId' in body and body['appId']:
        sql = sql + " AND A.appId LIKE '%{}%'".format(body['appId'])
    if 'tester' in body and body['tester']:
        sql = sql + " AND R.tester LIKE '%{}%'".format(body['tester'])
    if 'developer' in body and body['developer']:
        sql = sql + " AND R.developer LIKE '%{}%'".format(body['developer'])
    if 'status' in body and body['status']:
        sql = sql + " AND R.status = '{}'".format(body['status'])
    if 'pickTime' in body and body['pickTime']:
        sql = sql + " AND R.update >= '{}' and R.update <= '{}".format(body['pickTime'][0], body['pickTime'][1])

    #排序和页数拼接
    sql_all = sql + ' ORDER BY `updateDate` DESC LIMIT {},{}'.format((currentPage-1)*pagesize, pagesize)

    #使用连接池连接
    connection = pool.connection()
    with connection:
        with connection.cursor() as cursor:
            sql_total = "SELECT COUNT(*) as `count` FROM request AS R, apps AS A WHERE A.appId = R.appId and R.isDel=0" + sql
            print(sql_total)
            cursor.execute(sql_total)
            total = cursor.fetchall()
            print(total)

        with connection.cursor() as cursor:
            sql_search = "SELECT A.appId, R.* FROM request AS R, apps AS A WHERE A.appId = R.appId and R.isDel=0" + sql_all
            cursor.execute(sql_search)
            data = cursor.fetchall()
        response = format.resp_format_success
        response['data'] = data
        response['total'] = total
    return response


    

    

