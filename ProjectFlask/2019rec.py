
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
data = pd.read_csv('datasets/FIFADATA.csv')
#Taking only the attirbutes from the datafile
attributes = data.iloc[:, 54:83]
# adding the missing column skill moves to attributes df
attributes['Skill Moves'] = data['Skill Moves']

workrate = data['Work Rate'].str.get_dummies(sep='/ ')

attributes = pd.concat([attributes, workrate], axis=1)
df = attributes
attributes = attributes.dropna()
df['Name'] = data['Name']
df = df.dropna()

scaled = StandardScaler()
X = scaled.fit_transform(attributes)

recommendations = NearestNeighbors(n_neighbors=6,algorithm='ball_tree')
recommendations.fit(X)


player_index = recommendations.kneighbors(X)[1]



def get_index(x):
    return df[df['Name']==x].index.tolist()[0]

def recommend_me(player):
    print("5 Players similar to {} are : ".format(player))
    index=  get_index(player)
    for i in player_index[index][1:]:
        print(df.iloc[i]['Name'])



