from email.policy import default
from tkinter.tix import Select, Tree
from flask_login import UserMixin
import datetime
import json
from main import db,bcrypt
from main import login_manager
import time



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self,value, dialect):
        if value is None:
            return "{}"
        else:
            return json.dumps(value)
    def process_result_value(self,value, dialect):
        if value is None:
            return "{}"
        else:
            return json.loads(value)

# relationships = db.Table('relationships',
#     db.Column('cow_id', db.Integer(), db.ForeignKey("cow.id")),
#     db.Column("vaccinetype_id", db.Integer(), db.ForeignKey("vaccinetype.id")))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    farmname = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, default="0931516482")
    address = db.Column(db.String(200), nullable=False, default="Ubon Ratchathani")
    password = db.Column(db.String(50),nullable=False)
    user_type = db.Column(db.String(50), nullable=False, default="Farmer")
    user_img = db.Column(db.String(50), nullable=False,default="user.png")
    user_date = db.Column(db.Date(),default=datetime.datetime.utcnow)
    staffs = db.relationship('Staff', backref='user', lazy='dynamic')
    employeesalarys = db.relationship('Employeesalary', backref='user', lazy='dynamic')
    salemilks = db.relationship("Salemilk", backref='user', lazy='dynamic')
    cowfeeds = db.relationship("Cowfeed", backref='user', lazy='dynamic')
    vaccines = db.relationship("Vaccine", backref='user', lazy='dynamic')
    cowsales = db.relationship("Cowsale", backref='user',lazy='dynamic')
    expenses = db.relationship("Expense", backref='user',lazy='dynamic')
    suppliers = db.relationship("Supplier", backref='user',lazy='dynamic')
    branchs = db.relationship("Branch", backref="user", lazy='dynamic')
    animaltypes = db.relationship("Animaltype", backref="user", lazy='dynamic')
    vaccinetypes = db.relationship("Vaccinetype", backref="user", lazy='dynamic')
    foodunits = db.relationship("Foodunit", backref='user', lazy="dynamic")
    fooditems = db.relationship("FoodItem", backref='user', lazy='dynamic')
    monitorservices = db.relationship("Monitoringservice", backref='user', lazy='dynamic')
    cows = db.relationship("Cow", backref="user", lazy='dynamic')
    stalls = db.relationship("Stall", backref="user", lazy="dynamic")
    gc = db.relationship("Getvaccince", backref="user", lazy="dynamic")
    pu = db.relationship("Pregnant", backref="user", lazy="dynamic")
    milkstall = db.relationship("Milkstall", backref="user", lazy="dynamic")
    tr = db.relationship("Treatment", backref="user", lazy="dynamic")
    def __repr__(self) -> str:
        return f'<User: {self.username}>'
        
class Staff(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(20), nullable=False)
    joining_date = db.Column(db.Date(), nullable=False, default=datetime.datetime.utcnow)
    resign_date = db.Column(db.Date(), nullable=False, default=datetime.datetime.utcnow)
    staff_img = db.Column(db.String(30), default = '1.png')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    staffs = db.relationship("Employeesalary", backref="staff", lazy="dynamic")
    def __repr__(self) -> str:
        return f'<Staff: {self.fullname}>'

