import datetime
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.models import Cow, Cowfeed, Employeesalary, FoodItem, Foodunit, Staff, Stall, User
from flask_login import current_user, login_user, logout_user
import io,secrets,os

@app.route("/cow_feed")
def cow_feed():
    user = User.query.get(current_user.id)
    cfeed = Cowfeed.query.filter(Cow.user_id == user.id)
    print(datetime.datetime.today())
    date_and_time = datetime.datetime(2020, 2, 19, 12, 0, 0)
    print(date_and_time)
    time_change = datetime.timedelta(hours=336)
    new_time = date_and_time + time_change
    print(new_time)
    
    return render_template("/feed/cow_feed.html", data = cfeed,enumerate = enumerate)


@app.route("/add_feed",methods=["POST", "GET"])
def add_feed():
    user = User.query.get(current_user.id)
    mother = Cow.query.filter(Cow.user_id == user.id)
    unitItem = Foodunit.query.filter(Foodunit.user_id == user.id)
    foodItem = FoodItem.query.filter(FoodItem.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    if request.method == "POST":
        stall_nos = request.form["stall_no"]
        datefrom = request.form["datefrom"]
        dateto = request.form["dateto"]
        note = request.form["note"]
        
        foodname = request.form.getlist('foodname[]')
        unit_name = request.form.getlist('unit_name[]')
        quality = request.form.getlist("quality[]")
        feedtime = request.form.getlist("feeding_time[]")
        print(quality)
        cfeed = Cowfeed(stall_no =stall_nos,datefrom = datefrom, dateto = dateto, note =note,
        feed_item = foodname, item_quantity = quality, unit = unit_name, feeding_time=feedtime, user_id = current_user.id)
        db.session.add(cfeed)
        db.session.commit()
        return redirect(url_for("cow_feed"))
    return render_template("/feed/add_feed.html",stall = stall,cow = cow, foodItem = foodItem,foodUnit = unitItem, mother = mother)


@app.route("/edit_feed:<int:id>", methods=["POST", 'GET'])
def edit_feed(id):
    user = User.query.get(current_user.id)
    mother = Cow.query.filter(Cow.user_id == user.id)
    unitItem = Foodunit.query.filter(Foodunit.user_id == user.id)
    foodItem = FoodItem.query.filter(FoodItem.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    cfeed = Cowfeed.query.filter(Cowfeed.user_id == user.id)
    cfd = cfeed.filter_by(id = id).first()
    if request.method == "POST":
        cfd.stall_no = request.form["stall_no"]
        cfd.datefrom = request.form["datefrom"]
        cfd.dateto = request.form["dateto"]
        cfd.note = request.form["note"]
        cfd.feed_item = request.form.getlist('foodname[]')
        cfd.item_quantity = request.form.getlist("quality[]")
        cfd.feeding_time = request.form.getlist("feeding_time[]")
        db.session.commit()
        return redirect(url_for("cow_feed"))
    return render_template("/feed/edit_feed.html",cfd =cfd,stall = stall,cow = cow,enumerate = enumerate,
     foodItem = foodItem,foodUnit = unitItem, mother = mother,title = "Edit Feed")

@app.route("/delete_feed:<int:id>",methods=["POST", "GET"])
def delete_feed(id):
    user = User.query.get(current_user.id)
    co = Cowfeed.query.filter(Cowfeed.user_id == user.id)
    c = co.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("cow_feed"))
