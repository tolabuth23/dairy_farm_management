from imghdr import tests
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify,make_response
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Calf, Cow, Employeesalary, Expense, Getvaccince, Milkstall,  Pregnant, Salemilk, Staff, Stall, Treatment, User, Vaccinetype,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time
import pdfkit
from sqlalchemy import func


@app.route("/treatment", methods=["POST", "GET"])
def treatment():
    user = User.query.get(current_user.id)
    page = request.args.get('page', 1, type=int)
    stall = Stall.query.filter(Stall.user_id == user.id)
    if request.method == "POST":
        treats = Treatment.query.filter(Treatment.user_id == user.id)
        search = request.form["search"]
        if search =="":
            treat = Treatment.query.filter(Treatment.user_id == user.id)
            treat = treat.paginate(page = page, per_page = 25)
        else: 
            stalls = Stall.query.filter_by(stall_number = search).first()
            cows = Cow.query.filter_by(cow_no = search).first()
            if stalls:
                stall_id = int(stalls.id)
                print("stall id", stall_id)
                treat = treats.filter(Treatment.stall_no.like(2)).order_by(Treatment.id.desc())
                
                treat = treat.paginate(page = page, per_page = 50)
                print(treat.items)
            
            
            elif cows:
                cow_id = int(cows.id)
                print("Cow ID", cow_id)
                treat = treats.filter(Treatment.cow_no.like(cow_id)).order_by(Treatment.id.desc())
                treat = treat.paginate(page = page, per_page = 50)
            else:
                treat = treats.filter(Treatment.date.like("%"+search+"%")).order_by(Treatment.id.desc())
                treat = treat.paginate(page = page, per_page = 50)
    else:
        stall = Stall.query.filter(Stall.user_id == user.id)
        treat = Treatment.query.filter(Treatment.user_id == user.id)
        treat = treat.paginate(page = page, per_page = 25)
    
    return render_template("treatment/treatment.html", stall = stall, data = treat)

@app.route("/add_treatment", methods=["POST", "GET"])
def add_treatment():
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        cow_no = request.form["cow_id"]
        medicine = request.form["medicine"]
        spend = request.form["spend"]
        symptom = request.form["symptom"]
        tr = Treatment(stall_no = stall_no, cow_no = cow_no, medicine = medicine, symptom = symptom, spend = spend, user_id = current_user.id)
        db.session.add(tr)
        db.session.commit()
        return redirect(url_for('treatment'))
    

@app.route("/edit_treatment<int:id>", methods=["POST", "GET"])
def edit_treatment(id):
    user = User.query.get(current_user.id)
   
    treat = Treatment.query.filter(Treatment.user_id == user.id)
    tr = treat.filter_by(id = id).first()
    if request.method == "POST":
        tr.medicine = request.form["medicine"]
        tr.spend = request.form["spend"]
        tr.symptom = request.form["symptom"]
        db.session.commit()
        return redirect(url_for('treatment'))
@app.route("/delete_treatment:<int:id>")
def delete_treatment(id):
    user = User.query.get(current_user.id)
    treat = Treatment.query.filter(Treatment.user_id == user.id)
    tr = treat.filter_by(id = id).first()
    db.session.delete(tr)
    db.session.commit()
    return redirect(url_for('treatment'))
        
@app.route("/get_cow_treatment", methods=["POST", "GET"])
def get_cow_treatment():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(id = parent_id).first()
        
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/treatment/response.html', datas = datas)})