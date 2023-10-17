from flask import Flask, render_template, request, redirect, url_for
from settings import Config, db
from index_page import index_page
from list_page import list_page
from detail_page import detail_page
from user import user_page

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 注册蓝图到程序实例
app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(list_page, url_prefix="/")
app.register_blueprint(detail_page, url_prefix="/")
app.register_blueprint(user_page, url_prefix="/")

if __name__ == '__main__':
    app.run()
