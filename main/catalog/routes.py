from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Cow, Employeesalary, Expense,  FoodItem, Foodunit, Pregnant, Staff, Stall, User, Vaccinetype,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time
from sqlalchemy import true,func,or_
@app.route("/catalog")
def catalog():
    user = User.query.get(current_user.id)
    animaltype = Animaltype.query.filter(Animaltype.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    total_cow = db.session.query(func.sum(Stall.total_cow)).scalar()
    stall_cow = db.session.query(Cow)
    vatype = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    foodunit = Foodunit.query.filter(Foodunit.user_id == user.id)
    foodItem = FoodItem.query.filter(FoodItem.user_id == user.id)
    return render_template("/catalog/catalog.html",foodItem = foodItem,foodunit = foodunit,vatype = vatype, total_cow = total_cow, stall_cow = stall_cow, animaltype = animaltype, stall = stall,Cow = Cow,Stall = Stall)

@app.route("/add_animaltype", methods=["POST", "GET"])
def add_animaltype():
    if request.method == "POST":
        type_name = request.form["type_name"]
        antype =Animaltype(type_name = type_name, user_id = current_user.id)
        db.session.add(antype)
        db.session.commit()
        return redirect(request.referrer)
    
@app.route("/add_stall", methods=["POST", "GET"])
def add_stall():
    if request.method == "POST":
        stall_number = request.form["stall_number"]
        total_cow = request.form['total_cow']
        status = request.form["status"]
        detail=request.form["detail"]
        sta = Stall(stall_number = stall_number,total_cow = total_cow , status = status, detail = detail, user_id = current_user.id)
        db.session.add(sta)
        db.session.commit()
        return redirect(request.referrer)
        
        
@app.route("/edit_stall:<int:id>", methods=["POST", "GET"])
def edit_stall(id):
    user = User.query.get(current_user.id)
    data = Stall.query.filter(Stall.user_id == user.id)
    data = data.filter_by(id = id ).first()

    if request.method == "POST":
        data.stall_number = request.form["stall_number"]
        data.status = request.form["status"]
        data.detail = request.form["detail"]
        db.session.commit()
        return redirect(request.referrer) 
@app.route("/delete_stall:<int:id>")
def delete_stall(id):
    user = User.query.get(current_user.id)
    data = Stall.query.filter(Stall.user_id == user.id)
    data = data.filter_by(id = id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)      

@app.route("/add_vaccinetype", methods=["POST", "GET"])
def add_vaccinetype():
     if request.method == "POST":
        vaccine_name = request.form["vaccine_name"]
        period_day	 = request.form["period_day"]
        repeat_vaccine = request.form["repeat_vaccine"]
        dose = request.form["dose"]
        note = request.form["note"]
        vac = Vaccinetype(vaccine_name = vaccine_name, period_day= period_day,
        repeat_vaccine = repeat_vaccine, dose = dose, note  = note, user_id = current_user.id)
        db.session.add(vac)
        db.session.commit()
        return redirect(request.referrer)
    
@app.route("/catalog/delete_vaccine_type:<int:id>")
def delete_vaccine_type(id):
    user  = User.query.get(current_user.id)
    vacc = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    data = vacc.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/catalog/add_food_unit", methods=["POST", "GET"])
def add_food_unit():
    if request.method == "POST":
        unit_name = request.form["unit_name"]
        fo = Foodunit(unit_name=unit_name, user_id = current_user.id)
        db.session.add(fo)
        db.session.commit()
        return redirect(request.referrer)
@app.route("/catalog/delete_food_unit:<int:id>")
def delete_foodunit(id):
    user = User.query.get(current_user.id)
    food = Foodunit.query.filter(Foodunit.user_id == user.id)
    data = food.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("catalog"))

@app.route("/catalog/add_food_item", methods=["POST", "GET"])
def add_foodItem():
    if request.method == "POST":
        item_name = request.form["item_name"]
        fo = FoodItem(item_name=item_name, user_id = current_user.id)
        db.session.add(fo)
        db.session.commit()
        return redirect(url_for("catalog"))
    

@app.route("/catalog/delete_food_item:<int:id>")
def delete_foodItem(id):
    user = User.query.get(current_user.id)
    food = FoodItem.query.filter(FoodItem.user_id == user.id)
    data = food.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("catalog"))