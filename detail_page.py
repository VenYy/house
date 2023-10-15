import math

from flask import Blueprint, render_template, request
from models import House
from sqlalchemy import func, desc
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

detail_page = Blueprint("detail_page", __name__)


@detail_page.route("/house/<int:hid>", methods=["GET", "POST"])
def detail(hid):
    house = House.query.get(hid)
    if house:
        facilities_str = house.facilities
        facilities_list = facilities_str.split("-")
    else:
        facilities_list = []
    if request.method == "GET":
        return render_template("detail_page.html", house=house, facilities=facilities_list)
    if request.method == "POST":
        return facilities_list


# 户型占比可视化
@detail_page.route("/chart/rooms/<block>")
def chart_rooms(block):
    rooms_data = House.query.with_entities(
        House.rooms, func.count(House.rooms).label("rooms_count")
    ).filter(House.block == block).group_by(House.rooms).order_by(desc("rooms_count")).limit(20).all()

    rooms_pie = Pie()
    rooms_pie.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{block} 户型占比",
            subtitle="根据户型占比, 了解户型稀缺度",
            pos_left="center",
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )
    rooms_pie.add("", rooms_data,
                  radius="60%",
                  center=["50%", "60%"])
    return rooms_pie.dump_options_with_quotes()


# 小区房源数量Top20
@detail_page.route("/chart/column/<block>")
def chart_column(block):
    address_data = House.query.with_entities(
        House.address, func.count(House.address).label("address_count")
    ).filter(House.block == block).group_by(House.address).order_by(desc("address_count")).limit(20).all()
    address_data_result = []
    # 处理小区名称 [('东城-东单-东方豪庭', 172), ...]
    for elem in address_data:
        if len(elem[0].split("-")) == 2:
            address_data_result.append((elem[0].split("-")[1], elem[1]))
        elif len(elem[0].split("-")) == 3:
            address_data_result.append((elem[0].split("-")[2], elem[1]))

    address_bar = Bar()
    address_bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{block} 小区房源数量",
            subtitle="关注房源数量, 了解房源热点",
            pos_left="center"
        ),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False)),
    )

    address_bar.add_xaxis([elem[0] for elem in address_data_result])
    address_bar.add_yaxis(y_axis=[elem[1] for elem in address_data_result],
                          series_name="房源数量(套)",
                          label_opts=opts.LabelOpts(
                              color="white",
                              font_weight="bold"
                          ),
                          bar_max_width="50px"
                          )
    return address_bar.dump_options_with_quotes()


# 过滤器
def deal_none(word):
    if word:
        # print(word)
        if len(word) == 0 or word is None or word == "None":
            return "暂无信息"
        else:
            return word
    else:
        return "暂无信息"


detail_page.add_app_template_filter(deal_none, "deal_none")
