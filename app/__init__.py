from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

# Create an instance of SQLAlchemy (the ORM) with the Flask Application
db = SQLAlchemy(app)
# Create an instance of Migrate which will be our migration engine and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view= 'login'
login.login_message = 'bruh... login first'
login.login_message_category = 'danger'

from app.blueprints.api import api

app.register_blueprint(api)

from . import routes, models

