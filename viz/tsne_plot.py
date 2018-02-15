#!/usr/bin/python

import numpy as np
from skdata.mnist.views import OfficialImageClassification
from matplotlib import pyplot as plt
from tsne import bh_sne
import operator
import argparse
from sklearn.preprocessing import normalize
import sys
import re


labels = {
"unknown" : 0,
"mirai" : 1,
"bashlite" : 2,
"hajime" : 3,
"satori" : 4,
"suspicious" : 5,
"tsunami" : 6,
"virus" : 7,
#"trojanddos" : 8,
}

label_keys = []
array_tmp = sorted(labels.items(), key=operator.itemgetter(1))
for i in array_tmp:
  label_keys.append( i[0] )

'''
color = [
  'gray',
  'red',
  'green',
  'blue',
  'violet',
  'orange',
  'cyan',
  'gold',
  'black',
]
'''

color = [
  'red',
  'blue',
  'green',
  'yellow',
  'violet',
  'orange',
  'cyan',
  'gold',
  'black',
]

marker = [
  '+',
  'o',
  '^',
  's',
  'x',
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
]

  
parser = argparse.ArgumentParser(description="Plot a similarity matrix with TSNE")
parser.add_argument('infile_simmat', type=str, help="An input file of similarity matrix")
parser.add_argument('infile_name_csv', type=str, help="An input file of sample names")
parser.add_argument('-s', dest='showfig', action='store_true', help="A flag if a figure is shown or not")
args = parser.parse_args()
infile_simmat =  args.infile_simmat
infile_name_csv =  args.infile_name_csv
showfig = args.showfig

# load up data
#data = OfficialImageClassification(x_dtype="float32")
#x_data = data.all_images
#y_data = data.all_labels

# convert image data to float64 matrix. float64 is need for bh_sne
#x_data = np.asarray(x_data).astype('float64')
#x_data = x_data.reshape((x_data.shape[0], -1))

# For speed of computation, only run on a subset
#n = 200
#x_data = x_data[:n]
#y_data = y_data[:n]

f_sim = open( infile_simmat, "r")
x_data = []
for i in f_sim:
  i = i.rstrip('\r\n')
  s = i.split(',')
  tmp = []
  for j in s:
    tmp.append( float( j ) )

    # Jaccard distance calculated by 1 - float
    #tmp.append( 1 - float( j ) )

  x_data.append( tmp )
f_sim.close()

#
# Normalization
#
#x_data = normalize(x_data, axis=0)

f_label = open( infile_name_csv, "r")
y_data = []
malname = []
for i in f_label:
  i = i.rstrip('\r\n')
  s = i.split(',')

  if len(s) == 2:
    key = s[1]
    malname.append( s[0] )
  else:
    key = ""
    malname.append( s[0] )

  if labels.has_key( key ):
    y_data.append( int(labels[key]) )
  else:
    y_data.append( 0 )
f_label.close()

x_data = np.array(x_data)
y_data = np.array(y_data)

# perform t-SNE embedding
vis_data = bh_sne(x_data)

# plot the result
vis_x = vis_data[:, 0]
vis_y = vis_data[:, 1]

mark_x = [ [] for i in range(0,len(labels)) ]
mark_y = [ [] for i in range(0,len(labels)) ]
for i in range(0,len(y_data)):
  mark_x[ y_data[i] ].append( vis_x[i] )
  mark_y[ y_data[i] ].append( vis_y[i] )


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for i in range(0,len(labels)):
  if len(mark_x[ i ]) != 0:
    ax.scatter(mark_x[i],mark_y[i], c=color[i], marker=marker[i], label="%s"%(label_keys[i]), s=20)
    print "i=%d, len(mark_x[%d])=%d"%(i,i,len(mark_x[i]))
  else:
    print "%d: none"%(i)

#ax.scatter(x2,y2, c='blue',marker='o', label='group2')
#ax.scatter(x3,y3, c='green',marker='^', label='group3')
#ax.scatter(x4,y4, c='yellow',marker='s', label='group4')

#ax.set_title('fourth scatter plot')
#ax.set_xlabel('x')
#ax.set_ylabel('y')

#ax.xaxis.set_ticklabels([])
#ax.yaxis.set_ticklabels([])

ax.grid(True)

#ax.legend(loc='upper left')
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01),
ax.legend(loc='upper center',  bbox_to_anchor=(0.5, 1.16), fancybox=True, shadow=False, ncol=4)
#ax.legend(loc='upper center',  bbox_to_anchor=(0.5, 0), fancybox=True, shadow=False, ncol=4)

'''
for i in range(0,len(vis_x)):
  #ax.annotate("%d"%i, xy=(vis_x[i], vis_y[i]), arrowprops=dict(facecolor='black', shrink=0.05))
  if y_data[i] == 0:
    ax.annotate("%d"%i, xy=(vis_x[i], vis_y[i]), xytext=(vis_x[i]+2, vis_y[i]+2))
'''


def submit(id):
  if id < len(malname):
    ax.annotate("%d"%id, xy=(vis_x[id], vis_y[id]))
    ax.set_title('%d,%s'%(id,malname[id]))
    fig.canvas.draw()


def onclick(event):
  idx = 0
  margine = 0.03
  last_idx = -1
  global input_flag

  #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %('double' if event.dblclick else 'single', event.button, event.x, event.y, event.xdata, event.ydata))

  if event.dblclick:
    for idx in range(0,len(x_data[idx])):
      #print vis_x[idx], vis_y[idx]
      if ((vis_x[idx] - margine <= event.xdata) and (event.xdata <= vis_x[idx] + margine)) and ((vis_y[idx] - margine <= event.ydata) and (event.ydata <= vis_y[idx] + margine)):
        ax.annotate("%d"%idx, xy=(vis_x[idx], vis_y[idx]))
        last_idx = idx
    if ( last_idx != -1 ):
      #ax.set_title('%d,%s'%(last_idx,malname[last_idx]))
      ax.set_xlabel('ID=%d,HASH=%s'%(last_idx,malname[last_idx]))
    fig.canvas.draw()
  else:
    if input_flag != 1:
      input_flag = 1
      sys.stdout.write("Input sample ID: ")
      str = raw_input()
      if len(str) != 0:
        if re.search("[^0-9]", str) is None:
          sampleid = int(str)
          submit( sampleid )
      input_flag = 0

input_flag = 0
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.tick_params(axis='both', bottom='off', top='off', right='off', left='off')

figfile = re.sub('\.\w*$', ".eps", infile_simmat)
if figfile == infile_simmat:
  figfile = figfile + ".eps"
plt.savefig(figfile)

if showfig:
  fig.show()

#plt.scatter(vis_x, vis_y, c=y_data, cmap=plt.cm.get_cmap("jet", 10))
#plt.scatter(vis_x, vis_y, s=5, c=y_data)
#plt.colorbar(ticks=range(10))
#plt.colorbar()
#plt.clim(-0.5, 9.5)
#plt.xticks([])
#plt.yticks([])
if showfig:
  plt.show()

