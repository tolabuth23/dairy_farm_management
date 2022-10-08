import datetime
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.models import Cow, Cowfeed, Employeesalary, FoodItem, Foodunit, Getvaccince, Staff, Stall, User, Vaccinetype
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  

@app.route("/vaccine")
def vaccine():
    user = User.query.get(current_user.id)
    get = Getvaccince.query.filter(Getvaccince.user_id == user.id).order_by(Getvaccince.id.desc())
    page = request.args.get('page', 1, type=int)
    data = get.paginate(page = page, per_page = 5)
    print(datetime.datetime.now() + timedelta(days=382))
    return render_template("/vaccine/vaccine.html",data = data)
@app.route("/add_vaccine", methods=["POST", "GET"])
def add_vaccine():
    user = User.query.get(current_user.id)
    stalls = Stall.query.filter(Stall.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    vacs = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    if request.method == "POST":
        vaccine_id = request.form["vaccine_id"]
        date = request.form["date"]
        cow_id = request.form["cow_id"]
        remark = request.form["remark"]
        stall_id = request.form["stall_id"]
        time = request.form["time"]  
        get =Getvaccince(date=date, stall_id = stall_id,cow_id= cow_id, vaccine_id = vaccine_id, remark = remark , time= time, user_id=current_user.id)
        db.session.add(get)
        db.session.commit()
        return redirect(url_for("vaccine"))
    return render_template("/vaccine/add_vaccine.html",stall = stalls, cow = cows, data = vacs)


@app.route("/get_animal_vaccine", methods=["POST", "GET"])
def get_animal_vaccine():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(id = parent_id).first()
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/vaccine/response.html', datas = datas)})


@app.route("/get_cow_info", methods=["POST", "GET"])
def get_cow_info():
     user = User.query.get(current_user.id)
     if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        datas = Cow.query.filter_by(id = parent_id).first()
        vactype = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
        getv = Getvaccince.query.filter(Getvaccince.user_id == user.id, Getvaccince.cow_id == datas.id).all()
     return jsonify({'htmlresponse': render_template('/vaccine/cow_response.html', data = datas,vactype = vactype, getv = getv)})
 
 

@app.route("/delete_getVac:<int:id>")
def delete_getVac(id):
    user = User.query.get(current_user.id)
    getVac = Getvaccince.query.filter(Getvaccince.user_id == user.id)
    get = getVac.filter_by(id = id).first()
    db.session.delete(get)
    db.session.commit()
    return redirect(url_for("vaccine"))