
#Imports!
from logging import exception
from types import TracebackType
from flask import redirect, url_for, render_template, request,session  
from .models import db, User,login_manager,Team
from . import rec_2020 
from . import rec_2019
from . import reg2020
import flask_login
from flask_login import login_user, login_required, logout_user , current_user
from flask import current_app as app
from .userfunctions import player_df,player19_df,team_df
from flask_sqlalchemy import SQLAlchemy
import traceback


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


@app.route('/myteams',methods=['POST', 'GET'])
@login_required
def myteam():
	if current_user.user_teams != '':
		return render_template('myteams.html',user_team_list = current_user.user_teams)
	return render_template('createTeam.html')

@app.route('/myteam/<int:team_id>',methods=['POST', 'GET'])
@login_required
def myteamID(team_id):

	if request.method == "POST":
		player_id = request.form['player_id']
		sellplayer(team_id,int(player_id))
	try:
		team_info=current_user.user_teams[team_id-1].__dict__
		team_players_int = [int(player_id) for player_id in team_info['team_players'].split(',') if player_id]
		team_players_str = []
		for player in team_players_int:
			team_players_str.append(player_df.iloc[player-1]['str_player_name'])
		
		print(team_players_str)
		team_players = dict(zip(team_players_str,team_players_int))
	
		return render_template('myteam.html',myteam_info=team_info,team_players=team_players)
		
	except Exception as ex:
		print(traceback.format_exc())
		print(ex)
		return render_template('myteam.html',myteam_info=team_info,team_players={})


@app.route('/createTeam',methods=['POST', 'GET'])
@login_required
def createTeam():
	if request.method == "POST":
		team_name = request.form['team_name']
		team_version = request.form['version']
		if request.form['league'] == 'premierleague':
			team_balance = 200000000
		if request.form['league'] == 'laliga':
			team_balance = 180000000
		if not Team.query.filter_by(team_name=team_name).first():
			db.session.add(Team(team_name=team_name,team_version=team_version,team_balance=team_balance,user_id=current_user.id))
			db.session.commit()
			return redirect(url_for('index'))
	return render_template('createTeam.html')

@app.route('/player',methods=['POST', 'GET'])
def player():
	if current_user.is_authenticated:
		if not 'database' in session:
			session['database'] = current_user.database
	return render_template('player.html')
	
@app.route('/teams',methods=['POST', 'GET'])
@login_required
def teams():
	return render_template('teams.html')
	

@app.route('/player/<int:player_id>')
def playerbyID(player_id):
	if current_user.is_authenticated:
		if not 'database' in session:
			session['database'] = current_user.database
	if 'database' in session:
		if session['database'] == 'FIFA19':
			userdf=player19_df
		elif session['database'] == 'FIFA20':
			userdf=player_df
	else:
		userdf=player19_df
	return render_template('player.html',player_info=dict(userdf.loc[player_id]),player_id=str(player_id+1))

@app.route('/teams/<int:team_id>')
@login_required
def teambyID(team_id):
	return render_template('teams.html',team_info=dict(team_df.loc[team_id]),team_id=str(team_id+1))

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


@app.route('/alreadyAteam',methods=['POST', 'GET'])
@login_required
def alreadyAteam():
	if request.method == 'POST':
		session['database'] = 'FIFA20'
		name = request.form['name']
		# Gets the team's information , by the user's input (if exists) str_offensive_style str_defensive_style
		request_team = team_df.loc[team_df['str_team_name']==name].squeeze()
		try:
			eteam = Team(team_name =name,team_balance = int(request_team['int_transfer_budget']) ,\
				team_version = 'FIFA20', team_offensive_style = request_team['str_offensive_style'],\
					team_defensive_style = request_team['str_defensive_style'],df_team_id= int(request_team['int_team_id']))

			player_list = ''
			for player in player_df.loc[player_df['int_team_id'] == request_team['int_team_id']].values:
				print(type(player))
				print(player)
				player_list += str(player[0]) + ','
			
			eteam.team_players = player_list

			db.session.add(eteam)
			current_user.user_teams.append(eteam)
			db.session.commit()
			print(eteam)
		except Exception as ex:
			print(traceback.format_exc())
			print(ex)
			return render_template('alreadyAteam.html')
		return redirect(url_for('myteam'))
	return render_template('alreadyAteam.html')

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))


@app.errorhandler(404)
def error_handler(error):
	print(error)
	return render_template("404.html")

@app.route('/buyplayer/<int:team_id>',methods=['POST', 'GET'])
@login_required
def buyplayer(team_id):

	return render_template('buyplayer.html')

@app.route('/buyplayer/<int:team_id>/<int:player_id>',methods=['POST', 'GET'])
@login_required
def buyplayerV2(team_id,player_id):
	if current_team	:= current_user.user_teams[team_id-1]:
		print(current_team)
		if str(player_id+1) not in current_team.team_players:
			if current_team.team_version == 'FIFA20':
				request_player = player_df.loc[player_df['int_player_id']==player_id+1].squeeze()
				if current_team.team_balance > int(request_player['int_value']) :
					current_team.team_balance -= int(request_player['int_value']) 
					current_team.team_players += str(request_player['int_player_id']) + ','
					db.session.commit()
					return redirect(url_for('myteamID',team_id=team_id))
				else:
					return render_template('buyplayer.html',err='not enough money!')

			else:
				return render_template('buyplayer.html',err='not enough money!')
	return render_template('buyplayer.html')

def sellplayer(team_id,player_id):

	player = player_df.iloc[player_id-1]
	team = current_user.user_teams[team_id-1]
	team.team_balance = int(team.team_balance+player['int_value'])
	team_players_list = team.team_players.split(',')
	team_players_list.remove(str(player_id))
	team.team_players = ','.join(team_players_list)

	db.session.commit()

@app.route('/sitetools',methods=['POST', 'GET'])
@login_required
def sitetools():

	return render_template('sitetools.html')


@app.route('/similarplayers')
@login_required
def similarplayers():
	
	return render_template('knnsearch.html')

@app.route('/similarplayers/<int:player_id>',methods=['POST', 'GET'])
@login_required
def recommendedplayers(player_id):
	if current_user.database == 'FIFA20' :
		rec_players = rec_2020.similar_player(player_id+1)
		player	= player_df[player_df['int_player_id']==player_id+1].squeeze()
		return render_template('similarplayers.html',recommended = rec_players,player_name=player['str_player_name'])

	player	= player19_df[player19_df['int_player_id']==player_id+1].squeeze()
	rec_players = rec_2019.recommend_me(player['str_player_name'])

	return render_template('similarplayers.html',recommended = rec_players,player_name=player['str_player_name'])



@app.route('/linearreg')
@login_required
def linearreg():
	return render_template('linearreg.html')



@app.route('/linearreg/<int:player_id>',methods=['POST', 'GET'])
@login_required
def linoutput(player_id):
	player = player_df[player_df['int_player_id']==player_id+1].squeeze()
	print(player)
	reg2020.prep_data_linear_regression()
	value = reg2020.predict_by_linear_regression(player['int_overall_rating'],player['int_wage'],player['int_reactions'],player['int_composure'],player['int_potential_rating'],player['int_international_reputations'])
	print(value)
	if int(value) > int(player['int_value']):
		value = ''
		return render_template('linearreg.html',value="is worth buying",player_name=player['str_player_name'])
	else:
			return render_template('linearreg.html',value="is not worth buying!",player_name=player['str_player_name'])
	

