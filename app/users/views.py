from flask import render_template, flash, redirect, url_for, session, send_file
from flask_login import login_required, login_user, current_user
from forms import EditForm, SendMoney, ProfileImage
from . import users
from .. import document, db
from ..models import User, PassResets
import urllib

# function to check if user is verified
def userVerified():
	is_verified = current_user.is_verified
	if is_verified == 1:
		return True
	else:
		return False

def validate_type(url):
	# check if content-type is jpeg
	headers = urllib.urlopen(url).headers
	if headers['Content-Type'] != 'image/jpeg':
		return False
	else:
		return True


#user profile page - contains simple info: Name, SSN, Balance
@users.route('/profile')
@login_required
def profile():
	return render_template('users/profile.html')

def add_balance(id, amount):
        receive_query = User.query.get(id)
        current_balance = receive_query.balance
        new_balance = amount + current_balance
        receive_query.balance = new_balance
        db.session.commit()

def remove_balance(id, amount):
        send_query = User.query.get(id)
        current_balance = send_query.balance
        new_balance = current_balance - amount
        send_query.balance = new_balance
        db.session.commit()


#modifying user profile 
@users.route('/edit/<string:id>', methods=['GET','POST'])
@login_required
def profile_edit(id):
	form = EditForm()
	user = User.query.get(id)
	if form.validate_on_submit():
		try:
			new_email = form.email.data
			update_email = User.query.filter_by(id=id).update(dict(email=new_email))
			update_name = User.query.filter_by(id=id).update(dict(full_name=form.name.data))
			db.session.commit()
			flash('Edit successful')
			return redirect(url_for('users.profile'))
		except:
			flash('Something went wrong')
	form.email.data = user.email
	form.name.data = user.full_name
	return render_template('/users/modify.html', form = form)


@users.route('/send', methods=['GET','POST'])
@login_required
def send_money():
	form = SendMoney()
	if form.validate_on_submit():
		try:
			receiver_id = form.receiver.data
			transfer_amount = form.amount.data
			sender_id = form.sender.data
			# check if sender can send money
			send_query = User.query.get(sender_id)
			if transfer_amount > send_query.balance:
				flash("You do not have enough balance")
				return redirect(url_for('users.profile'))
			else: 
				add_balance(receiver_id, transfer_amount)
				remove_balance(sender_id, transfer_amount)
				flash('Money transfer successful')
				return redirect(url_for('users.profile'))
		except:
			flash('Something went wrong')
			return redirect(url_for('users.profile'))
	form.sender.data = current_user.id
	return render_template('users/send.html', form = form)





@users.route('/image', methods=['GET','POST'])
@login_required
def profile_image():
	form = ProfileImage()
	if form.validate_on_submit():
		link = form.url.data
		if validate_type(link):
			user = User.query.get(current_user.id)
			user.profile_image = link
			db.session.commit()
			flash("Profile picture updated")
		else:
			flash("Image is not JPEG")
	return render_template('users/image.html', form=form)
