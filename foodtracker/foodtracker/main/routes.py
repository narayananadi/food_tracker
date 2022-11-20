from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_session import Session
import sqlite3
from foodtracker.models import Food, UserData, Log
from foodtracker.extensions import db            
import uuid
from datetime import datetime 
from cryptography.fernet import Fernet


key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)
main = Blueprint('main', __name__)

@main.route('/')
def index():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))
    login_dict={}
    login_dict['isLogged']=True
    uid = session["name"]
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()
    user_details = {"email":usr_dat[3], 
     "name":usr_dat[1], 
     "height":usr_dat[4],
     "weight":usr_dat[5], 
     "calories":usr_dat[8],
     "carbs":usr_dat[9], 
     "proteins":usr_dat[10],
     "fats": usr_dat[11]

    }
    food_data = Food.query.filter_by(uid=uid).all()
    food_dict = {}
    for food in food_data:
        food_dict[food.fid] = {"name":food.name, "carbs":food.carbs, "proteins":food.proteins, "fats":food.fats, "calories":food.calories}
        

    logs = Log.query.filter_by(uid=uid).all()
    dict_food = {}
    dict_date = {}
    for log in logs:
        if log.pub_date not in dict_date.keys():
            dict_date[log.pub_date] = []
        food = Food.query.filter_by(fid=log.fid).first()
        dict_food[log.fid] = {"name":food.name, "carbs":food.carbs, "proteins":food.proteins, "fats":food.fats, "calories":food.calories}
        dict_date[log.pub_date].append({"name":food.name, "carbs":food.carbs, "proteins":food.proteins, "fats":food.fats, "calories":food.calories})


    return render_template('index.html', food_dict=food_dict, user_details=user_details,food_data=food_data)

@main.route('/create_log', methods=['POST'])
def create_log():
    uid = session["name"]
    date = request.form.get('date')

    food_data = Food.query.filter_by(id=uid).all()
    food_dict = {}
    for food in food_data:
        food_dict[food_data.fid] = {"name":food_data.name, "carbs":food_data.carbs, "proteins":food_data.proteins, "fats":food_data.fats, "calories":food_data.calories}
        

    return redirect(url_for('main.view'))

@main.route('/add',methods=['GET', 'POST'])
def add():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))

    uid = session["name"]
    record = None
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()
    print(usr_dat)
    user_details = {"name":usr_dat[1] }
    if request.method == 'POST':
        food_name = request.form.get('food-name')
        proteins = request.form.get('protein')
        carbs = request.form.get('carbohydrates')
        fats = request.form.get('fat')
        food_id = str(uuid.uuid4())

        if_food = Food.query.filter_by(name=food_name).first()
        if not if_food:
            new_food = Food(name = food_name, proteins = proteins, carbs = carbs, fats = fats, fid = food_id, uid = uid)
            db.session.add(new_food)
            db.session.commit()   
            return redirect(url_for('main.add'))
        else:
            Food.query.filter_by(name=food_name).update(dict(name = food_name, proteins = proteins, carbs = carbs, fats = fats, fid = food_id, uid = uid))

    foods = Food.query.filter_by(uid=uid).all()
    return render_template('add.html', foods=foods, user_details=user_details)


@main.route('/delete_food/<food_id>')
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for('main.add'))

@main.route('/view/<log_id>')
def view(log_id):
    log = Log.query.get_or_404(log_id)

    foods = Food.query.all()

    totals = {
        'protein' : 0,
        'carbs' : 0,
        'fat' : 0,
        'calories' : 0
    }

    for food in log.foods:
        totals['protein'] += food.proteins
        totals['carbs'] += food.carbs
        totals['fat'] += food.fats 
        totals['calories'] += food.calories

    return render_template('view.html', foods=foods, log=log, totals=totals)

@main.route('/add_food_to_log/<int:log_id>', methods=['POST'])
def add_food_to_log(log_id):
    log = Log.query.get_or_404(log_id)

    selected_food = request.form.get('food-select')

    food = Food.query.get(int(selected_food))

    log.foods.append(food)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))

@main.route('/remove_food_from_log/<int:log_id>/<int:food_id>')
def remove_food_from_log(log_id, food_id):
    log = Log.query.get(log_id)
    food = Food.query.get(food_id)

    log.foods.remove(food)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))


