from cgitb import text
from datetime import date, timedelta
import datetime
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Calf, Cow, Expense, Milkstall, Pregnant, Salemilk, Staff, Supplier, User,bcrypt
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func
@app.route("/dashboard")
def dashoard():
    staff = db.session.query(Staff).filter(Staff.user_id==current_user.id).count()
    cow = db.session.query(Cow).filter(Cow.user_id == current_user.id).count()
    calf = db.session.query(Calf).filter(Calf.user_id == current_user.id).count()
    print(date.today())
    total_cow_stall = cow + calf
    supplier = db.session.query(Supplier).filter(Supplier.user_id == current_user.id).count()
    total_sale = db.session.query(func.sum(Salemilk.total)).filter(Salemilk.user_id == current_user.id).scalar()
    total_milk = db.session.query(func.sum(Milkstall.totalmilk)).filter(Milkstall.user_id == current_user.id).scalar()
    total_expense = db.session.query(func.sum(Expense.total_amount)).filter(Expense.user_id == current_user.id).scalar()
    milk = db.session.query(func.sum(Milkstall.totalmilk)).filter(Milkstall.date ==date.today(), Milkstall.user_id == current_user.id).scalar()
    expense = db.session.query(func.sum(Expense.total_amount)).filter(Expense.date == date.today(), Expense.user_id == current_user.id).scalar()
    sale_milk_amount = db.session.query(func.sum(Salemilk.lite)).filter(Salemilk.date == date.today(), Salemilk.user_id == current_user.id).scalar()
    sale_milk = db.session.query(func.sum(Salemilk.total)).filter(Salemilk.date == date.today(), Salemilk.user_id == current_user.id).scalar()
    data = Expense.query.filter(Expense.user_id == current_user.id).all()
    chart =[]
    dates = []
    for i in data:
        chart.append(int(i.total_amount))
        dates.append(i.date)    
    dat = date.today()
    dat1 = timedelta(7)
    
    da = dat - dat1
    data1 = Milkstall.query.filter(Milkstall.date <= dat, Milkstall.date >= da,Milkstall.user_id == current_user.id).all()
    charts =[]
    dates1 = []
    for i in data1:
        charts.append(int(i.totalmilk))
        dates1.append(i.date)
    print(dates1)
    print(dates1)
    chart3 =[]
    date3 = []
    data3 = Salemilk.query.filter(Salemilk.user_id == current_user.id).all()
    for i in data3:
        chart3.append(int(i.total))
        date3.append(i.date)
    pre = Pregnant.query.filter(Pregnant.user_id == current_user.id)
    mount = 0
    for i in pre:
        data1 = i.delivery_date 
        text1 = data1.strftime("%Y, %m, %d")
        d1 = text1.split(",")
        data2 = datetime.datetime.now()
        text2 = data2.strftime("%Y, %m, %d")
        d2 = text2.split(",")
        wid = date((int(d1[0])), (int(d1[1])), (int(d1[2]))) - date((int(d2[0])), (int(d2[1])), (int(d2[2])))
        wid1 = wid.days
        if wid1 <=5 and wid1 >-1:
            mount += 1
            print("The mount of pregnment",mount)
        else:
            print("No have pregnment!!!!")
            
        dat = date.today()
        dat1 = timedelta(7)
    
        da = dat - dat1
        user = User.query.get(current_user.id)
        print("data start : ",da)
        print("date finish : ", dat)
        ex =Expense.query.filter(Expense.date <= dat, Expense.date >= da ,Expense.user_id == user.id).all()
    
        print(ex)
        date4 = []
    
        for i in ex:
            t = i.date
            text1 = t.strftime("%Y-%m-%d")
            date4.append(text1)
    return render_template("index.html",ds = date4, ex = ex, mount = mount,
                           chart3 = chart3,pre = pre,d=date,dates = dates, date3 = date3,charts = charts,
                           dates1 = dates1,da = chart,sale_milk = sale_milk,sale_milk_amount= sale_milk_amount,
                           datetime = datetime,   total_sale =total_sale,total_cow_stall = total_cow_stall,
                           total_milk = total_milk, total_expense = total_expense, staff = staff, cow = cow,
                           calf = calf, milk = milk, expense = expense, supplier = supplier)



@app.route("/show_chartjs")
def show_chartjs():
    dat = date.today()
    dat1 = timedelta(7)
    
    da = dat - dat1
    user = User.query.get(current_user.id)
    print("data start : ",da)
    print("date finish : ", dat)
    ex =Expense.query.filter(Expense.date <= dat, Expense.date >= da ,Expense.user_id == user.id).all()
    
    print(ex)
    dates = []
    
    for i in ex:
        t = i.date
        text1 = t.strftime("%Y-%m-%d")
        dates.append(text1)
    print(dates)
    
    for i in dates:
        print(i)
    return render_template("/show_chartjs.html", d = dates, ex = ex)