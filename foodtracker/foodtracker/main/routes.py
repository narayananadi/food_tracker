from flask import Blueprint, render_template, request, redirect, url_for, session, json
from flask_session import Session
import sqlite3
from foodtracker.models import Food, UserData, Log
from foodtracker.extensions import db            
import uuid
from datetime import datetime 
from cryptography.fernet import Fernet
from datetime import date
import os
from datetime import date, timedelta
from random import randint

key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)
main = Blueprint('main', __name__)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# def calculate_total(log_data, index):



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
    return render_template('index.html', user_details=user_details,food_data=food_data)

@main.route('/create_log', methods=['POST'])
def create_log():
    uid = session["name"]
    pub_date = request.form.get('date')
    fate_arr = pub_date.split("-")
    fate_arr = [int(x) for x in fate_arr]
    pub_date = date(fate_arr[0],fate_arr[1],fate_arr[2])
    total_fields = len(list(request.form.keys())) - 1
    total_fields = int(total_fields/2)
    new_record_list_dict = []
    entry = []
    for x in range(total_fields):
        lid = str(uuid.uuid4())
        new_record_list_dict.append({"fid":request.form[f"input_field_{x}"], "uid":uid, "count":request.form[f"count_field_{x}"], "pub_date":pub_date})
        entry.append(Log(lid = lid, pub_date = pub_date, uid = uid, fid = request.form[f"input_field_{x}"], count = request.form[f"count_field_{x}"]))

    
    db.session.bulk_save_objects(entry)
    db.session.commit()
    return redirect(url_for('main.index'))

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
    list_of_foods = []
    log_data = Log.query.filter_by(uid=uid).all()
    for x in log_data:
        list_of_foods.append(x.fid)

    today = date.today()
    food_data = Food.query.filter(Food.uid.like(uid),Food.fid.in_(list_of_foods)).all()
    start_date = os.environ['START_DATE']
    start_date = start_date.split("-")
    start_date = [int(x) for x in start_date]
    start_date = date(start_date[0],start_date[1],start_date[2])
    end_date = today
    log_date_list = []
    for data in log_data:
        log_date_list.append(str(data.pub_date))
    
    date_wise_data = {
    "proteins":{"date":[], "value":[]},
    "fats":{"date":[], "value":[]},
    "calories":{"date":[], "value":[]},
    "carbs":{"date":[], "value":[]}
    }

    for single_date in daterange(start_date, end_date):
        single_date = str(single_date)
        print(len(single_date), type(single_date))
        print(len(log_date_list[0]), type(log_date_list[0]))
        if single_date in log_date_list:
            index = log_date_list.index(single_date)
            # proteins, carbs, fats, calories = calculate_total(log_data, index)
            proteins = randint(10,50)
            fats = randint(10,50)
            calories = randint(10,50)
            carbs = randint(10,50)
            date_wise_data["proteins"]["date"].append(str(log_data[index].pub_date))
            date_wise_data["proteins"]["value"].append(proteins)
            date_wise_data["fats"]["date"].append(str(log_data[index].pub_date))
            date_wise_data["fats"]["value"].append(fats)
            date_wise_data["carbs"]["date"].append(str(log_data[index].pub_date))
            date_wise_data["carbs"]["value"].append(carbs)
            date_wise_data["calories"]["date"].append(str(log_data[index].pub_date))
            date_wise_data["calories"]["value"].append(calories)
            # date_wise_data[log_data[index].pub_date] = {"proteins":100, "carbs":100, "fats":100, "calories":300}
        else:
            proteins = randint(10,50)
            fats = randint(10,50)
            calories = randint(10,50)
            carbs = randint(10,50)
            date_wise_data["proteins"]["date"].append(single_date)
            date_wise_data["proteins"]["value"].append(proteins)
            date_wise_data["fats"]["date"].append(single_date)
            date_wise_data["fats"]["value"].append(fats)
            date_wise_data["carbs"]["date"].append(single_date)
            date_wise_data["carbs"]["value"].append(carbs)
            date_wise_data["calories"]["date"].append(single_date)
            date_wise_data["calories"]["value"].append(calories)

    date_wise_data = json.dumps(date_wise_data)

    return render_template('dashboard.html', user_details=user_details, food_data = food_data, log_data = log_data,  today = today, date_wise_data=date_wise_data)

@main.route('/create', methods=['GET', 'POST'])
def create():
    if "name" not in session.keys():
        return redirect(url_for('main.login'))

    uid = session["name"]
    usr_dat = db.session.execute(UserData.query.filter_by(id=uid)).first()

    user_details = {"name":usr_dat[1]}
    foods = Food.query.filter_by(uid=uid).all()    
    return render_template('create_log.html',user_details=user_details,foods=foods)

@main.route('/land', methods=['GET', 'POST'])
def land():
        return render_template('land.html')