# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:48:23 2021

@author: Johannes
"""
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
# Random hex color
rNum = lambda: random.randint(0,255)
rCol = lambda: 'rgba(%i,%i,%i,0.4)' % (rNum(),rNum(),rNum())

# Load data
data = pd.read_excel('applicationProcessData.xlsx')
data.drop(labels=['DATE','NAME'],axis=1,inplace=True)

# Get unique values in dataframe
uniqueLabs = pd.unique(data.values.flatten())

# Create label/node dictionaries
nodeLabelDict = dict(enumerate(uniqueLabs, 0))
labelNodeDict = {value : key for (key, value) in nodeLabelDict.items()}

# Create color dictionary
colorDict = {value : rCol() for (_, value) in nodeLabelDict.items()}

# Iter over rows to work out source and target nodes
pairList = []
for i,j in data.iterrows():
    for k in range(len(j.values)-1):
        s = j.values[k]
        t = j.values[k+1]
        if s is not t and not pd.isnull(s) and not pd.isnull(t):
            pairList.append({'From': s, 'To': t})

# Get counts of from and to
counts=pd.DataFrame(pairList).groupby(['From','To']).size().reset_index(name='counts')

# Get lists of sources, targets and labels
from_=counts['From'].tolist()
to_=counts['To'].tolist()
uniqueValues = pd.unique(pd.concat((counts['From'],counts['To']),axis=0)).tolist()
labelCounts = [np.sum(counts.loc[counts['From'] == x,['counts']].sum(axis=1)) 
               for x in pd.unique(counts['From'])]
nLastNodes = len(uniqueValues) - len(labelCounts)
lastNodes = uniqueValues[-nLastNodes:]
lastLabelCounts = [np.sum(counts.loc[counts['To'] == x,['counts']].sum(axis=1)) 
               for x in lastNodes]
labelCounts += lastLabelCounts
nodeLabels = [(uv + ": " + str(vc)) for (uv, vc) in zip(uniqueValues,labelCounts)]

fromIndices = [uniqueValues.index(i) for i in from_]
toIndices = [uniqueValues.index(i) for i in to_]
colorNodes = [colorDict[x] for x in uniqueValues]
colorLinks = [colorDict[x] for x in from_]

# Create figure
fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 5,
      thickness = 30,
      line = dict(color = "black", width = 0.5),
      label = nodeLabels,
      color =  colorNodes
    ),
    # Add links
    link = dict(
      source =  fromIndices,
      target =  toIndices,
      value =  counts['counts'],
      color = colorLinks
))])

fig.update_layout(title="Job search March-May 2021", font_size=20)
plot(fig)