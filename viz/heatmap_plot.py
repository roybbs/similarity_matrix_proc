#!/usr/bin/python

import argparse
import numpy as np 
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import csv

parser = argparse.ArgumentParser()
parser.add_argument("csvfile", help="Matrix of Edit distance")
parser.add_argument("imgext", help="Extention of Image file (e.g., png and pdf)")
args = parser.parse_args()
csvfile = args.csvfile
imgext = args.imgext

index = 0
mat = []
with open( csvfile, 'rb') as cf:
  spamreader = csv.reader(cf, delimiter=',')
  for row in spamreader:
    mat.append( [] )
    for column in row:
      mat[index].append( float(column) )
    index += 1



'''
max = 0
min = -1
mat = []
for v in f:
  v = v.rstrip('\r\n')
  s = v.split(' ')
  for i, v in enumerate(s):
    s[i] = int( v )
    if s[i] > max:
      max = s[i]
    if s[i] < min or min < 0:
      min = s[i]

  mat.append( s )

for i in range(0,len(mat)):
  for j in range(0,len(mat[i])):
    mat[i][j] = (mat[i][j] - min)/((max-min)*1.0)
    mat[i][j] = 1 - mat[i][j]
'''

#ax = sns.heatmap( mat, square=True, cmap="Greys", linecolor="cyan", linewidths=0, xticklabels=15, yticklabels=15)
ax = sns.heatmap( mat, square=True, cmap="Greys", linecolor="cyan", linewidths=0, xticklabels=500, yticklabels=500)
#ax.set_xticklabels(xlabels)
ax.xaxis.set_ticks_position('top')

#plt.yticks(rotation=0)
#plt.xticks(rotation=90)

plt.yticks(rotation=0,fontsize = 11)
plt.xticks(rotation=90,fontsize = 11)

#plt.yticks(rotation=0,fontsize = 0)
#plt.xticks(rotation=90,fontsize = 0)

#plt.show(ax)
#plt.savefig("%s.eps"%csvfile, bbox_inches='tight')
plt.savefig("%s.%s"%(csvfile,imgext), bbox_inches='tight')


'''
cmap values: Colormap black is not recognized. Possible values are: Accent,
Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap,
CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd,
OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r,
Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r,
PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r,
RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r,
Set3, Set3_r, Spectral, Spectral_r, Vega10, Vega10_r, Vega20, Vega20_r,
Vega20b, Vega20b_r, Vega20c, Vega20c_r, Wistia, Wistia_r, YlGn, YlGnBu,
YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn,
autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r,
coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r,
gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r,
gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r,
gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r,
hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r,
nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r,
prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r,
spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b,
tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, winter,
winter_r
'''

