import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import os

from plotly.offline import init_notebook_mode, iplot, plot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go

from sklearn.neighbors import NearestNeighbors

pd.set_option('display.max_columns', None)

import warnings
warnings.filterwarnings('ignore')


player_df = pd.read_csv("datasets/players.csv", header=0)
team_df = pd.read_csv("datasets/teams.csv", header=0)[['int_team_id','str_team_name']]
# Player Attributes 
field_cols = [
    'int_ball_control', 'int_long_passing', 'int_fk_accuracy', 
    'int_curve', 'int_dribbling', 'int_skill_moves', 
    'int_weak_foot', 'int_long_shots', 'int_shot_power', 
    'int_stamina', 'int_jumping', 'int_agility', 
    'int_balance', 'int_reactions', 'int_sprint_speed', 
    'int_acceleration', 'int_composure', 'int_vision', 
    'int_positioning', 'int_kicking', 'int_handling', 'int_diving','int_penalties','int_sliding_tackle','int_standing_tackle',
    'int_defensive_awareness','int_volleys','int_short_passing','int_heading_accuracy','int_finishing','int_crossing'
]

tr = player_df[['int_player_id','str_player_name']+field_cols].dropna()
id_name = player_df[['str_player_name','int_player_id']].set_index('int_player_id')['str_player_name'].to_dict()


NUM_RECOM = 7

X = tr[field_cols].dropna().values
nbrs = NearestNeighbors(n_neighbors=NUM_RECOM+1, algorithm='ball_tree').fit(X)
dist, rank = nbrs.kneighbors(X)

similar_df = pd.DataFrame(columns=[f'rank_{i}'for i in range(1,NUM_RECOM+1)],
                          index=tr['int_player_id'].values,
                          data=rank[:,1:])
dist_df = pd.DataFrame(columns=[f'rank_{i}'for i in range(1,NUM_RECOM+1)],
                       index=tr['int_player_id'].values,
                       data=dist[:,1:])


for cols in list(similar_df):
    tg_col = similar_df[cols]
    new_value = tr['int_player_id'].iloc[tg_col].tolist()
    similar_df[cols] = new_value


def similar_player(player_id):
    player_id = int(player_id)
    player_name = tr[tr['int_player_id'] == player_id]['str_player_name'].values[0]
    
    ## Bar chart
    
    Xaxis = reversed(1/(1+dist_df.loc[player_id].values[::-1]))
    Yaxis = reversed(similar_df.loc[player_id].map(id_name).values[::-1])
    
    return dict(zip(Yaxis,Xaxis))

    

