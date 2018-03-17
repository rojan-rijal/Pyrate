# app/__init__.py

# third-party imports
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
document = UploadSet('documents', DOCUMENTS)
login_manager = LoginManager() 

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config["production"])
    app.config.from_pyfile('../instance/config.py')
    db.init_app(app)
    migrate = Migrate(app,db)
    from app import models
    Bootstrap(app)
    configure_uploads(app, document)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in"
    login_manager.login_view = "users.login"

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
	return render_template('error.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
	return render_template('error.html'), 500

    return app
