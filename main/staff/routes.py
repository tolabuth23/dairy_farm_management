from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Employeesalary, Staff, User,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os

def save_picture(img):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(img.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img',image_name)
    img.save(image_path)
    return image_name

def delete_picture(img):
    os.remove(os.path.join(app.root_path, 'static/img', img))


@app.route("/staff_list")
def staff_list():
    user = User.query.get(current_user.id)
    data = Staff.query.filter(Staff.user_id == user.id)
    page = request.args.get('page', 1, type=int)
    data = data.paginate(page = page, per_page = 10)
    return render_template("/staff/staff_list.html", data = data)

@app.route("/add_staff", methods=["POST","GET"])
def add_staff():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form['email']
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        salary = request.form["salary"]
        joining_date = request.form["joining_date"]
        resign_date = request.form["resign_date"]
        staff_img = request.files["staff_img"]
        staff_img = save_picture(staff_img)
        staff = Staff(fullname = fullname, email = email, phone_number = phone_number,
        address = address, salary =salary, joining_date = joining_date, resign_date = resign_date,
        staff_img = staff_img, user_id = current_user.id)
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for("staff_list"))
    

@app.route("/human/edit_staff:<int:id>", methods=["POST","GET"])
def edit_staff(id):
    user = User.query.get(current_user.id)
    staff = Staff.query.filter(Staff.user_id == user.id)
    data = staff.filter_by(id = id).first()

    if request.method == "POST":
        data.fullname = request.form["fullname"]
        data.email = request.form["email"]
        data.phone_number = request.form["phone_number"]
        data.address = request.form["address"]
        data.salary = request.form["salary"]
        data.joining_date = request.form["joining_date"]
        data.resign_date = request.form['resign_date']
        db.session.commit()
        return redirect(url_for("staff_list"))

@app.route("/human/delete_staff:<int:id>")
def delete_staff(id):
    user = User.query.get(current_user.id)
    staff = Staff.query.filter(Staff.user_id == user.id)
    data = staff.filter_by(id = id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("staff_list"))

@app.route("/staff_salary")
def staff_salary():
    user = User.query.get(current_user.id)
    data = Employeesalary.query.filter(Employeesalary.user_id == user.id)
    page = request.args.get('page', 1, type=int)
    data = data.paginate(page = page, per_page = 10)
    staff = Staff.query.filter(Staff.user_id == user.id)
    return render_template("/staff/staff_salary.html", data = data,staff =staff)

@app.route("/get_salary_info", methods=["POST", "GET"])
def get_salary_info():
     user = User.query.get(current_user.id)
     if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        es =Staff.query.filter(Staff.user_id == user.id)
        datas = es.filter_by(id = parent_id).first()
        
     return jsonify({'htmlresponse': render_template('/staff/response.html', datas = datas)})
 
@app.route("/human/add_salary", methods=["POST","GET"])
def add_salary():
    user = User.query.get(current_user.id)
    staff = Staff.query.filter(Staff.user_id == user.id)
    if request.method == "POST":
        pay_date = request.form["pay_date"]
        month = request.form["month"]
        year = request.form["year"]
        empoyee_name = request.form["staff_id"]
        salary_amount = request.form["salary_amount"]
        addition_amount = request.form["addition_amount"]
        esalary = Employeesalary(pay_date = pay_date,employee_id = empoyee_name, month = month,
        year = year,salary_amount=salary_amount, addition_amount = addition_amount, total =int(salary_amount)+int(addition_amount),
        user_id = current_user.id )
        db.session.add(esalary)
        db.session.commit()
        return redirect(url_for("staff_salary"))

 
 
@app.route("/staff/delete_esalary:<int:id>")
def delete_esalary(id):
    user = User.query.get(current_user.id)
    es = Employeesalary.query.filter(Employeesalary.user_id == user.id)
    data  = es.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("staff_salary"))
