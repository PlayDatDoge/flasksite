import pandas as pd
import numpy as np
import pandas as pd
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

player_df = pd.read_csv("D:\datalist\\players.csv", header=0)


corr = player_df.corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(corr,mask=mask,square=True,linewidths=.8,cmap="coolwarm")



def player_finder(name):

	if name in player_df['str_player_name'].values:
		 print('Further information about the player: '+name+'down below')
            
	else:
		 print('No such player, Try using capital letters / for example  "Ben Hough"')






