from flask import Blueprint, render_template
from models import House

detail_page = Blueprint("detail_page", __name__)


@detail_page.route("/house/<int:hid>")
def detail(hid):
    house = House.query.get(hid)
    if house:
        facilities_str = house.facilities
        facilities_list = facilities_str.split("-")
    else:
        facilities_list = []
    return render_template("detail_page.html", house=house, facilities=facilities_list)
