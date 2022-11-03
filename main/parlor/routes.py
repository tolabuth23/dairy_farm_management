
from datetime import date
from re import search
from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify,make_response
from main.signIO.forms import LoginForm, RegisterForm
from main.models import Cow, Employeesalary, Milkstall, Salemilk, Staff, Stall,  Supplier, User,bcrypt
from flask_login import current_user, login_user, logout_user
import io,secrets,os
import pdfkit

@app.route("/parlor/collect_milk", methods=["POST", "GET"])
def collect_milk():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        page = request.args.get('page', 1, type=int)
        csm = Milkstall.query.filter(Milkstall.user_id == user.id)
        by_date = request.form['by_date']
        csmilk = csm.filter(Milkstall.date.like('%'+by_date+'%') | Milkstall.stall_no.like('%'+ by_date+'%')).order_by(Milkstall.id.desc())
        data = csmilk.paginate(page = page, per_page = 100)
        
        
    else:
        user = User.query.get(current_user.id)
        csmilk = Milkstall.query.filter(Milkstall.user_id == user.id).order_by(Milkstall.id.desc())
        page = request.args.get('page', 1, type=int)
        data = csmilk.paginate(page = page, per_page = 20)
    
    
    return render_template('parlor/collect_milk.html', data = data)


@app.route("/new_stall_milk",methods=["POST","GET"])
def newstallmilk():
    user = User.query.get(current_user.id)
    stall = Stall.query.filter(Stall.user_id == user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    return render_template("/parlor/stall_milk.html", stall = stall, cow = cow)


@app.route("/get_stall_no", methods=["POST", "GET"])
def get_stall_no():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.get(parent_id).first()
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/parlor/response.html', datas = datas)})



@app.route("/get_animal", methods=["POST", "GET"])
def get_animal():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        stall = Stall.query.filter_by(stall_number = parent_id).first()
        
        s = stall.id
        datas = Cow.query.filter(Cow.stall_id == s)
    return jsonify({'htmlresponse': render_template('/parlor/response.html', datas = datas)})

def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
@app.route("/add_stallmilk", methods=["POST", "GET"])
def add_stallmilk():
    if request.method == "POST":
        stall_no = request.form["stall_no"]
        cow_no = request.form["cow_id"]
        milk = request.form["milk"]
        milk_id = cow_no
        DictItems = {milk_id:{'stall_no': stall_no, 'cow_no': cow_no, 'milk': milk}}
        if "Dictmilk" in session:
            if milk_id in session["Dictmilk"]:
                for key, item in session["Dictmilk"].items():
                    if key == milk_id:
                        session.modified =True
            else:
                session["Dictmilk"] = MergeDict(session["Dictmilk"], DictItems)
                print(session["Dictmilk"])
                return jsonify({'htmlresponse': render_template("/parlor/milk_response.html")})
        else:
            session["Dictmilk"] = DictItems
            print(session["Dictmilk"])
            return jsonify({'htmlresponse': render_template("/parlor/milk_response.html")})
        return jsonify({'htmlresponse': render_template("/parlor/milk_response.html")})
    
    
    
@app.route("/milkstall", methods=["POST", "GET"])
def milkstall():
    if request.method =="POST":
        milk_detail = session["Dictmilk"]
        print(milk_detail)
        totalmilk =0
        for key, item in session["Dictmilk"].items():
            stall_no = item["stall_no"]
            totalmilk = int(item["milk"]) + totalmilk
        
        db.session.add(Milkstall(stall_no=stall_no, milk_detail=milk_detail, totalmilk=totalmilk, user_id = current_user.id))
        db.session.commit()
        session.pop("Dictmilk",None)
        return redirect(url_for("collect_milk"))
@app.route("/milk_parlor/delete_collect_milk:<int:id>")
def delete_collect_milk(id):
    user = User.query.get(current_user.id)
    milk  = Milkstall.query.filter(Milkstall.user_id == user.id)
    milk = milk.filter_by(id  =id).first()
    db.session.delete(milk)
    db.session.commit()
    return redirect(url_for('collect_milk'))


@app.route("/parlor/sale_milk", methods=['POST', "GET"])
def sale_milk():
    user = User.query.get(current_user.id)
    sal1 = Salemilk.query.filter(Salemilk.user_id == user.id).all()
    sal = Salemilk.query.filter(Salemilk.user_id == user.id).order_by(Salemilk.id.desc())
    n = 0
    if sal:
        for no in sal1:
            n = no.sale_no
            print(n)
        n1 = int(n) + 1
        sale_no = n1
    else:
        sale_no = 1001
    cmilk = Milkstall.query.filter(Milkstall.user_id == user.id, Milkstall.date == date.today())
    salemilk = Salemilk.query.filter(Salemilk.user_id == user.id, Salemilk.date == date.today())
    cm = date.today()
    print(cmilk)
    totalmilk = 0
    for dt in cmilk:
        totalmilk = int(dt.totalmilk) + totalmilk  
        print(totalmilk)
    to = totalmilk    
    print(to)
    suppliers = Supplier.query.filter(Supplier.user_id == user.id)
    tsale = 0
    for s in salemilk:
        tsale = int(s.lite) + tsale
    s = tsale
    print(s)
    if request.method == 'POST':
        
        page = request.args.get('page', 1, type=int)
        csm = Salemilk.query.filter(Salemilk.user_id == user.id)
        search = request.form['search']
        salemilks = csm.filter(Salemilk.date.like('%'+search+'%') | Salemilk.sale_no.like('%'+ search+'%') | Salemilk.supplier_name.like('%'+search+'%')).order_by(Salemilk.id.desc())
        data = salemilks.paginate(page = page, per_page = 100)
    else:
        
        sal = Salemilk.query.filter(Salemilk.user_id == user.id).order_by(Salemilk.id.desc())
        page = request.args.get('page', 1, type=int)
        data = sal.paginate(page = page, per_page = 25)
        
    
    
    return render_template("/parlor/sale_milk.html",sale_no = sale_no, data = data, datas = to, suppliers = suppliers , cmilk = cm, saled = s)

@app.route("/delete_smilk:<int:id>")
def delete_smilk(id):
    user = User.query.get(current_user.id)
    salemilk = Salemilk.query.filter(Salemilk.user_id == user.id)
    sm = salemilk.filter_by(id =id).first()
    db.session.delete(sm)
    db.session.commit()
    return redirect(url_for("sale_milk"))

@app.route("/new_smilk", methods=["POST", "GET"])
def new_smilk():
    invoice = secrets.token_hex(5)
    if request.method == "POST":
        sale_no = request.form["sale_no"]
        lite = request.form["lite"]
        price = request.form["price"]
        total = request.form["total"]
        supplier_name = request.form["supplier_name"]
        contact = request.form["contact"]
        email = request.form["email"]
        address = request.form["address"]
        month_today = date.today()
        month_today = month_today.strftime("%m")
        smilk = Salemilk(month=month_today,invoice = invoice,sale_no = sale_no, supplier_name = supplier_name,
        contact = contact, email = email, address = address, lite = lite, price = price, total = total, user_id =current_user.id)
        db.session.add(smilk)
        db.session.commit()
        return redirect(url_for("sale_milk"))
@app.route("/parlor/order:<int:id>")
def order(id):
    ord = Salemilk.query.filter_by(id = id).first()
    return render_template("/parlor/order.html", tola = "Tola", ord = ord)

@app.route("/get_account_info", methods=["POST", "GET"])
def get_account_info():
    user = User.query.get(current_user.id)
    Sup = Supplier.query.filter(Supplier.user_id == user.id)
    if request.method == "POST":
        parent_id = request.form["parent_id"]
        print(parent_id)
        accu = Sup.filter_by(supplier_name = parent_id).first()
    return jsonify({"htmlresponse": render_template('parlor/sale_response.html', sup = accu)})


