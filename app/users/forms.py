from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, HiddenField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from .. import document

class EditForm(FlaskForm):
	name = StringField('Your Name (First & Last)', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update Data')


class SendMoney(FlaskForm):
	sender = HiddenField('Sender', validators=[DataRequired()])
	receiver = IntegerField('User ID of the receiver', validators=[DataRequired()])
	amount = IntegerField('Amount being transferred', validators=[DataRequired()])
	submit = SubmitField('Send Money')

class ProfileImage(FlaskForm):
	url = StringField('Image link', validators=[DataRequired()])
	submit = SubmitField('Add profile picture')
