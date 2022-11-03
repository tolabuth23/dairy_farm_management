from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Cow, Employeesalary, Expense, Pregnant, Staff, Stall, User,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time

def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
@app.route("/breeding", methods=["POST","GET"])
def breeding():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        pres = Pregnant.query.filter(Pregnant.user_id == user.id)
        search = request.form['search']
        if search == "":
            pre = Pregnant.query.filter(Pregnant.user_id == user.id).order_by(Pregnant.id.desc())
            page = request.args.get('page', 1, type=int)
            data = pre.paginate(page = page, per_page = 25)
            
        else:
            stall = Stall.query.filter_by(stall_number = search).first()
            if stall:
                stall_id = int(stall.id)
                preg = pres.filter(Pregnant.stall_id.like(stall_id)).order_by(Pregnant.id.desc())
                data = preg.paginate(page = page, per_page = 100)
            cow = Cow.query.filter_by(cow_no = search).first()
            if cow:
                cow_id = int(cow.id)
                print(cow.id)
                preg = pres.filter(Pregnant.cow_id.like(cow_id)).order_by(Pregnant.id.desc())
                data = preg.paginate(page = page, per_page = 100)
            pre = Pregnant.query.filter(Pregnant.user_id == user.id).order_by(Pregnant.id.desc())
            page = request.args.get('page', 1, type=int)
            data = pre.paginate(page = page, per_page = 25)
    else:
        pre = Pregnant.query.filter(Pregnant.user_id == user.id).order_by(Pregnant.id.desc())
        page = request.args.get('page', 1, type=int)
        data = pre.paginate(page = page, per_page = 25)
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
        month_today = date.today()
        month_today = month_today.strftime("%m")
        
        ex = Expense(date = date.today(), month=month_today, purposes= "Semen Cost", detail = "Expense on the breeding cow.", total_amount = semen_cost, user_id=current_user.id)
        db.session.add(ex)
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
        if pstatus == "Delivered":
            cow.pregnant_status ="Pregnant"
            db.session.commit()
        dat = timedelta(280)
        print(data.pregnancy_start_date + dat)
        data.pregnancy_start_date = psd 
        data.pregnancy_status = pstatus
        print(psd)
        db.session.commit()
        data.delivery_date = data.pregnancy_start_date +dat
        db.session.commit()
        
    pre = Pregnant.query.filter(Pregnant.user_id == current_user.id)
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
                                print('This is  DictPreg: ', session['DictPre'])
                    else:
                        session["DictPre"] = MergeDict(session["DictPre"], DictItems)
                        print('This is i DictPreg: ', session['DictPre'])
                else:
                    session["DictPre"] = DictItems
                print("The mount of pregnment",mount)
                session['amount'] = mount
            else:
                print("No have pregnment!!!!")
                
                
    date_now = datetime.datetime.now()
    listPre = []
    date_now_convert = date_now.strftime("%Y-%m-%d")
    print("This is date now convert", date_now_convert)
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
                print("The cow is pregnant already!!")
            else:
                session.modified =True         
    #pop
    print('This list pre',listPre)
    for i in listPre:
        session["DictPre"].pop(i, None)
        session['amount'] -= 1
        print("This dict pregnant is pop already!!",i)        
                
    return redirect(url_for("breeding"))

@app.route("/delete_breeding:<int:id>")
def delete_breeding(id):
    user = User.query.get(current_user.id)
    breeding = Pregnant.query.filter(Pregnant.user_id == user.id)
    get = breeding.filter_by(id = id).first()
    cow = Cow.query.filter_by(id=get.cow_id, stall_id=get.stall_id).first()
    cow.pregnant_status ="No Pregnant"
    db.session.commit()
    db.session.delete(get)
    db.session.commit()
    return redirect(url_for("breeding"))