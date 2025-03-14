from wtforms import Form, StringField, PasswordField, validators, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from email_validator import validate_email, EmailNotValidError
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()])
    confirm = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()])

class ManufacturerApplication(FlaskForm):
    kamid = StringField('KAM ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    IndustryNiche = StringField('Industry Niche', [validators.Length(min=1, max=150), validators.DataRequired()])
    Supporting_Documents = FileField('Supporting Documents', [validators.Length(min=1, max=150), validators.DataRequired()])