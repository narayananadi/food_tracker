from foodtracker.models import Log, UserData, Food
from foodtracker.extensions import db
from foodtracker import create_app
db.drop_all(app=create_app())
db.create_all(app=create_app())
print("updated")