import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import zipfile
import os
import shutil
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA

#Import the 2019 fifa dataframe
data = pd.read_csv('datasets/players.csv')
#Taking only the attirbutes from the datafile
attributes = data[['int_ball_control', 'int_long_passing', 'int_fk_accuracy', 
    'int_curve', 'int_dribbling', 'int_skill_moves', 
    'int_weak_foot', 'int_long_shots', 'int_shot_power', 
    'int_stamina', 'int_jumping', 'int_agility', 
    'int_balance', 'int_reactions', 'int_sprint_speed', 
    'int_acceleration', 'int_composure', 'int_vision', 
    'int_positioning', 'int_kicking', 'int_handling', 'int_diving','int_penalties','int_sliding_tackle','int_standing_tackle',
    'int_defensive_awareness','int_volleys','int_short_passing','int_heading_accuracy','int_finishing','int_crossing']]


workrate = data['str_work_rate'].str.get_dummies(sep='/ ')

attributes = pd.concat([attributes, workrate], axis=1)
df = attributes
attributes = attributes.dropna()
df['str_player_name'] = data['str_player_name']
df = df.dropna()

scaled = StandardScaler()
X = scaled.fit_transform(attributes)

recommendations = NearestNeighbors(n_neighbors=6,algorithm='ball_tree')
recommendations.fit(X)


player_index = recommendations.kneighbors(X)[1]



def get_index(x):
    return df[df['str_player_name']==x].index.tolist()[0]

def recommend_me(player):
    print("5 Players similar to {} are : ".format(player))
    index=  get_index(player)
    for i in player_index[index][1:]:
        print(df.iloc[i]['str_player_name'])



