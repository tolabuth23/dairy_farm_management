from cgitb import text
from datetime import date, timedelta
import datetime

from main import db,app
from flask import render_template,session,request,flash,redirect,url_for
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Calf, Cow, Cowfeed, Expense, Milkstall, Pregnant, Product, Salemilk, Staff, Stall, Supplier, User,bcrypt
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func


def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route("/dashboard")
def dashoard():
    staff = db.session.query(Staff).filter(Staff.user_id==current_user.id).count()
    cow = db.session.query(Cow).filter(Cow.user_id == current_user.id).count()
    print("This is cow: ", cow)
    
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
    
 
        
    pre = Pregnant.query.filter(Pregnant.user_id == current_user.id).all()
    print("This is a pregnant ", pre)
    #show about cow about near pregnant
    if pre:
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
                pre_id = str(i.id)
                datase = i.delivery_date.strftime("%Y-%m-%d")
                DictItems = {pre_id:{'stall_no': i.stall.stall_number,'cow_no': i.cow.cow_no,'delivery_date':datase}}
                if "DictPre" in session:
                    if pre_id in session["DictPre"]:
                        for key, item in session["DictPre"].items():
                            if key == pre_id:
                                session.modified =True
                               
                    else:
                        session["DictPre"] = MergeDict(session["DictPre"], DictItems)
                        print('This is i DictPreg: ', session['DictPre'])
                else:
                    session["DictPre"] = DictItems
                
                session['amount'] = mount
            else:
                print("No have pregnment!!!!")
                
                
                
    #pop up of the item in dictPre of pregnant until pregnant
    #convert date now() to string
    date_now = datetime.datetime.now()
    listPre = []
    date_now_convert = date_now.strftime("%Y-%m-%d")
    pre = Pregnant.query.filter(Pregnant.user_id == current_user.id).all()
    
    if pre:
        if "DictPre" in session:
            for key, item in session["DictPre"].items():
                print(key)
                if item["delivery_date"] == date_now_convert: 
                    listPre.append(key)
                    #edit of pregnant status
                    stall_no = item['stall_no']
                    cow_ID = item['cow_no']
                    stal = Stall.query.filter_by(stall_number = stall_no).first()
                    stall_id = stal.id
                    print("Stall id", stall_id)
                    cow1 = Cow.query.filter_by(cow_no = cow_ID,stall_id = stall_id).first()
                    print("Cow ID", cow1.id)
                    cow1.pregnant_status ="No Pregnant"
                    db.session.commit()
                    
                else:
                    session.modified =True         
    #pop
   
    for i in listPre:
        session["DictPre"].pop(i, None)
        session['amount'] -= 1
            
            
    
    dat = date.today()
    dat1 = timedelta(6)
    da = dat - dat1
    user = User.query.get(current_user.id)
    
    ex =Expense.query.filter(Expense.date <= dat, Expense.date >= da ,Expense.user_id == user.id).all()
    
    date4 = []
    for i in ex:
        t = i.date
        text1 = t.strftime("%Y-%m-%d")
        date4.append(text1)
        #get data all
            
    user = User.query.get(current_user.id) 
    ex_all = Expense.query.filter(Expense.user_id == user.id).all()
    sale_all = Salemilk.query.filter(Salemilk.user_id == user.id).all()
    milk_all = Milkstall.query.filter(Milkstall.user_id == user.id).all()
        
        
    #kHow to find data for to get data expense
    date_today = date.today()
    determie_delta = timedelta(6)
    user = User.query.get(current_user.id)
    date_last = date_today - determie_delta
    get_data_expense = Expense.query.filter(Expense.user_id == user.id, 
                        Expense.date <= date_today, Expense.date >= date_last).all()
    data_expense = []
    month_expense=[]
    for i in get_data_expense:
        t = i.date
        text1 =t.strftime("%Y-%m-%d")
        data_expense.append(text1)
        tx = t.strftime("%m")
        month_expense.append(tx)
     
     #tst
    #get month expense 
    get_month_ex = Expense.query.filter(Expense.user_id == user.id, 
                        Expense.month <= 12, Expense.month >= 1).all()
    for i in get_month_ex:
        t = i.date
        tx = t.strftime("%m")
        month_expense.append(tx)
        
    month_expense_date = list(dict.fromkeys(month_expense))
    pr_month_exp=[]
    print("Date of month expense", month_expense_date)
    for i in month_expense_date:
        pr_month_expense = db.session.query(func.sum(Expense.total_amount)).filter(Expense.month == i).scalar()
        pr_month_exp.append(pr_month_expense)
    print("Month price of data: ", pr_month_exp)
    
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
    txt_date =[]
    for i in get_sale_milk:
        t = i.date
        text2 = t.strftime("%Y-%m-%d")
        data_sale.append(text2)
        
        
    get_month =Salemilk.query.all()    
    for i in get_month:
        t = i.date

        txt1 = t.strftime("%m")
        txt_date.append(txt1)
    
    
    fromkey_txt_date = list(dict.fromkeys(txt_date))
    print("from key txt date: ",fromkey_txt_date)
    month_sale_list =[]
    for i in fromkey_txt_date:
        month_sale = db.session.query(func.sum(Salemilk.total)).filter(Salemilk.user_id == user.id,
                            Salemilk.month == i).scalar()
        month_sale_list.append(month_sale)
    print("Month sale list: ", month_sale_list)
    
    data_sale_cost =[]
    data_sal = list(dict.fromkeys(data_sale))
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
    
    for i in get_stall_milk:
        t = i.date
        text2 = t.strftime("%Y-%m-%d")
        data_total.append(text2)
        
        
    
   
    
    data_stall_total_date = list(dict.fromkeys(data_total))
    data_stall_milk =[]
    for i in data_stall_total_date:
        sal = db.session.query(func.sum(Milkstall.totalmilk)).filter(Milkstall.user_id == user.id,
                            Milkstall.date == i).scalar()
        data_stall_milk.append(sal)
        
        
        

    cfeed = Cowfeed.query.filter(Cow.user_id == user.id)
    
    
    #Net income of farm
    #Month of netincome
    month_character =["Jan","Feb","Mar","Apr","May","June","Junly","Aug", "Sep", "Oct","Nov", "Dec"]
    month_data_income =[]
    for index, item in enumerate(fromkey_txt_date):
        get_month = month_character[int(item)-1]
        month_data_income.append(get_month)
    print("Month date income",month_data_income)    
    #month_sale_list,pr_month_exp
    print(month_sale_list)
    print(pr_month_exp)
    net_income =[]
    if pre:
        if month_sale_list:
            for index, item in enumerate(month_sale_list):
                print("this is number", index)
                net = month_sale_list[index] - pr_month_exp[index]
                print(net)
                net_income.append(net)
                print("Net in of farm", net_income)
    return render_template("index.html",
                           net_income = net_income,
                           month_data_income=month_data_income,
                           data = cfeed,enumerate = enumerate,
                            data_exp = data_exp,
                            data_exp_price = data_exp_price,
                            data_sal = data_sal,
                            data_sale_cost = data_sale_cost,
                            data_stall_total_date = data_stall_total_date,
                            data_stall_milk = data_stall_milk,
                           sale_all = sale_all,
                           milk_all = milk_all,
                           ds = date4, ex = ex, 
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