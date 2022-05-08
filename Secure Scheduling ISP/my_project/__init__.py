#__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from waitress import serve

login_manager = LoginManager()

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def authenticate(username,password):
    if username and password:
        if username=="admin" and password=="fdkgfhbgfvcvfhbgfb":
            return True
        else:
            return False
    return False

app.config['SECRET_KEY']='mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'