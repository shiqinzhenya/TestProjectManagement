# 创建 用户登录、获取用户信息的蓝图

from flask_cors import CORS 
from flask import Flask
from flask import request
import json

#使用 Blueprint 来进行模块化的管理和开发
from flask import Blueprint
app_user = Blueprint("app_user", __name__)

#用户登录
@app_user.route("/api/user/login", methods = ["POST"])
def login():
    data = request.get_data()
    js_data = json.loads(data)

    if "username" in js_data and js_data["username"] == "admin":
        result_success = {"code":20000, "data":{"token":"admin-token"}}
        return result_success
    else:
        result_error = {"code":60204, "message":"账号密码错误"}
        return result_error

#获取用户信息    
@app_user.route("/api/user/info", methods = ["GET"])
def info():

    #从URL请求“http://127.0.0.1:5000/api/user/info?token=admin-token”中获取token信息
    token = request.args.get("token")
    if token == "admin-token":
        result_success = {
            "code": 20000,
            "data": {
                "roles": ["admin"],
                "introduction": "I am a super administrator",
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "name": "Super Admin"}
                        }
        return result_success
    else:
        result_error = {"code":60204, "message":"用户信息获取错误"}
        return result_error

# if __name__ == "__main__":
#     app_user.run(debug=True)
    