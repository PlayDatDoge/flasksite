from flask import redirect, url_for, render_template, request,session
from .models import db, User,login_manager
import flask_login
from flask_login import login_user, login_required, logout_user , current_user
from flask import current_app as app


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/myteam', methods=['POST', 'GET'])
# def myteam():
#     if request.method == 'POST':
#         return render_template('myteam.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if logged_user := User.query.filter_by(username=username).first():
            if password == logged_user._hashedpassword:
                login_user(logged_user)
                print(current_user)
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]
        db.session.add(User(username=username, _hashedpassword=password, email=email))
        db.session.commit()
    return render_template('register.html')