@main.route('/login', methods=['GET', 'POST'])
def login():
    error_dict = {"email_exists":False,"wrong_pass":False,"login_err":False}
    if request.method == 'POST':
        req_email = request.form['email']
        if_email = db.session.execute(UserData.query.filter_by(email=req_email)).first()
        if not if_email:
            print("email doesn't exist")
            error_dict = {"email_exists":False,"wrong_pass":False,"login_err":True}
            return render_template('login.html', error_dict=error_dict)
        actual_pass = if_email[2]
        unciphered_pass = (cipher_suite.decrypt(actual_pass))
        req_password = request.form['password'] 
        req_password = bytes(req_password, encoding='utf8')
        if req_password != unciphered_pass:
            print("invalid password")
            error_dict = {"email_exists":False,"wrong_pass":True,"login_err":False}
            return render_template('login.html', error_dict=error_dict)
        session["name"] = if_email[0]
        
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', error_dict=error_dict)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    error_dict = {"email_exists":False,"wrong_pass":False,"login_err":False}
    if request.method == 'POST':
        req_id = str(uuid.uuid4())
        req_email = request.form['email'] 
        is_email = db.session.execute(UserData.query.filter_by(email=req_email)).first()
        if is_email:
            error_dict = {"email_exists":True,"wrong_pass":False,"login_err":False}
            print("email already exists")
            return render_template('login.html' , error_dict=error_dict)

        req_username = request.form['username']
        req_password = request.form['password']

       
        ciphered_pass = cipher_suite.encrypt(bytes(req_password, encoding='utf8'))
        print(ciphered_pass) 
        req_password = ciphered_pass
        req_weight = 0
        req_height = 0
        req_weight_unit = "KGS"
        req_height_unit = "CMS"
        calories_limit = 0
        carbs_limit = 0
        proteins_limit = 0
        fats_limit = 0

        entry = UserData(id = req_id, 
        email = req_email, 
        username = req_username, 
        password = req_password, 
        weight = req_weight,
        height = req_height,
        weight_unit = req_weight_unit,
        height_unit = req_height_unit,
        calories_limit=calories_limit,
        carbs_limit=carbs_limit,
        proteins_limit=proteins_limit,
        fats_limit = fats_limit
        )


        db.session.add(entry)
        db.session.commit()
        session["name"] = req_id

        return redirect(url_for('main.dashboard'))

    return render_template('login.html', error_dict=error_dict)



@main.route('/forgot', methods=['GET', 'POST'])
def forgot():
    error_dict = {"email_exists":False}
    if request.method == 'POST':
        req_email = request.form['email']
        req_new_password = request.form['n_password']
        if_email = db.session.execute(UserData.query.filter_by(email=req_email)).first()
        if not if_email:
            print("email doesnot exist")
            error_dict = {"email_exists":True}
            return render_template('forgot.html', error_dict=error_dict)

        ciphered_pass = cipher_suite.encrypt(bytes(req_new_password, encoding='utf8'))
        UserData.query.filter_by(email=req_email).update(dict(password=ciphered_pass))
        db.session.commit()
        return render_template('login.html', error_dict=error_dict)
    return render_template('forgot.html', error_dict=error_dict)


@main.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))

    uid = session["name"]
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()
    print(usr_dat)
    user_details = {"email":usr_dat[3], 
     "name":usr_dat[1], 
     "height":usr_dat[4],
     "weight":usr_dat[5], 
     "calories":usr_dat[8],
     "carbs":usr_dat[9], 
     "proteins":usr_dat[10],
     "fats": usr_dat[11]
    }
    if request.method == 'POST':
        update_dict = {}
        for keys in request.form.keys():
            if request.form[keys] != "":
                update_dict[keys] = request.form[keys]
        if update_dict:
            UserData.query.filter_by(id=uid).update(update_dict)        
            db.session.commit()
        return redirect(url_for('main.user_profile'))
    return render_template('profile.html', user_details=user_details)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main.login'))



@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))

    uid = session["name"]
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()

    user_details = {"email":usr_dat[3], 
     "name":usr_dat[1], 
     "height":usr_dat[4],
     "weight":usr_dat[5], 
     "calories":usr_dat[8],
     "carbs":usr_dat[9], 
     "proteins":usr_dat[10],
     "fats": usr_dat[11]
    }

    return render_template('dashboard.html', user_details=user_details)

@main.route('/create', methods=['GET', 'POST'])
def create():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))

    uid = session["name"]
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()

    user_details = {"name":usr_dat[1]}
    foods = Food.query.filter_by(uid=uid).all()    
    return render_template('create_log.html',user_details=user_details,foods=foods)