import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv("datasets\\FIFADATA.csv", header=0)
top_clubs = df.groupby(by=['Club'])['Overall'].sum().reset_index().sort_values(by=["Overall"], ascending=False).head(10)
sns.barplot(y='Club', x='Overall', data=top_clubs, palette=sns.color_palette("Blues_r", 10))