from flask import Flask
from apis.user import app_user
from apis.product import app_product
from flask_cors import CORS
from apis.application import app_application
app = Flask(__name__)

#解决Chrome跨域失败的问题，在python flask中允许跨域
CORS(app, supports_credentials=True)
# CORS(app_product, supports_credentials=True)

#注册蓝图 参数 url_prefix="/api/product" 定义统一URL前缀，那么在 route 路径定义都可以去掉相同的前缀路径/api/product
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(app_application)


if __name__ == '__main__':
    # debug=True：调试模式，每次有代码修改保存时程序会自动重新热加载，不需要每次重新手动启动
    app.run(debug=True)