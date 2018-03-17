from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    full_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    ssn = db.Column(db.String(200), unique=True)
    credit_limit = db.Column(db.String(200))
    balance = db.Column(db.Integer)
    card_number = db.Column(db.Integer, unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(200))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PassResets(db.Model):
    """
    Store password reset tokens
    """

    __tablename__ = 'passresets'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    reset_token = db.Column(db.String(200))
    

    def __repr__(self):
        return '<PassResets: {}>'.format(self.name)

