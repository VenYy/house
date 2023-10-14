import math

from flask import Blueprint, render_template, request, redirect, url_for
from models import House

list_page = Blueprint("list_page", __name__)


@list_page.route("/query/", methods=["GET", "POST"])
def search_result():
    # if request.args.get("addr"):
    #     addr = request.args.get("addr")
    #     house_data = House.query.filter(House.address == addr).limit(10).all()
    #     return render_template("search_list.html", house_data=house_data)
    if request.args.get("addr"):
        addr = request.args.get("addr")
        house_data = House.query.filter(House.address == addr)
        house_num = house_data.count()
        total_page_num = math.ceil(house_num / 10)
        current_page = request.args.get("page", 1, type=int)
        pagination = house_data.paginate(page=current_page, per_page=10)
        return render_template("search_list.html",
                               pagination=pagination,
                               house_list=pagination.items,
                               page_num=pagination.page,
                               total_page_num=total_page_num)

    if request.args.get("rooms"):
        rooms = request.args.get("rooms")
        house_data = House.query.filter(House.rooms == rooms)
        house_num = house_data.count()
        total_page_num = math.ceil(house_num / 10)
        current_page = request.args.get("page", 1, type=int)
        pagination = house_data.paginate(page=current_page, per_page=10)
        return render_template("search_list.html",
                               pagination=pagination,
                               house_list=pagination.items,
                               page_num=pagination.page,
                               total_page_num=total_page_num)
    return redirect("/")


@list_page.route("/list/pattern/")
def return_new_list():
    house_num = House.query.count()  # 房源总数量
    total_page_num = math.ceil(house_num / 10)  # 总的页码数
    current_page = request.args.get("page", 1, type=int)
    pagination = House.query.order_by(
        House.publish_time.desc()
    ).paginate(page=current_page, per_page=10)

    return render_template("new_list.html",
                           pagination=pagination,
                           house_list=pagination.items,
                           page_num=pagination.page,
                           total_page_num=total_page_num)


@list_page.route("/list/hot/")
def return_hot_list():
    house_num = House.query.count()  # 房源总数量
    total_page_num = math.ceil(house_num / 10)  # 总的页码数
    current_page = request.args.get("page", 1, type=int)
    pagination = House.query.order_by(
        House.page_views.desc()
    ).paginate(page=current_page, per_page=10)

    return render_template("hot_list.html",
                           pagination=pagination,
                           house_list=pagination.items,
                           page_num=pagination.page,
                           total_page_num=total_page_num)
