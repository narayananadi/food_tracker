from .extensions import db


class Log(db.Model):
    lid = db.Column(db.String(50), primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False)
    fid = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.String(50), nullable=False)


class Food(db.Model):
    fid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.String(50), nullable=False)

    @property
    def calories(self):
        return self.proteins * 4 + self.carbs * 4 + self.fats * 9


class UserData(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique = True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    height_unit = db.Column(db.String(50), nullable=False)
    weight_unit = db.Column(db.String(50), nullable=False)
    calories_limit = db.Column(db.Integer, nullable=False)
    carbs_limit = db.Column(db.Integer, nullable=False)
    proteins_limit = db.Column(db.Integer, nullable=False)
    fats_limit = db.Column(db.Integer, nullable=False)


