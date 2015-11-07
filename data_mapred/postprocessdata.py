#!/usr/bin/python

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.plotly as py 
import plotly.graph_objs as go

datafile = "adr3.txt"
with open(datafile) as f:
    content = f.readlines()
content = np.array(content)
df_x = content[::2]
df_y = content[1::2]
df_x = [int(x) for x in df_x]

df = pd.DataFrame(columns=['prec','recall','fscore'])
for line in df_y:
    linearray = line.strip().split(' ')
    df = df.append({'prec': float(linearray[0]),
                    'recall': float(linearray[1]),
                    'fscore': float(linearray[2])}, ignore_index=True)
print df['prec'].mean(), df['recall'].mean(), df['fscore'].mean()

#plt.plot(gbr_x, df_gbr['prec'])
#plt.show()

'''
Output: 
gbr without latlong: 0.821347106469 0.667813375492 0.696495815541
gbr: 0.821347106469 0.667813375492 0.696495815541
gbr2: 0.808857298115 0.655769445635 0.684843682443
bnn: 0.450703354717 0.503172235156 0.449295656394
adr: 0.244861048315 0.293190211695 0.203692208222
tree: 0.832181097698 0.809044246021 0.800413977589
adr3: 0.251405292988 0.274110786846 0.125927099725
'''