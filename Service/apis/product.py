#实现产品管理页面
from flask import Blueprint
import pymysql.cursors
from flask import request
import json
app_product = Blueprint("app_product", __name__)


#连接数据库

#封装
def connectDB():
    connection = pymysql.connect(
        host='localhost',  #数据库IP地址或连接域名
        user='root',  #用户名
        passwd='root', #密码
        database='TPMDatas', #数据库名
        charset='utf8mb4', #编码格式
        cursorclass=pymysql.cursors.DictCursor #结果作为字典返回游标
    )

    return connection

# get方法获取产品信息
#@—-- flask提供的装饰器，作用是将指定的 URL 路径和对应的请求方法（GET）映射到特定的处理函数。当服务器接收到 "/api/product/list" 的 GET 请求时，get_product_list() 函数就会被调用，获取产品列表，并返回给客户端。
@app_product.route("/api/product/list",methods = ["GET"]) 
def product_list():
    #初始化连接
    connection = connectDB()
    #使用python的with 。。 as 控制流语句（相当于简化的try excpt finally）
    with connection.cursor() as cursor:
        #查询表信息并更新新旧排序
  
        sql = "SELECT * FROM `Products` WHERE `status`=0 ORDER BY `update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()
    

    # #硬编码返回list
    # data = [
    #     {"id":1, "keyCode":"project1", "title":"项目一", "desc":"这是项目一的描述", "operator":"admin", "update":"2020-04-06"},
    #     {"id":2, "keyCode":"project2", "title":"项目二", "desc":"这是项目二的描述", "operator":"user", "update":"2020-04-03"}
    # ]

    #按照返回模版格式进行json结果返回

    resp_data = {
        "code": 20000,
        "data": data
    }

    return resp_data

#[post方法] 实现新建数据的数据库插入。
@app_product.route("/api/product/create", methods=["POST"])
def product_create():
    #初始化数据库
    connection = connectDB()
    #定义默认的返回体结构
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    #获取用户传递的请求的请求体（body），并解析成json格式
    body = request.get_data()
    body = json.loads(body)

    with connection:
        #首先查询数据库， 判断keycode（唯一关键字）是否重复
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s and `status`=0"
            cursor.execute(select, body['keyCode'])
            result = cursor.fetchall()
        
        # 判断查询的keycode是否已经存在于数据库中，如果已有，直接返回提示
        if result:
            resp_data["code"] = 20001
            resp_data["message"] = "唯一编码keyCode已存在"
            return resp_data
        
        #如果没有，则实现数据库插入
        with connection.cursor() as cursor:
            # 永远不要使用用户的输入来拼接sql语句！！用参数化%s构造防止基本的SQL注入
            # 其中id为自增，插入数据默认数据设置的当前时间
            insert = "INSERT INTO `products` (`keyCode`, `title`, `desc`, `operator`) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert, (body["keyCode"], body["title"], body["desc"], body["operator"]))
            connection.commit()
        return resp_data
    
@app_product.route("/api/product/update",methods=["POST"])
def product_update():
    connection = connectDB()
    resp_data={
        "code": 20000,
        "message": "success",
        "data": []
    }
    body = request.get_data()
    body = json.loads(body)
    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`= %s  and `status`=0"
            cursor.execute(select, body['keyCode'])
            result = cursor.fetchall()
        if result:
            resp_data['code'] = 20001
            resp_data['message'] = "the Unique Code 'keyCode' Has Been Exited!"
            return resp_data
        
        #更新产品
        with connection.cursor() as cursor:
            update = "UPDATE `products` SET `keyCode`=%s, `title`=%s,`desc`=%s,`operator`=%s, `update` = NOW() WHERE id=%s"
            cursor.execute(update, (body["keyCode"], body["title"], body["desc"], body["operator"], body['id']))
            connection.commit()
        return resp_data
    

@app_product.route("/api/product/delete", methods=["DELETE"])
def product_delete():
    connection = connectDB()
    resp_data={
        "code": 20000,
        "message": "success",
        "data": []
    }
    #方式一：通过params 获取id（ 即URL中 '?' 后面的部分）
    ID = request.args.get('id')
    # 做个参数必填校验
    if not ID:
        resp_data['id'] = 20002
        resp_data['message'] = "请求参数为空"
        return resp_data
    
    with connection.cursor() as cursor:
        delete = "DELETE from `products` WHERE id=%s"
        cursor.execute(delete, ID)
        connection.commit()
    return resp_data

@app_product.route("/api/product/remove", methods=["POST"])
def product_remove():
    connection = connectDB()
    resp_data={
        "code": 20000,
        "message": "success",
        "data": []
    }
    #方式一：通过params 获取id（ 即URL中 '?' 后面的部分）
    ID = request.args.get('id')
    # 做个参数必填校验
    if not ID:
        resp_data['id'] = 20002
        resp_data['message'] = "请求参数为空"
        return resp_data
    
    with connection.cursor() as cursor:
        remove = "UPDATE `products` SET `status`=1 WHERE id=%s"
        cursor.execute(remove, ID)
        connection.commit()
    return resp_data

# 根据title和keyCode实现模糊查询
@app_product.route("/api/product/search", methods = ["GET"])
def product_search():
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')
    resp_data = {
        'code': 20000,
        'data': ''
    }
    
    # 定义默认的查询语句，默认查询全部
    sql = "SELECT * FROM `products` WHERE `status`=0"

    if title is not None:
        # sql中的模糊查询 like
        sql = sql + " AND `title` LIKE '%{}%'".format(title)
    if keyCode is not None:
        sql = sql + " AND `keyCode` LIKE '%{}%'".format(keyCode)

    # 排序最后拼接
    sql = sql + " ORDER BY `update` DESC"

    connection = connectDB()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        
    resp_data["data"] = result

    return resp_data 
    

    



    