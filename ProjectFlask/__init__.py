from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasksite.db'
app.config['SECRET_KEY'] = 'CodexFadex'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



with app.app_context():
  from . import routes
  db.create_all()