from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "CompatibiltyScore"

# UPLOAD_FOLDER = 'C:\\Users\\Jada-Rae\\Compatibility-Score-Index\\app\\static\\uploads'
UPLOAD_FOLDER = 'C:\\Users\\Loretta\\Desktop\\CSI\\Compatibility-Score-Index\\app\\static\\uploads'


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)

from app import views