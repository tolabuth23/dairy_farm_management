from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root@localhost/dairymanagement'
app.config['SECRET_KEY'] = b'tola@1212'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category="info"

from main import routes
from main.signIO import routes
from main.staff import routes
from main.parlor import routes
from main.feed import routes
from main.vaccine import routes
from main.breeding import routes
from main.expense import routes
from main.supplier import routes
from main.manage import routes
from main.catalog import routes
from main.reporting import routes
from main.treatment import routes
from main.admin import routes