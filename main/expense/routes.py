
from msilib import datasizemask
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Cow, Employeesalary, Expense, Pregnant, Staff, Stall, User,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time



@app.route("/expense", methods=["POST", "GET"])
def expense():
    user = User.query.get(current_user.id)
    exp = Expense.query.filter(Expense.user_id == user.id)
    page = request.args.get('page', 1, type=int)
    if request.method == "POST":
        search = request.form['search']
        
        if search == "":
            data = exp.paginate(page = page, per_page = 25)
        else:
            exps = exp.filter(Expense.date.like("%"+search+"%") | Expense.purposes.like("%"+search+"%")).order_by(Expense.id.desc())
            data = exps.paginate(page = page, per_page = 50)
    else:
        data = exp.paginate(page = page, per_page = 25)
    return render_template("/expense/expense.html", data = data)


@app.route("/edit_expense:<int:id>", methods=["POST", "GET"])
def edit_expense(id):
    user  = User.query.get(current_user.id)
    datas = Expense.query.filter(Expense.user_id == user.id)
    data = datas.filter_by(id = id).first()
    if request.method == "POST":
        data.date = request.form["date"]
        data.purposes = request.form["purpose_name"]
        data.detail = request.form["detail"]
        data.total_amount = request.form["total_amount"]
        db.session.commit()
    return redirect(request.referrer)

@app.route("/add_expense",methods=["POST", "GET"])
def add_expense():
    if request.method == "POST":
        dates = request.form["date"]
        purepose_name = request.form["purpose_name"]
        detail = request.form["detail"]
        total_amount = request.form["total_amount"]
        month_today = date.today()
        month_today = month_today.strftime("%m")
        ex = Expense(date = dates, month= month_today, purposes= purepose_name, detail = detail, total_amount = total_amount, user_id=current_user.id)
        db.session.add(ex)
        db.session.commit()
        return redirect(request.referrer) 
    else:
        return redirect(request.referrer) 
    
    
@app.route("/delete_expense<int:id>")
def delete_expense(id):
    user = User.query.get(current_user.id)
    data = Expense.query.filter(Expense.user_id == user.id)
    data = data.filter_by(id= id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("expense"))
