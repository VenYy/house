from settings import db


class House(db.Model):
    __tablename__ = 'house_info'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, comment='房源标题')
    rooms = db.Column(db.String(20), nullable=False, comment='房源户型')
    area = db.Column(db.String(20), nullable=False, comment='房源面积')
    price = db.Column(db.String(20), nullable=False, comment='房源价格')
    direction = db.Column(db.String(10), nullable=False, comment='朝向')
    rent_type = db.Column(db.String(20), nullable=False, comment='租住类型')
    region = db.Column(db.String(20), nullable=False, comment='房源所在区')
    block = db.Column(db.String(30), nullable=False, comment='所在街道')
    address = db.Column(db.String(20), nullable=False, comment='所在小区')
    traffic = db.Column(db.Text, nullable=False, comment='交通条件')
    publish_time = db.Column(db.DateTime, nullable=False, comment='发布时间')
    facilities = db.Column(db.Text, nullable=False, comment='配套设施')
    highlights = db.Column(db.Text, nullable=False, comment='房屋优势')
    matching = db.Column(db.Text, nullable=False, comment='周边')
    travel = db.Column(db.Text, nullable=False, comment='公交出行')
    page_views = db.Column(db.Integer, nullable=False, comment='浏览量')
    landlord = db.Column(db.String(10), nullable=False, comment='房东姓名')
    phone_num = db.Column(db.String(11), nullable=False, comment='房东电话')
    house_num = db.Column(db.String(10), nullable=False, comment='房源编号')


class Recommend(db.Model):
    __tablename__ = 'house_recommend'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    house_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(20), nullable=True)
    block = db.Column(db.String(30), nullable=True)
    score = db.Column(db.Integer, nullable=True, comment='浏览次数')


class User(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, comment='用户昵称')
    password = db.Column(db.String(10), nullable=False, comment='用户密码')
    email = db.Column(db.String(20), nullable=True)
    addr = db.Column(db.String(50), nullable=False, comment='住址')
    collect_id = db.Column(db.String(100), nullable=True, comment='用户收藏的房源编号')
    seen_id = db.Column(db.String(100), nullable=True, comment='用户浏览记录')
