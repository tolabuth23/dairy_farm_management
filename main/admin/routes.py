from main import db,app
from flask import render_template,session,request,flash,redirect,url_for,jsonify

from main.models import Calf, Cow, Cowfeed, Employeesalary, Expense, Getvaccince, Milkstall, Pregnant, Salemilk, Staff, Supplier, Treatment, User

@app.route('/member')
def member():
    users = User.query.filter(User.user_type == "Farmer").all()
    return render_template("/admin/member.html",data = users)


@app.route('/delete/:<int:id>')
def delete_member(id):
    data = User.query.filter_by(id = id).first()
    da = Staff.query.filter(Staff.user_id == id)
    for i in da:
        print(i.id)
        dels = Staff.query.filter_by(id=i.id).first()
        db.session.delete(dels)
    #delete staffsalary
    sala = Employeesalary.query.filter(Employeesalary.user_id == id)
    for i in sala:
        s = Employeesalary.query.filter_by(id=i.id).first()
        db.session.delete(s)
    #delete of Stall Milk
    smilk = Milkstall.query.filter(Milkstall.user_id == id)
    for i in smilk:
        smi = Milkstall.query.filter_by(id = i.id).first()
        db.session.delete(smi)
    #delete of sale milk
    samilk = Salemilk.query.filter(Salemilk.user_id == id)
    for i in samilk:
        sam = Salemilk.query.filter_by(id=i.id).first()
        db.session.delete(sam)
        
    #delete of cow feed
    feed = Cowfeed.query.filter(Cowfeed.user_id == id)
    for i in feed:
        fe = Cowfeed.query.filter_by(id=i.id).first()
        db.session.delete(fe)
    #delete of getVaccine
    getVac = Getvaccince.query.filter(Getvaccince.user_id == id)
    for i in getVac:
        get = Getvaccince.query.filter_by(id=i.id).first()
        db.session.delete(get)
    #delete of pregnment
    breed = Pregnant.query.filter(Pregnant.user_id == id)
    for i in breed:
        br = Pregnant.query.filter_by(id=i.id).first()
        db.session.delete(br)
        
    #delete of treatment
    treat = Treatment.query.filter(Treatment.user_id == id)
    for i in treat:
        tre = Treatment.query.filter_by(id=i.id).first()
        db.session.delete(tre)
    #delete of Expense
    exp = Expense.query.filter(Expense.user_id == id)
    for i in exp:
        ex = Expense.query.filter_by(id=i.id).first()
        db.session.delete(ex)
    #delete of Supplier
    supp = Supplier.query.filter(Supplier.user_id == id)
    for i in supp:
        su = Supplier.query.filter_by(id=i.id).first()
        db.session.delete(su)
        
    #delete of Cow 
    cows = Cow.query.filter(Cow.user_id == id)
    for i in cows:
        co=Cow.query.filter_by(id=i.id).first()
        db.session.delete(co)
    #delete of calf
    calf = Calf.query.filter(Calf.user_id == id)
    for i in calf:
        ca = Calf.query.filter_by(id = i.id).first()
        db.session.delete(ca)
        
    #delte of 
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("member"))
