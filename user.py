from flask import Blueprint, render_template, request, redirect, url_for, session, g, jsonify
from models import User, House
from settings import db
from werkzeug.security import generate_password_hash, check_password_hash

user_page = Blueprint("user_page", __name__)


#
@user_page.route("/user")
def user_home():
    current_user = session.get("username")
    print("current_user", current_user)
    if current_user:
        user_info = User.query.filter(User.name == current_user).all()
        if len(user_info) == 0:
            # 用户不存在, 返回登录
            return redirect(url_for("user_page.log_in"))
        else:
            user_info = user_info[0]
            return render_template("user_page.html", user_info=user_info)
    else:
        return redirect(url_for("user_page.log_in"))


@user_page.route("/log-in")
def log_in():
    return render_template("login.html")


@user_page.route("/login", methods=["POST"])
def login():
    username = request.form["uname"]
    password = request.form["pwd"]
    targets = User.query.filter(User.name == username).all()
    if len(targets) == 0:
        return render_template("login.html", error="用户名不存在")
    for u in targets:
        if check_password_hash(generate_password_hash(u.password), password):
            session["username"] = u.name
            return redirect(url_for("index_page.index"))
    return render_template("login.html", error="用户名或密码错误")


@user_page.route("/log-out")
def log_out():
    session.pop("username", None)
    return redirect(url_for("index_page.index"))


@user_page.route("/register-page")
def register_page():
    return render_template("register.html")


@user_page.route("/register", methods=["POST"])
def register():
    username = request.form["uname"]
    password = request.form["pwd"]
    confirm_password = request.form["confirm-pwd"]
    if len(User.query.filter(User.name == username).all()) == 0:
        if password == confirm_password:
            user = User(name=username, password=password)
            db.session.add(user)
            db.session.commit()
            session["username"] = username
            return render_template("index.html", info="注册成功")
        else:
            return render_template("register.html", error="两次输入密码不一致!")
    else:
        return render_template("register.html", error="用户名已存在")


# 用户编辑个人信息
@user_page.route("/edit_info", methods=["POST"])
def edit_info():
    current_user = g.current_user
    print(current_user)
    new_username = request.form["i_username"]
    new_password = request.form["i_password"]
    new_address = request.form["i_address"]
    new_email = request.form["i_email"]

    query = db.session.query(User).filter(User.name == current_user)
    data_to_update = {}
    if len(User.query.filter(User.name == new_username).all()) == 0 or current_user == new_username:
        if new_username:
            data_to_update["name"] = new_username
        if new_password:
            data_to_update["password"] = new_password
        if new_address:
            data_to_update["addr"] = new_address
        if new_email:
            data_to_update["email"] = new_email
    else:
        error = "用户已存在!"
        user_info = User.query.filter(User.name == current_user).one()
        return render_template("user_page.html", user_info=user_info, error=error)

    if data_to_update:
        query.update(data_to_update)
        if not new_username:
            pass
        else:
            session["username"] = new_username
        db.session.commit()

    return redirect(url_for("user_page.user_home"))


# 用户收藏
@user_page.route("/stars")
def stars():
    user_stars = User.query.with_entities(User.collect_id).filter(User.name == g.current_user).all()[0]
    if user_stars[0] is not None:
        user_stars = user_stars[0].split(",")
    else:
        user_stars = []

    # print(collections)
    result = []

    if len(user_stars) == 0:
        return jsonify({"code": 0, "stars": []})
    else:
        collections = House.query.filter(House.id.in_(user_stars)).all()
        for i in collections:
            result.append({
                "id": i.id,
                "title": i.title,
                "rooms": i.rooms,
                "area": i.area,
                "price": i.price,
                "direction": i.direction,
                "address": i.address,
                "traffic": i.traffic,
                "page_views": i.page_views
            })
        return jsonify({"code": 1, "stars": result})


# 用户添加搜藏
@user_page.route("/add_star/<int:house_id>")
def add_star(house_id):
    # 判断是否有用户登录
    if session.get("username"):
        user_stars = User.query.with_entities(User.collect_id).filter(User.name == g.current_user).all()[0]
        if user_stars[0] is not None:
            user_stars_list = user_stars[0].split(",")
        else:
            user_stars_list = []
        print(user_stars_list)
        # 判断用户是否收藏过该房源, 否则添加至数据库
        if str(house_id) in user_stars_list:
            return jsonify({"code": 0, "error": "已经收藏过该房源了"})
        else:
            query = db.session.query(User).filter(User.name == g.current_user)
            # 新的用户收藏列表
            new_stars = user_stars[0] + ',' + str(house_id)
            # print(new_stars)
            query.update({"collect_id": new_stars})
            db.session.commit()
            return jsonify({"code": 1, "info": "收藏成功"})
    else:
        return jsonify({"code": 0, "error": "需要先登录"})


@user_page.route("/views")
def views():
    user_views = User.query.with_entities(User.seen_id).filter(User.name == g.current_user).all()[0]
    if user_views[0] is not None:
        user_views = user_views[0].split(",")
    else:
        user_views = []

    # print(collections)
    result = []

    if len(user_views) == 0:
        return jsonify({"code": 0, "stars": []})
    else:
        collections = House.query.filter(House.id.in_(user_views)).all()
        for i in collections:
            result.append({
                "id": i.id,
                "title": i.title,
                "rooms": i.rooms,
                "area": i.area,
                "price": i.price,
                "direction": i.direction,
                "address": i.address,
                "traffic": i.traffic,
                "page_views": i.page_views
            })
        return jsonify({"code": 1, "views": result})
