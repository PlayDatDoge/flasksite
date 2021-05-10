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
# player_skill_df = pd.read_csv("D:\datalist\\tbl_player_skill.csv", header=0)
# player_movement_df = pd.read_csv("D:\datalist\\tbl_player_movement.csv", header=0)
# player_mentality_df = pd.read_csv("D:\datalist\\tbl_player_mentality.csv", header=0)
# player_power_df = pd.read_csv("D:\datalist\\tbl_player_power.csv", header=0)
# player_profile_df = pd.read_csv("D:\datalist\\tbl_player_profile.csv", header=0)
# player_traits_df = pd.read_csv("D:\datalist\\tbl_player_traits.csv", header=0)
# player_specialities_df = pd.read_csv("D:\datalist\\tbl_player_specialities.csv", header=0)


player_df = pd.read_csv("datasets/players.csv", header=0)
url_df = pd.read_csv("datasets/tbl_player_urls.csv", header=0)['str_url']
linearreg = "ProjectFlask/datasets/linearreg.sav"

def corr_table():
	corr = player_df.corr()
	mask = np.zeros_like(corr)
	mask[np.triu_indices_from(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize=(15, 15))
		ax = sns.heatmap(corr,mask=mask,square=True,linewidths=.8,cmap="coolwarm")


def fixname():
	namelist = [val.split('/')[-3].replace('-',' ').title() for val in url_df]
	player_df['str_player_name'] = pd.Series(namelist)
    



def player_finder(name):
	name = name.title()
	if name in player_df['str_player_name'].values:
		 print('Further information about the player: '+name+'down below')   
	else:
		 print('No such player, Try using capital letters / for example  "Ben Hough"')







