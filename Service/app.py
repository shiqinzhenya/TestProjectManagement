from flask import Flask
from apis.user import app_user
from apis.product import app_product
from flask_cors import CORS
app = Flask(__name__)

#解决Chrome跨域失败的问题，在python flask中允许跨域
CORS(app_user, supports_credentials=True)
CORS(app_product, supports_credentials=True)

#注册蓝图
app.register_blueprint(app_user)
app.register_blueprint(app_product)

if __name__ == '__main__':
    app.run(debug=True)