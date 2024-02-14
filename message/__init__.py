from requests import sessions
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask import Flask
import mongoengine as db
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_caching import Cache

# import flask_fs as fs

# from flask_ckeditor import CKEditor


import os
from dotenv import load_dotenv
load_dotenv()

database_name = "projectbestfriends"

# DB_URI = os.environ["DB_URI"]
DB_URI = os.getenv('DB_URI') or os.environ["DB_URI"]
UPLOAD_FOLDER = '/temp_file_storage'



config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1000
}

db.connect(host=DB_URI)
app = Flask(__name__)
bcrypt = Bcrypt(app)
CSRFProtect(app)
cache = Cache(app,config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
# fs.init_app(app)

# ckeditor = CKEditor(app)

# remove the limit for csrf token
app.secret_key  = os.getenv('APP_SECRET') or os.environ["APP_SECRET"]
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.config['CONTENT_TYPE'] = 'multipart/form-data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SECURE=True
)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=420)

# app.config['SESSION_COOKIE_SECURE '] = True
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['REMEMBER_COOKIE_SECURE '] = True


#login 
login_manager = LoginManager(app)
login_manager.session_protection = "strong"


login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from message import routes
