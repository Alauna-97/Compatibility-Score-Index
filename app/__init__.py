from flask import Flask
from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "CompatibiltyScore"

UPLOAD_FOLDER = 'C:\\Program Files\\heroku\\flasky\\Compatibility-Score-Index\\app\\static\\uploads'

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/csi"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
