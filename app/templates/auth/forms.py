
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')