class Employeesalary(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(db.Integer(), db.ForeignKey("staff.id"))
    pay_date = db.Column(db.Date(), nullable=False, default=datetime.datetime.utcnow)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    salary_amount = db.Column(db.Integer(), nullable=False)
    addition_amount = db.Column(db.Integer(), nullable=False)
    total = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'<Employeesalary: {self.total}>'

    
class Salemilk(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False,default=datetime.datetime.utcnow)
    invoice = db.Column(db.String(50), nullable=False)
    sale_no =db.Column(db.String(50), nullable=False)
    supplier_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    lite = db.Column(db.Float(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    total = db.Column(db.Float(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'<Sale Milk: {self.sale_no}>'
class Cowfeed(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    stall_no = db.Column(db.String(50), nullable=False)
    datefrom = db.Column(db.Date(), nullable=False, default=datetime.datetime.utcnow)
    dateto = db.Column(db.Date(), nullable=False)
    note = db.Column(db.String(200), nullable=False)
    feed_item = db.Column(JsonEcodedDict)
    item_quantity = db.Column(JsonEcodedDict)
    unit = db.Column(JsonEcodedDict)
    feeding_time = db.Column(JsonEcodedDict)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
class Vaccine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    stall_no = db.Column(db.String(50), nullable=False)
    cow_number = db.Column(db.String(30), nullable=False)
    vaccine_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date(), default= datetime.datetime.utcnow)
    note = db.Column(db.String(200), nullable=False)
    dose = db.Column(db.String(100), nullable=False)
    repeat = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.String(100), nullable=False)
    given_time = db.Column(db.Date(), default = datetime.datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Vaccine: {self.vaccine_name}>'



class Cowsale(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    invoice = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200),nullable=False)
    cow_img = db.Column(db.String(100), default="cow.png")
    animaltype_id = db.Column(db.String(50), nullable=False)
    animail_id = db.Column(db.String(50), nullable=False)
    stall_no  = db.Column(db.String(50), nullable=False)
    sell_price = db.Column(db.Float(), nullable=False)
    total_price = db.Column(db.Float(), nullable=False)
    due_amount= db.Column(db.Float(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Cow Feed: {self.invoice}>'

class Expense(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    purposes = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Expense: {self.date}>'



class Supplier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(100), nullable=False, default="supplier.png")
    supplier_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address =db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __reduce__(self):
        return f'<Supplier: {self.supplier_name}>'

class Branch(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    build_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address  = db.Column(db.String(50), nullable=False)
    setup_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Branch: {self.branch_name}>'

class Animaltype(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    cows = db.relationship("Cow", backref="animaltype", lazy="dynamic")
    calfs = db.relationship("Calf", backref="animaltype", lazy="dynamic")
    pres = db.relationship("Pregnant", backref="animaltype", lazy='dynamic')
    def __repr__(self) -> str:
        return f'<AnimalType: {self.type_name}>'

class Vaccinetype(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vaccine_name = db.Column(db.String(100), nullable=False)
    period_day = db.Column(db.Integer(), nullable=False)
    repeat_vaccine = db.Column(db.String(20), nullable=False)
    dose = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    gv = db.relationship("Getvaccince", backref="vaccinetype", lazy="dynamic")
    cows =db.relationship("Cow", backref="vaccinetype", lazy="dynamic")
    calfs =db.relationship("Calf", backref="vaccinetype", lazy="dynamic")
    def __repr__(self) -> str:
        return f'<Vaccinetype: {self.vaccine_name}>'

class Foodunit(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    unit_name = db.Column(db.String(100), nullable=False)
    user_id  = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<FoodUnit: {self.unit_name}>'

class FoodItem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f"<FoodItem : {self.item_name}>"

class Monitoringservice(db.Model):
    id  = db.Column(db.Integer(), primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Monitoring: {self.service_name}>'   
class Cow(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cow_no = db.Column(db.String(30), nullable=False)
    date_of_birth  = db.Column(db.Date(), nullable=False, default=datetime.datetime.utcnow())
    animal_age = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    animaltype_id = db.Column(db.Integer(), db.ForeignKey('animaltype.id'))
    pregnant_status = db.Column(db.String(50), nullable=False)
    previous_pregnant = db.Column(db.String(50), nullable=False)
    next_prenancy = db.Column(db.String(100), nullable=False)
    milk_per_day = db.Column(db.String(100), nullable=False)
    buy_from = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Integer(), nullable=False)
    buy_date = db.Column(db.Date(),nullable=False)
    stall_id = db.Column(db.Integer(), db.ForeignKey('stall.id'))
    previous_vaccine_done = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    vaccinetype_id = db.Column(db.Integer(), db.ForeignKey('vaccinetype.id'))
    cow_img = db.Column(db.String(50), nullable=False, default="logo.png")
    calfs = db.relationship("Calf", backref='cow', lazy='dynamic')
    # vaccinetypes = db.relationship("Vaccinetype", secondary = relationships, backref=db.backref('cow', lazy="dynamic"), lazy='dynamic')
    gc = db.relationship("Getvaccince", backref="cow", lazy="dynamic")
    pc = db.relationship("Pregnant", backref="cow", lazy="dynamic")
    tr = db.relationship("Treatment", backref="cow", lazy="dynamic")
    def __repr__(self) -> str:
        return f'<Cow: {self.cow_no}>'

class Calf(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    calf_no = db.Column(db.String(50), nullable=False)
    calf_img = db.Column(db.String(50), nullable=False, default="1.png")
    stall_mother = db.Column(db.Integer(), db.ForeignKey("stall.id"))
    motherid = db.Column(db.Integer(), db.ForeignKey("cow.id"))
    date_of_birth = db.Column(db.Date(),nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    animaltype_id = db.Column(db.Integer(), db.ForeignKey('animaltype.id'))
    calf_age = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    stall_no = db.Column(db.String(50), nullable=False)
    previous_vaccine_done = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200), nullable=False)
    vaccinetype_id = db.Column(db.Integer(), db.ForeignKey('vaccinetype.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f'<Calf: {self.calf_no}>'

class Stall(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    stall_number =db.Column(db.String(50), nullable=False)
    total_cow = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    stalls = db.relationship("Cow", backref="stall", lazy='dynamic')
    calfs = db.relationship("Calf", backref='stall', lazy='dynamic')
    gt = db.relationship("Getvaccince", backref="stall", lazy='dynamic')
    ps = db.relationship("Pregnant", backref="stall", lazy='dynamic')
    tr = db.relationship("Treatment", backref="stall", lazy='dynamic')
    def __repr__(self) -> str:
        return f"<Stall: {self.stall_number}>"

class Getvaccince(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    stall_id = db.Column(db.Integer(), db.ForeignKey("stall.id"))
    cow_id = db.Column(db.Integer(), db.ForeignKey("cow.id"))
    vaccine_id = db.Column(db.Integer(), db.ForeignKey("vaccinetype.id"))
    remark = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    def __repr__(self) -> str:
        return f"<Get Vaccine: {self.date}>"
class Pregnant(db.Model):
    id = db.Column(db.Integer(), primary_key=Tree)
    stall_id = db.Column(db.Integer(), db.ForeignKey("stall.id"))
    cow_id  = db.Column(db.Integer(), db.ForeignKey("cow.id"))
    pregnancy_type = db.Column(db.String(50), nullable=False)
    semen_type = db.Column(db.Integer(), db.ForeignKey("animaltype.id"))
    semen_push_date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    pregnancy_start_date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    delivery_date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    semen_cost = db.Column(db.Integer(), nullable=False)
    pregnancy_status = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    def __repr__(self):
        return f"<Pregnant: {self.pregnancy_type}>"


class Milkstall(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    stall_no = db.Column(db.String(50), nullable=True)
    totalmilk = db.Column(db.Integer(), nullable=True)
    milk_detail = db.Column(JsonEcodedDict)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    def __repr__(self) -> str:
        return f"<Milkstall: {self.milk_detail}>"
# Treatment of model
class Treatment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    stall_no = db.Column(db.Integer(), db.ForeignKey("stall.id"))
    cow_no = db.Column(db.Integer(), db.ForeignKey("cow.id"))
    medicine = db.Column(db.String(100), nullable=True)
    symptom = db.Column(db.String(100), nullable=True)
    spend = db.Column(db.Integer(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    def __repr__(self) -> str:
        return f"<Treatment: {self.medicine}>"
    
    
    