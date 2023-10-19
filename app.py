from flask import Flask, session

import context_processors
from settings import Config, db
from index_page import index_page
from list_page import list_page
from detail_page import detail_page
from user import user_page

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "123@123"

db.init_app(app)

# 注册蓝图到程序实例
app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(list_page, url_prefix="/")
app.register_blueprint(detail_page, url_prefix="/")
app.register_blueprint(user_page, url_prefix="/")

app.before_request(context_processors.inject_user)


@app.context_processor
def inject_user():
    if "username" in session:
        return dict(current_user=session["username"])
    return dict(current_user=None)


if __name__ == '__main__':
    app.run()
