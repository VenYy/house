from flask import Blueprint, render_template, request, redirect, url_for

user_page = Blueprint("user_page", __name__)


def check_login():
    user_cookie = request.cookies.get("user")
    if user_cookie:
        current_user = user_cookie.split("=")[0]
    else:
        current_user = None
    return current_user


#
#
@user_page.route("/user")
def user_home():
    current_user = check_login()
    print(current_user)
    if current_user:
        return render_template("user_page.html", username=current_user)
    else:
        return redirect(url_for("user_page.login"))


@user_page.route("/login")
def login():
    return render_template("login.html")


@user_page.route("/register")
def register():
    return render_template("register.html")
