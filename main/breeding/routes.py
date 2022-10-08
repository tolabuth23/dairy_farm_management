from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Cow, Employeesalary, Pregnant, Staff, Stall, User,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time

@app.route("/breeding")
def breeding():
    user = User.query.get(current_user.id)
    pre = Pregnant.query.filter(Pregnant.user_id == user.id).order_by(Pregnant.id.desc())
    page = request.args.get('page', 1, type=int)
    data = pre.paginate(page = page, per_page = 5)
    return render_template("/breeding/breeding.html",data =data,dat = timedelta(280), dates = datetime, d =date, datetime = datetime)
@app.route("/add_breeding", methods=["POST", "GET"])
def add_breeding():
    user = User.query.get(current_user.id)
    stalls = Stall.query.filter(Stall.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    antype = Animaltype.query.filter(Animaltype.user_id == user.id)
    if request.method =="POST":
        stall_id = request.form['stall_id']
        cow_id = request.form['cow_id']
        pregnancy_type = request.form["pregnancy_type"]
        semen_type = request.form["semen_type"]
        semen_push_date = request.form["semen_push_date"]
        semen_cost = request.form['semen_cost']
        pregnancy_status = request.form["pregnancy_status"]
        cows = Cow.query.filter_by(id = cow_id, stall_id=stall_id).first()
        print(cows.cow_no)
        cows.pregnant_status = "Pregnant"
        db.session.commit()
        note = request.form["note"]
        pre = Pregnant(stall_id=stall_id, cow_id = cow_id,pregnancy_type = pregnancy_type, semen_type=semen_type, 
                           semen_push_date=semen_push_date,
                       semen_cost=semen_cost, pregnancy_status=pregnancy_status, note=note, user_id = current_user.id)
        db.session.add(pre)
        db.session.commit()
        return redirect(url_for("breeding"))
    return render_template("/breeding/add_breeding.html",stall = stalls, cow = cows, antype = antype)


@app.route("/get_cow_breeding", methods=["POST", "GET"])
def get_cow_breeding():
     user = User.query.get(current_user.id)
     if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        datas = Cow.query.filter_by(id = parent_id).first()
     return jsonify({'htmlresponse': render_template('/breeding/breeding_response.html', data = datas)})
 
 
@app.route("/edit_breeding:<int:id>", methods=["POST", "GET"])
def edit_breeding(id):
    user = User.query.get(current_user.id)
    preg = Pregnant.query.filter(Pregnant.user_id == user.id)
    data = preg.filter_by(id = id).first()
    if request.method == "POST":
        psd = request.form["pregnancy_start_date"]
        pstatus = request.form["pregnancy_status"]
        cow = Cow.query.filter_by(id=data.cow_id, stall_id=data.stall_id).first()
        if pstatus == "Failed":
            cow.pregnant_status ="No Pregnant"
            db.session.commit()
        dat = timedelta(280)
        print(data.pregnancy_start_date + dat)
        data.pregnancy_start_date = psd 
        data.pregnancy_status = pstatus
        print(psd)
        db.session.commit()
        data.delivery_date = data.pregnancy_start_date +dat
        db.session.commit()
    return redirect(url_for("breeding"))

@app.route("/delete_breeding:<int:id>")
def delete_breeding(id):
    user = User.query.get(current_user.id)
    breeding = Pregnant.query.filter(Pregnant.user_id == user.id)
    get = breeding.filter_by(id = id).first()
    db.session.delete(get)
    db.session.commit()
    return redirect(url_for("breeding"))