from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Calf, Cow, Employeesalary, Expense,  Pregnant, Staff, Stall, User, Vaccinetype,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
from datetime import timedelta  
import datetime
from datetime import date,time

def save_picture(img):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(img.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img',image_name)
    img.save(image_path)
    return image_name

def delete_picture(img):
    os.remove(os.path.join(app.root_path, 'static/img', img))
    
@app.route("/cow")
def cow():
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    page = request.args.get('page',1,type=int)
    data = cow.paginate(page = page, per_page=10)
    
    return render_template("/manage/cow.html", data = data,datetime = datetime,d =date)

@app.route("/add_cow",methods=["POST","GET"])
def add_cow():
    user = User.query.get(current_user.id)
    animaltype = Animaltype.query.filter(Animaltype.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    vacc = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    cow = db.session.query(Cow)
    c = db.session.query(Cow).filter(Cow.stall_id == 1).count()
    
    if request.method == "POST":
        date_of_birth = request.form['date_of_birth']
        animal_age = request.form['animal_age']
        gender  = request.form['gender']
        pregnant_status = request.form['pregnant_status']
        milk_per_day = request.form['milk_per_day']
        buying_date = request.form['buying_date']
        weight = request.form['weight']
        color  = request.form['color']
        previous_pregnant = request.form['previous_pregnant']
        buy_from = request.form['buy_from']
        stall_no = request.form["stall_no"]
        height = request.form["height"]
        animal_type = request.form["animal_type"]
        next_prenancy = request.form['next_prenancy']
        buying_price = request.form['buying_price']
        previous_vaccine_done = request.form['previous_vaccine_done']
        select_previous_vaccine  = request.form['select_previous_vaccine']
        cow_img = save_picture(request.files['cow_img'])
        cow_no = request.form['cow_no']
        note = request.form['note']
        cow = Cow(cow_no= cow_no, date_of_birth = date_of_birth, animal_age = animal_age,
         weight = weight,height = height, gender = gender, color = color, animaltype_id = animal_type,
          pregnant_status = pregnant_status,previous_pregnant = previous_pregnant, next_prenancy = next_prenancy,
           milk_per_day =  milk_per_day, buy_from = buy_from,buying_price = buying_price, buy_date =buying_date,
            stall_id =stall_no,previous_vaccine_done = previous_vaccine_done, note = note, 
           user_id = current_user.id, vaccinetype_id = select_previous_vaccine, cow_img = cow_img )
        db.session.add(cow)
        db.session.commit()
        return redirect(url_for("cow"))
    
    return render_template("/manage/add_cow.html",animaltype = animaltype,stall = stall,vacc= vacc,cow = cow, Cow = Cow)
@app.route("/manage_cow/delete_cow:<int:id>")
def delete_cow(id):
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    cow = cow.filter_by(id = id).first()
    db.session.delete(cow)
    db.session.commit()
    return redirect(url_for('cow'))


@app.route("/edit_cow:<int:id>", methods=['POST', "GET"])
def edit_cow(id):
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    cow = cow.filter_by(id = id).first()
    animaltype = Animaltype.query.filter(Animaltype.user_id == user.id)
    vacc = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    if request.method == "POST":
        cow.date_of_birth = request.form["date_of_birth"]
        cow.animal_age = request.form["animal_age"]
        cow.gender = request.form['gender']
        cow.pregnant_status = request.form['pregnant_status']
        cow.milk_per_day = request.form['milk_per_day']
        cow.buying_date = request.form['buying_date']
        cow.weight  = request.form['weight']
        cow.color = request.form['color']
        cow.previous_pregnant = request.form['previous_pregnant']
        cow.buy_from = request.form['buy_from']
        cow.stall_no = request.form['stall_no']
        cow.height = request.form['height']
        cow.animal_type = request.form['animal_type']
        cow.next_prenancy = request.form['next_prenancy']
        cow.buying_price = request.form['buying_price']
        cow.previous_vaccine_done = request.form["previous_vaccine_done"]
        cow.cow_no = request.form['cow_no']
        cow.note = request.form['note']
        db.session.commit()
        return redirect(url_for("cow"))

    return render_template("/manage/edit_cow.html",datetime = datetime,d =date, data = cow, animaltype = animaltype , stall = stall,vacc =vacc)

@app.route("/manage/calf")
def calf():
    user = User.query.get(current_user.id)
    calf =Calf.query.filter(Calf.user_id == user.id)
    page = request.args.get('page',1,type=int)
    data = calf.paginate(page =page, per_page=5)
    return render_template("/manage/calf.html", data = data,datetime = datetime,d =date)

@app.route("/manage/add_calf", methods=["POST", "GET"])
def add_calf():
    user = User.query.get(current_user.id)
    animaltype = Animaltype.query.filter(Animaltype.user_id == user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    vacc = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    if request.method == "POST":
        calf_no = request.form['calf_no']
        calf_img =request.files['calf_img']
        stall_mother = request.form['stall_mother']
        calf_img = save_picture(calf_img)
        date_of_birth = request.form['date_of_birth']
        motherid = request.form["motherid"]
        gender = request.form['gender']
        animaltype_id = request.form['animal_type']
        calf_age = request.form['calf_age']
        weight = request.form['weight']
        height = request.form['height']
        color = request.form['color']
        stall_no = request.form['stall_no']
        previous_vaccine_done = request.form['previous_vaccine_done']
        note = request.form['note']
        select_previous_vaccine = request.form['select_previous_vaccine']
        calf = Calf(calf_no = calf_no, calf_img = calf_img,stall_mother=stall_mother, motherid = motherid,date_of_birth = date_of_birth,
        gender = gender, animaltype_id = animaltype_id,
        calf_age = calf_age, weight = weight, height = height, color = color, 
        stall_no = stall_no,previous_vaccine_done = previous_vaccine_done, note = note, vaccinetype_id= select_previous_vaccine,
        user_id = current_user.id)
        db.session.add(calf)
        db.session.commit()
        return redirect(url_for("calf"))
    return render_template("/manage/add_calf.html",animaltype = animaltype,stall = stall,vacc= vacc, cow = cow)


@app.route("/get_calf", methods=["POST", "GET"])
def get_calf():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(id = parent_id).first()
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/manage/response.html', datas = datas)})



@app.route("/manage_calf/edit_calf:<int:id>", methods=['POST', 'GET'])
def edit_calf(id):
    user = User.query.get(current_user.id)
    calf = Calf.query.filter(Calf.user_id == user.id)
    calf = calf.filter_by(id = id).first()
    animaltype = Animaltype.query.filter(Animaltype.user_id == user.id)
    stall = Stall.query.filter(Staff.user_id == user.id)
    vacc = Vaccinetype.query.filter(Vaccinetype.user_id == user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    if request.method == "POST":
        calf.calf_no = request.form['calf_no']
        calf_img =request.files['calf_img']
        calf_img = save_picture(calf_img)
        calf.date_of_birth = request.form['date_of_birth']
        calf.stall_mother = request.form["stall_mother"]
        calf.motherid = request.form["motherid"]
        calf.gender = request.form['gender']
        calf.animaltype_id = request.form['animal_type']
        calf.calf_age = request.form['calf_age']
        calf.weight = request.form['weight']
        calf.height = request.form['height']
        calf.color = request.form['color']
        calf.stall_no = request.form['stall_no']
        calf.previous_vaccine_done  = request.form['previous_vaccine_done']
        calf.note = request.form['note']
        calf.select_previous_vaccine = request.form['select_previous_vaccine']
        db.session.commit()
        return redirect(url_for("calf"))
    return render_template('/manage/edit_calf.html',datetime = datetime,d =date,data = calf ,animaltype = animaltype, stall= stall, cow = cow, vacc = vacc )

@app.route("/manage_calf/delete_calf:<int:id>")
def delete_calf(id):
    user = User.query.get(current_user.id)
    calf = Calf.query.filter(Calf.user_id == user.id)
    calf = calf.filter_by(id = id).first()
    db.session.delete(calf)
    db.session.commit()
    return redirect(url_for('calf'))
