from requests import sessions
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask import Flask
import mongoengine as db
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
load_dotenv()

database_name = "projectbestfriends"

# DB_URI = os.environ["DB_URI"]
DB_URI = os.getenv('DB_URI') or os.environ["DB_URI"]


db.connect(host=DB_URI)
app = Flask(__name__)

CSRFProtect(app)

# remove the limit for csrf token
app.config['WTF_CSRF_TIME_LIMIT'] = None

app.secret_key  = "hori-san"
#login 
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from message import routes
