from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify,make_response
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Calf, Cow, Employeesalary, Expense, Getvaccince, Milkstall,  Pregnant, Salemilk, Staff, Stall, User, Vaccinetype,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time
import pdfkit
from sqlalchemy import func
@app.route("/office_report")
def office_report():
    
    return render_template("/reporting/office_expense.html")

@app.route("/get_expense_report", methods=["POST", "GET"])
def get_expense_report():
    if request.method == "POST":
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Expense.query.filter(Expense.date >= date_from, Expense.date <=date_to, Expense.user_id == user.id).all()
        total = 0.0
        for dt in data:
            total = total + dt.total_amount
    return jsonify({"htmlresponse": render_template("/reporting/expense_response.html", data = data,date_from=date_from, date_to = date_to, total_amount = total)})
@app.route("/get_expense", methods=["POST", "GET"])
def get_expense():
    random_hex = secrets.token_hex(8)
    if request.method == "POST":
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Expense.query.filter(Expense.date >= date_from, Expense.date <=date_to, Expense.user_id == user.id).all()
        total = 0.0
        for dt in data:
            total = total + dt.total_amount
        rendered= render_template("/pdf/expense_pdf.html",data = data,date_from=date_from, date_to = date_to, total_amount = total)
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] ='application/pdf'
        response.headers['Content-Disposition']='attachment; filename='+random_hex+'.pdf'
        return response
    return request(url_for('office_expense'))



@app.route("/employee_salary")
def employee_salary():
    user = User.query.get(current_user.id)
    staff = Staff.query.filter(Staff.user_id == user.id)
    return render_template("/reporting/employee_salary.html", data = staff)

@app.route("/get_employee_salary", methods=["POST","GET"])
def get_employee_salary():
    if request.method == "POST":
        month = request.form["month"]
        year = request.form["year"]
        employee = request.form["employee"]
        print(month)
        print(year)
        print(employee)
        user = User.query.get(current_user.id)
        data = Employeesalary.query.filter(Employeesalary.user_id == user.id, Employeesalary.employee_id== employee,
                                           Employeesalary.month == month, Employeesalary.year == year).all()
        print(data)
        return jsonify({"htmlresponse": render_template("/reporting/salary_response.html", data = data, month = month, year=year, employee = employee)})
        

#this is get html salary to pdf
@app.route("/salary_pdf", methods=["POST", "GET"])
def salary_pdf():
    random_hex = secrets.token_hex(8)
    if request.method == "POST":
        month = request.form["month"]
        year = request.form["year"]
        employee = request.form["employee"]
        print(month)
        print(year)
        print(employee)
        user = User.query.get(current_user.id)
        data = Employeesalary.query.filter(Employeesalary.user_id == user.id, Employeesalary.employee_id== employee,
                                           Employeesalary.month == month, Employeesalary.year == year).all()
        rendered= render_template("/pdf/salary_pdf.html",data = data, month = month, year=year, employee = employee)
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] ='application/pdf'
        response.headers['Content-Disposition']='attachment; filename='+random_hex+'.pdf'
        return response
    return request(url_for('employee_salary'))       



@app.route("/milk_collect")
def milk_collect():
    user = User.query.get(current_user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    
    return render_template("/reporting/milk_collect.html", data = stall)

@app.route("/get_milk_collect", methods=["POST","GET"])
def get_milk_collect():
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Milkstall.query.filter(Milkstall.user_id == user.id, Milkstall.date >= date_from, Milkstall.date <=date_to,
                                      Milkstall.stall_no == stall_no).all()
        total = 0
        for dt in data:
            total = total + int(dt.totalmilk)
            
        return jsonify({"htmlresponse": render_template("/reporting/milk_response.html",stall_no = stall_no ,total = total, data = data, date_from = date_from, date_to = date_to)})
#this is get html salary to pdf
@app.route("/milk_pdf", methods=["POST", "GET"])
def milk_pdf():
    random_hex = secrets.token_hex(8)
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Milkstall.query.filter(Milkstall.user_id == user.id, Milkstall.date >= date_from, Milkstall.date <=date_to,
                                      Milkstall.stall_no == stall_no).all()
        total = 0
        for dt in data:
            total = total + int(dt.totalmilk)
        rendered= render_template("/pdf/milk_pdf.html",total = total, data = data, date_from = date_from, date_to = date_to)
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] ='application/pdf'
        response.headers['Content-Disposition']='attachment; filename='+random_hex+'.pdf'
        return response
    return request(url_for('milk_collect')) 


