from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder="views", static_folder="static")

app.config['SECRET_KEY'] = 'c4a7705a9e3c2040aca1b9f803201fb6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrigenius.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para continuar'
login_manager.login_message_category = 'alert-info'

def create_app():
    from app import routes
    routes.init_app(app)
    return app
