# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:48:23 2021

@author: Johannes
"""
import sys,os
sys.path.append('.')
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load data
data = pd.read_excel('applicationProcessData.xlsx')
data.drop(labels=['DATE','NAME'],axis=1,inplace=True)

# Get unique values in dataframe
unique_labs = pd.unique(data.values.flatten())

# Create label/node dictionaries
nodeLabel_dict = dict(enumerate(unique_labs, 0))
labelNode_dict = {value : key for (key, value) in nodeLabel_dict.items()}

# Iter over rows to work out source and target nodes
pair_list = []
for i,j in data.iterrows():
    for k in range(len(j.values)-1):
        s = j.values[k]
        t = j.values[k+1]
        if s is not t and not pd.isnull(s) and not pd.isnull(t):
            pair_list.append({'From': s, 'To': t})

# Get counts of from and to
counts=pd.DataFrame(pair_list).groupby(['From','To']).size().reset_index(name='counts')

# Get lists of sources, targets and labels
from_=counts['From'].tolist()
to_=counts['To'].tolist()
unique_values=pd.unique(pd.concat((counts['From'],counts['To']),axis=0)).tolist()
from_indices=[unique_values.index(i) for i in from_]
to_indices=[unique_values.index(i) for i in to_]

# Create figure
fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label = unique_values
      # color
    ),
    # Add links
    link = dict(
      source =  from_indices,
      target =  to_indices,
      value =  counts['counts']
))])

fig.update_layout(title="Job search year 2021", font_size=20)
plot(fig)