@app.route("/milk_sale")
def milk_sale():
    user = User.query.get(current_user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    
    return render_template("/reporting/milk_sale.html", data = stall)
@app.route("/get_milk_sale", methods=["POST","GET"])
def get_milk_sale():
    if request.method == "POST":
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Salemilk.query.filter(Salemilk.user_id == user.id, Salemilk.date >= date_from, Salemilk.date <=date_to).all()
        #make a data of sale chart
        print("Date _from : ", date_from)
        print("Date to :", date_to) 
        data_date = []
        for i in data:
            t = i.date
            text1 =t.strftime("%Y-%m-%d")
            data_date.append(text1)
        print("Date date: ", data_date)
        data_date_focus = list(dict.fromkeys(data_date))
        print("Data date focus: ", data_date_focus)
        data_sale_milk = []
        for i in data_date_focus:
            ddf = db.session.query(func.sum(Salemilk.total)).filter(Salemilk.user_id ==user.id, 
                                    Salemilk.date == i).scalar()
            data_sale_milk.append(ddf)
            
  
        
        chart =[]
        dates = []
        supplier =[]
        for i in data:
            chart.append(int(i.total))
            dates.append(i.date)
            supplier.append(i.supplier_name)
        sup = list(dict.fromkeys(supplier))
        dates = list(dict.fromkeys(dates))
        total_date =[]
        for i in dates:
            dat =db.session.query(func.sum(Salemilk.total)).filter(Salemilk.date == i).scalar()
            total_date.append(dat)
            
        total =[]
        for i in sup:
            dat =db.session.query(func.sum(Salemilk.lite)).filter(Salemilk.supplier_name == i,Salemilk.date >= date_from, Salemilk.date <=date_to).scalar()
            total.append(dat)
        sup_total = dict(zip(sup,total_date))
        s =[{"num1": 200}, {"num2": 300}, {"num3": 400}, {"num4": 500}]
        totalprice = 0
        for dt in data:
            totalprice = totalprice +int(dt.total)
        return jsonify({"htmlresponse": render_template("/reporting/sale_response.html",
                                                        data_date = data_date_focus,
                                                        sup_total = s,total = total,sup = sup,
                                                        da =chart,dates = dates,
                                                        totalprice = totalprice,data = data,data_sale_milk = data_sale_milk,
                                                        date_from = date_from, date_to = date_to,
                                                        chart = total_date)})
#this is get html salary to pdf
@app.route("/sale_pdf", methods=["POST", "GET"])
def sale_pdf():
    random_hex = secrets.token_hex(8)
    if request.method == "POST":
      
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Salemilk.query.filter(Salemilk.user_id == user.id, Salemilk.date >= date_from, Salemilk.date <=date_to).all()
        totalprice = 0
        for dt in data:
            totalprice = totalprice +int(dt.total)
        rendered= render_template("/pdf/sale_pdf.html",totalprice = totalprice,data = data, date_from = date_from, date_to = date_to)
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] ='application/pdf'
        response.headers['Content-Disposition']='attachment; filename='+random_hex+'.pdf'
        return response
    return request(url_for('milk_collect')) 

@app.route("/vaccine_monitor")
def vaccine_monitor():
    user = User.query.get(current_user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    
    return render_template("/reporting/vaccine_monitor.html", stall= stall)

@app.route("/get_vaccine_monitor", methods=["POST","GET"])
def get_vaccine_monitor():
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        cow_id = request.form["cow_id"]
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Getvaccince.query.filter(Getvaccince.user_id == user.id, Getvaccince.date >= date_from, Getvaccince.date <=date_to,
                                        Getvaccince.stall_id == stall_no, Getvaccince.cow_id == cow_id).all()
       
        return jsonify({"htmlresponse": render_template("/reporting/vaccine_response.html",stall_no = stall_no, cow_id =cow_id,date_from = date_from, date_to = date_to,data = data)})
#this is get html salary to pdf
@app.route("/vaccine_pdf", methods=["POST", "GET"])
def vaccine_pdf():
    random_hex = secrets.token_hex(8)
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        cow_id = request.form["cow_id"]
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        user = User.query.get(current_user.id)
        data = Getvaccince.query.filter(Getvaccince.user_id == user.id, Getvaccince.date >= date_from, Getvaccince.date <=date_to,
                                        Getvaccince.stall_id == stall_no, Getvaccince.cow_id == cow_id).all()
        rendered= render_template("/pdf/vaccine_pdf.html",date_from = date_from, date_to = date_to,data = data)
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] ='application/pdf'
        response.headers['Content-Disposition']='attachment; filename='+random_hex+'.pdf'
        return response
    return request(url_for('vaccine_monitor')) 

@app.route("/get_sanimal", methods=["POST", "GET"])
def get_sanimal():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(id = parent_id).first()
        
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/reporting/aresponse.html', datas = datas)})

@app.route("/cow_statistic")
def cow_statistic():
    user = User.query.get(current_user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    calf = Calf.query.filter(Calf.user_id == user.id).all()
   
    return render_template("/reporting/cow_statistic.html", stall= stall, calf = calf)
@app.route("/get_canimal", methods=["POST", "GET"])
def get_canimal():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(id = parent_id).first()
        
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/reporting/cresponse.html', datas = datas)})

@app.route("/get_cow_statistic", methods=["POST","GET"])
def get_cow_statistic():
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        cow_no = request.form["cow_id"]
        user = User.query.get(current_user.id)
        print(stall_no)
        print(cow_no)
        data = Cow.query.filter(Cow.user_id == user.id, Cow.stall_id == stall_no, Cow.cow_no == cow_no).all()
        print(data)
        
        return jsonify({"htmlresponse": render_template("/reporting/cow_response.html",data = data)})
    
@app.route("/get_scow_info", methods=["POST", "GET"])
def get_scow_info():
     user = User.query.get(current_user.id)
     if request.method == "POST":
        parent_id = request.form["parent_id"]
        stall_id = request.form["stall_id"]
        print("Satll _id", parent_id)
        datas = Cow.query.filter_by(id = parent_id).first()
        print("Cow ID",datas.id)
        getv = Getvaccince.query.filter(Getvaccince.user_id == user.id, Getvaccince.cow_id == datas.id).all()
        pre = Pregnant.query.filter(Pregnant.user_id == user.id, Pregnant.stall_id ==stall_id, Pregnant.cow_id == datas.id).all()
        print("Pre",pre)
        calf = Calf.query.filter(Calf.user_id == user.id, Calf.motherid == parent_id, Calf.stall_mother == stall_id).all()
     return jsonify({'htmlresponse': render_template('/reporting/cow_response_statistic.html',calf = calf, data = datas, getv = getv, pre = pre,dat = timedelta(280), dates = datetime, d =date, datetime = datetime)})
 