from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(min=3, max=30)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    farmname = StringField("Farm Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


