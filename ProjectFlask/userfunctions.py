import collections
import pandas as pd
import numpy as np
import datetime
from sklearn import linear_model
from numpy.distutils.system_info import dfftw_info
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split  
# Import train_test_split function
from sklearn import metrics  
# Import scikit-learn metrics module for accuracy calculation
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import seaborn as sns
import os 
from flask_sqlalchemy import SQLAlchemy
import json
# player_skill_df = pd.read_csv("D:\datalist\\tbl_player_skill.csv", header=0)
# player_movement_df = pd.read_csv("D:\datalist\\tbl_player_movement.csv", header=0)
# player_mentality_df = pd.read_csv("D:\datalist\\tbl_player_mentality.csv", header=0)
# player_power_df = pd.read_csv("D:\datalist\\tbl_player_power.csv", header=0)
# player_profile_df = pd.read_csv("D:\datalist\\tbl_player_profile.csv", header=0)
# player_traits_df = pd.read_csv("D:\datalist\\tbl_player_traits.csv", header=0)
# player_specialities_df = pd.read_csv("D:\datalist\\tbl_player_specialities.csv", header=0)
import requests
from bs4 import BeautifulSoup
from PIL import Image
from urllib.request  import urlopen,Request

player_df = pd.read_csv("datasets/players.csv", header=0)
url_df = pd.read_csv("datasets/tbl_player_urls.csv", header=0)['str_url']
linearreg = "ProjectFlask/datasets/linearreg.sav"
player19_df = pd.read_csv("datasets/FIFADATA.csv", header=0)
team_df = pd.read_csv("datasets/teams.csv", header=0)
team_df_url = pd.read_csv("datasets/team_urls.csv", header=0)

# def currencyConverter(val):
#     if val[-1] == 'M':
#         val = val[1:-1]
#         val = float(val) * 1000000
#         return val
        
#     elif val[-1] == 'K':
#         val = val[1:-1]
#         val = float(val) * 1000
#         return val
    
#     else:
#         return 0

# player19_df['Value in Pounds'] = player19_df['Value'].apply(currencyConverter)
# player19_df['Wage in Pounds'] = player19_df['Wage'].apply(currencyConverter)



player19_df.head()

def corr_table():
	corr = player_df.corr()
	mask = np.zeros_like(corr)
	mask[np.triu_indices_from(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize=(15, 15))
		ax = sns.heatmap(corr,mask=mask,square=True,linewidths=.8,cmap="coolwarm")


namelist = [val.split('/')[-3].replace('-',' ').title() for val in url_df]
player_df['str_player_name'] = pd.Series(namelist)
    

player19_df.rename(columns={'Unnamed: 0': 'player_id19','ID' : 'int_player_id' ,'Name' : 'str_player_name'},inplace=True)

json_df = player_df.to_json(orient='records')
json_df19 = player19_df.to_json(orient='records')
json_dfteam = team_df.to_json(orient='records')


# with open('json_dfteam.json','w') as f:
#     f.write(json_dfteam)

# url = 'http://sofifa.com/teams?type=club'
# https://cdn.sofifa.com/teams/467/60.png


# for i in range(1,682):
# 	url_x = dict(team_df_url.loc[i-1])
# 	url_loc = url_x['str_url'].split('/')[4]
# 	url = 'https://cdn.sofifa.com/teams/'+url_loc+'/60.png'
# 	try:
# 		d = Request('https://cdn.sofifa.com/teams/'+url_loc+'/60.png', headers={'User-Agent': 'Mozilla/5.0'})
# 		x = Image.open(urlopen(d)).save('ProjectFlask/static/club_images/'+str(i)+'.png','PNG')
# 	except:
# 		pass

	
	