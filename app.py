from flask import Flask
from settings import Config, db
from index_page import index_page
from list_page import list_page

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 注册蓝图到程序实例
app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(list_page, url_prefix="/")

if __name__ == '__main__':
    app.run()
