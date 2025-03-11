from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo
from email_validator import validate_email, EmailNotValidError
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()])
    confirm = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()])

class AdminLoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()])