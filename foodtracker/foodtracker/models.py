from .extensions import db

log_food = db.Table('log_food',
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)

    @property
    def calories(self):
        return self.proteins * 4 + self.carbs * 4 + self.fats * 9

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    foods = db.relationship('Food', secondary=log_food, lazy='dynamic')


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


