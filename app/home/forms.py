from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from .. import document

class SignUp(FlaskForm):
	name = StringField('Your Name (First & Last)', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	ssn = StringField('Social Security Number (Last 4 digits)', validators=[DataRequired()])
	pdf_file = FileField('Scanned document of your Driving License', validators=[FileRequired(), FileAllowed(document, '.doc file Only')])
	submit = SubmitField('Apply')

class Login(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
