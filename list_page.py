import math

from flask import Blueprint, render_template, request, redirect
from models import House

list_page = Blueprint("list_page", __name__)


@list_page.route("/query", methods=["GET", "POST"])
def search_result():
    if request.args.get("addr"):
        addr = request.args.get("addr")
        house_data = House.query.filter(House.address == addr).limit(10).all()
        return render_template("search_list.html", house_data=house_data)

    if request.args.get("rooms"):
        rooms = request.args.get("rooms")
        house_data = House.query.filter(House.rooms == rooms).limit(10).all()
        return render_template("search_list.html", house_data=house_data)
    return redirect("/")


@list_page.route("/list/pattern/<int:page>")
def return_new_list(page):
    house_num = House.query.count()  # 房源总数量
    total_page_num = math.ceil(house_num / 10)  # 总的页码数
    result = House.query.order_by(
        House.publish_time.desc()
    ).paginate(page, per_page=10)
    return render_template("list.html",
                           house_list=result.items,
                           page_num=result.page,
                           total_page_num=total_page_num)
