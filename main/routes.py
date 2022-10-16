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
    dat1 = timedelta(6)
    
    da = dat - dat1
    datas1 = Milkstall.query.filter(Milkstall.date <= dat, Milkstall.date >= da,Milkstall.user_id == current_user.id).all()
    charts =[]
    dates1 = []
    for i in datas1:
        #charts.append(int(i.totalmilk))
        t = i.date
        text1 = t.strftime("%Y-%m-%d")
        dates1.append(text1)
    print(dates1)
    print(dates1)
    
    dat = date.today()
    dat1 = timedelta(6)
    da = dat - dat1
    chart3 =[]
    date3 = []
    data3 = Salemilk.query.filter(Salemilk.date <= dat, Salemilk.date >= da, Salemilk.user_id == current_user.id).all()
    for i in data3:
        #chart3.append(int(i.total))
        #date3.append(i.date)
        t = i.date
        text3 = t.strftime("%Y-%m-%d")
        date3.append(text3)
    print("Amount of chart 3: ", date3)
    print("Amount of data: ", data3)
    
        
        
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
        dat1 = timedelta(6)
    
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
            #get data all 
        ex_all = Expense.query.filter(Expense.user_id == user.id).all()
        sale_all = Salemilk.query.filter(Salemilk.user_id == user.id).all()
        milk_all = Milkstall.query.filter(Milkstall.user_id == user.id).all()
        
        
    #kHow to find data for to get data expense
    date_today = date.today()
    determie_delta = timedelta(6)
    date_last = date_today - determie_delta
    get_data_expense = Expense.query.filter(Expense.user_id == user.id, 
                        Expense.date <= date_today, Expense.date >= date_last).all()
    data_expense = []
    for i in get_data_expense:
        t = i.date
        text1 =t.strftime("%Y-%m-%d")
        data_expense.append(text1)      
    data_exp = list(dict.fromkeys(data_expense))
    data_exp_price =[]
    for i in data_exp:
        price = db.session.query(func.sum(Expense.total_amount)).filter(Expense.user_id == user.id,
                                Expense.date == i).scalar()
        data_exp_price.append(price)
    #kHow to find data for to get data expense
    date_today = date.today()
    determie_delta = timedelta(6)
    date_last = date_today - determie_delta
    get_sale_milk = Salemilk.query.filter(Salemilk.user_id == user.id,
                                          Salemilk.date <= date_today, Salemilk.date >= date_last).all()
    data_sale = []
    for i in get_sale_milk:
        t = i.date
        text2 = t.strftime("%Y-%m-%d")
        data_sale.append(text2)
    data_sal = list(dict.fromkeys(data_sale))
    data_sale_cost =[]
    for i in data_sal:
        sal = db.session.query(func.sum(Salemilk.total)).filter(Salemilk.user_id == user.id,
                            Salemilk.date == i).scalar()
        data_sale_cost.append(sal)
        
        
    #kHow to find data for to get data expense
    date_today = date.today()
    determie_delta = timedelta(6)
    date_last = date_today - determie_delta
    get_stall_milk = Milkstall.query.filter(Milkstall.user_id == user.id,
                                          Milkstall.date <= date_today, Milkstall.date >= date_last).all()
    data_total = []
    for i in get_sale_milk:
        t = i.date
        text2 = t.strftime("%Y-%m-%d")
        data_total.append(text2)
    data_stall_total_date = list(dict.fromkeys(data_total))
    data_stall_milk =[]
    for i in data_stall_total_date:
        sal = db.session.query(func.sum(Milkstall.totalmilk)).filter(Milkstall.user_id == user.id,
                            Milkstall.date == i).scalar()
        data_stall_milk.append(sal)
        

    
    
    return render_template("index.html",
                            data_exp = data_exp,
                            data_exp_price = data_exp_price,
                            data_sal = data_sal,
                            data_sale_cost = data_sale_cost,
                            data_stall_total_date = data_stall_total_date,
                            data_stall_milk = data_stall_milk,
                           ex_all = ex_all,
                           sale_all = sale_all,
                           milk_all = milk_all,
                           ds = date4, ex = ex, mount = mount,
                           data3 = data3,data1 = datas1,
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