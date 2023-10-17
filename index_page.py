from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import House
from sqlalchemy import func

# 创建蓝图
index_page = Blueprint("index_page", __name__)


@index_page.route("/", methods=["GET", "POST"])
def index():
    house_total_num = House.query.count()
    # 获取最新房源Top6
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()

    return render_template("index.html", num=house_total_num, house_new_list=house_new_list)


@index_page.route("/search/keyword/", methods=["POST"])
def search_kw():
    keyword = request.form.get("keyword")
    search_type = request.form.get("search_type")

    if search_type == "地区搜索":
        # 查询满足条件的数据和出现的次数
        house_data = House.query.with_entities(
            House.address, func.count()
        ).filter(House.address.contains(keyword))
        # 对查询结果排序并显示
        result = house_data.group_by("address").order_by(
            func.count().desc()
        ).limit(6).all()
        # [('大兴-亦庄-上海沙龙', 62), ('丰台-大红门-上海建筑', 8), ('丰台-大红门-海上海花园', 7), ('大兴-亦庄-旭东嘉园上海沙龙', 1)]
        if len(result) > 0:
            data = []
            for i in result:
                data.append({"name": i[0], "count": i[1]})
            return jsonify({"code": 1, "data": data})
        else:
            return jsonify({"code": 0, "data": []})

    if search_type == "户型搜索":
        house_data = House.query.with_entities(
            House.rooms, func.count()
        ).filter(House.rooms.contains(keyword))
        result = house_data.group_by("rooms").order_by(
            func.count().desc()
        ).limit(6).all()
        if len(result) > 0:
            data = []
            for i in result:
                data.append({"name": i[0], "count": i[1]})
            return jsonify({"code": 1, "data": data})
        else:
            return jsonify({"code": 0, "data": []})
