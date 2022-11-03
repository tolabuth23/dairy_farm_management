
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Animaltype, Cow, Employeesalary, Expense, Pregnant, Staff, Stall, Supplier, User,bcrypt
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
@app.route("/supplier", methods=["POST", "GET"])
def supplier():
    user = User.query.get(current_user.id)
    sup = Supplier.query.filter(Supplier.user_id == user.id)
    page = request.args.get('page', 1, type=int)
    if request.method == "POST":
        search = request.form["search"]
        if search == "":
            data = sup.paginate(page = page, per_page=25)
        else:
            sups = sup.filter(Supplier.supplier_name.like("%"+search+"%") | Supplier.company_name.like("%"+search+"%")).order_by(Supplier.id.desc())
            data = sups.paginate(page=page, per_page=25)
            
    else:
        data = sup.paginate(page = page, per_page = 25)
    return render_template("/supplier/supplier.html",data =data)


@app.route("/add_supplier", methods=["POST", "GET"])
def add_supplier():
    if request.method == "POST":
        supplier_name = request.form["supplier_name"]
        company_name = request.form["company_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        address = request.form["address"]
        image = request.files["image"]
        image = save_picture(image)
        sup = Supplier(image = image, supplier_name = supplier_name, company_name = company_name, phone_number = phone_number,
        email = email, address = address, user_id = current_user.id)
        db.session.add(sup)
        db.session.commit()
    return redirect(request.referrer)
@app.route("/delete_supplier:<int:id>", methods=["POST", "GET"])
def delete_supplier(id):
    user = User.query.get(current_user.id)
    datas = Supplier.query.filter(Supplier.user_id == user.id)
    data = datas.filter_by(id=id).first()
    delete_picture(data.image)
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/edit_supplier:<int:id>", methods=["POST", "GET"])
def edit_supplier(id):
    user = User.query.get(current_user.id)
    datas= Supplier.query.filter(Supplier.user_id == user.id)
    data = datas.filter_by(id = id).first() 
    if request.method == "POST":
        if data.image != request.files["image"]:
            delete_picture(data.image)
        data.image =save_picture(request.files["image"])
        data.supplier_name = request.form["supplier_name"]
        data.company_name = request.form["company_name"]
        data.phone_number = request.form["phone_number"]
        data.email = request.form["email"]
        data.address = request.form["address"]
        db.session.commit()
        return redirect(request.referrer)
