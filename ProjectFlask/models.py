from flask_login import UserMixin
from . import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(130), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(15), nullable=False,default='theme')
    database = db.Column(db.String(20), nullable=False,default='FIFA19')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def validate_password(self, password):
        return check_password_hash(self._password_hash, password)

