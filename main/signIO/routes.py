from main import db,app
from flask import render_template,session,request,flash,redirect,url_for
from main.signIO.forms import LoginForm, RegisterForm
from main.models import User,bcrypt
from flask_login import current_user, login_user, logout_user

@app.route("/",methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        pa = bcrypt.generate_password_hash(user.password)

        if user and bcrypt.check_password_hash(pa, form.password.data):
            session['login']=True
            session['id'] = user.id 
            login_user(user, remember=form.remember.data)
            next_page  = request.args.get('next')
            flash("Login is successfully", 'info')
            return redirect(next_page) if next_page else redirect(url_for('dashoard'))
    return render_template("signIO/signIn.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/Register",methods=["POST","GET"])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        us = User(username=form.username.data, email = form.email.data, farmname=form.farmname.data,
        password =form.password.data)
        db.session.add(us)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("/signIO/signUp.html", form = form)