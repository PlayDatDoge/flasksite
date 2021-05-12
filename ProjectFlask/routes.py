from flask import redirect, url_for, render_template, request,session  
from .models import db, User,login_manager
import flask_login
from flask_login import login_user, login_required, logout_user , current_user
from flask import current_app as app
from .userfunctions import player_df,player19_df
from flask_sqlalchemy import SQLAlchemy

@app.route('/index')
@app.route('/')
def index():
	if not flask_login.current_user.is_authenticated:
		if 'user' in session:	
			if logged_user := User.query.filter_by(username=session['user']).first():
				login_user(logged_user)
				session['theme'] = current_user.theme
				session['database'] = current_user.database
				return render_template('index.html')
		else:
			return redirect(url_for('login'))
	return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
	session.pop('user', None)
	session.pop('theme', None)
	session.pop('database', None)
	logout_user()
	return redirect(url_for('login'))	
								

@app.route('/login', methods=['POST', 'GET'])
def login():
	if not flask_login.current_user.is_authenticated:
		if 'user' in session:
			if logged_user := User.query.filter_by(username=session['user']).first():
				login_user(logged_user)
				session['database'] = current_user.database
				session['theme'] = current_user.theme
				return redirect(url_for('index'))
		
		if request.method == 'POST':
			username12 = request.form['username']
			password = request.form['password']
			if logged_user := User.query.filter_by(username=username12).first():
				if logged_user.validate_password(password):
					session['user'] = logged_user.username
					session['theme'] = logged_user.theme
					login_user(logged_user)
					print(current_user)
					return redirect(url_for('index'))

		return render_template('login.html')
	return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		email = request.form["email"]
		if not  User.query.filter_by(username=username).first():
			db.session.add(User(username=username, password=password, email=email))
			db.session.commit()
			return redirect(url_for('login'))
	return render_template('register.html')


@app.route('/myteam',methods=['POST', 'GET'])
@login_required
def myteam():
	return render_template('myteam.html')


@app.route('/player',methods=['POST', 'GET'])
@login_required
def player():
	return render_template('player.html')
	

@app.route('/player/<int:player_id>')
def playerbyID(player_id):
	if 'database' in session:
		if session['database'] == 'FIFA19':
			userdf=player19_df
		elif session['database'] == 'FIFA20':
			userdf=player_df
	else:
		userdf=player19_df
	return render_template('player.html',player_info=dict(userdf.loc[player_id]))


@app.route('/userpref',methods=['POST', 'GET'])
@login_required
def userpref():
	if request.method == 'POST':
		if 'cbox' in request.form:
			print(current_user.theme)
			if current_user.theme == 'theme':
				current_user.theme = 'dark_theme'
			elif current_user.theme == 'dark_theme':
				current_user.theme = 'theme'
			session['theme'] = current_user.theme
		if 'dbox' in request.form:
			print(current_user.database)
			if current_user.database == 'FIFA19':
				current_user.database = 'FIFA20'
			elif current_user.database == 'FIFA20':
				current_user.database = 'FIFA19'
			session['database'] = current_user.database
		db.session.commit()
	return render_template('userpref.html')


@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))


@app.errorhandler(404)
def error_handler(error):
	print(error)
	return render_template("404.html")
