#__init__.py imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from waitress import serve

# Login Manager comes from flask_login
login_manager = LoginManager()

# Initialize new flask app (it's in the name)
app = Flask(__name__)
auth = HTTPBasicAuth()

# If password is verified, only then will we authenticate
@auth.verify_password
def authenticate(username,password):
    if username and password:
        # Environment variables to protect password from being exposed, and authenticate the username and password.
        if username=="admin" and password==os.environ["Password"]:
            return True
        else:
            return False
    return False

# Configure SECRET_KEY for Werkzeug, configure SQLite file and don't track modifications, unnecessary overhead.
app.config['SECRET_KEY']='mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the database to the flask app and migrate these changes (see presentation for details on migration)
db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'


os.environ.get("password")
os.environ.get("password")



