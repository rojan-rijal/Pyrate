from flask import render_template, flash, redirect, url_for, session, send_file
from forms import SignUp, Login
from flask_login import login_required, login_user, logout_user
from . import home
from .. import document, db
from ..models import User, PassResets
@home.route('/')
def homepage():
	return render_template('home/index.html')

@home.route('/apply', methods=['GET','POST'])
def apply():
	form = SignUp()
	if form.validate_on_submit():
		try:
			filename = document.save(form.pdf_file.data)
			url = document.url(filename)
			user = User(email = form.email.data, full_name = form.name.data,
			    	    password = form.password.data, ssn = form.ssn.data)
			db.session.add(user)
			db.session.commit()
			flash('Your application has been submitted. You may now login but you will not be able to use the account until it is approved.')
			return redirect(url_for('home.homepage'))
		except:
			flash('Something went wrong during registration')
			return render_template('home/index.html')
	return render_template('home/apply.html', form = form)

@home.route('/login', methods=['GET','POST'])
def login():
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is not None and user.verify_password( form.password.data ):
			login_user(user)
			return redirect(url_for('users.profile'))
		else:
			flash('Invalid login. Check to make sure your email and password matches')
	return render_template('home/login.html', form = form, title='Login')
