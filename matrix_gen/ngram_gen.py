#!/usr/bin/python

from jaccard_box import get_sets, jaccard_distance
#from similarity_cosine import get_sets, cosine_similarity_ngrams
from ngram import NGram
import argparse
import sys
import string

parser = argparse.ArgumentParser(description='Conduct a n-gram-comparison.')
parser.add_argument('files', default=[], nargs='*', type=str, help='Text files that have one element per line.')
parser.add_argument('-n', dest="n_of_ngram", required=True, type=int, help='n of n-gram')
parser.add_argument('-o', dest="outfile_simmat", required=True, type=str, help='A file in which the similarity matrix is written')
parser.add_argument('-w', dest="outfile_labels", required=True, type=str, help='A file in which the IDs of input files are written')
parser.add_argument('-p', dest="outfile_pairs", required=True, type=str, help='A file in which pars of similar files are written')
parser.add_argument('-t', dest="threshold", default=0.3, type=float, help='A threathould value used to determine similar pairs')
parser.add_argument('-l', dest="listfile", default="", type=str, help='A file that lists test files that have one element per line.')

args = parser.parse_args()
files = args.files
outfile_simmat = args.outfile_simmat
outfile_labels = args.outfile_labels
outfile_pairs  = args.outfile_pairs
threshold      = args.threshold
listfile       = args.listfile
n_of_ngram = args.n_of_ngram


if listfile != "":
  files = []
  f = open( listfile, "r" )
  for line in f:
    line = line.rstrip('\r\n')
    files.append( line )
  f.close()

num_of_files = len(files)

if num_of_files < 2:
  sys.stderr.write("Error: please give more than one file to make a similarity matrix.\n")
  sys.exit(1)

def makeUniqNgrams(ngrams,src,n_of_ngram):
  buf = ["" for i in range(0,n_of_ngram)]
  num_appended_elements = 0
  index = 0

  for element in src:
    #element = element.strip('\r\n')
    #if element == "":
    #  continue

    if num_appended_elements < (n_of_ngram-1):
      buf[index] = element
      index += 1
      num_appended_elements += 1
      continue

    buf[index] = element
    index += 1
    index %= n_of_ngram

    seq = buf[index]
    for j in range(1,n_of_ngram):
      seq = seq + " " + buf[(index + j) % n_of_ngram]
    ngrams.add( seq )  

  return ngrams

def calcNgramSim(a,b):
  num_shared_ngrams = len(a.intersection(b))
  #num_all_ngrams = len(a.difference(b)) + len(b.difference(a)) + num_shared_ngrams 
  num_all_ngrams = len(list(a)) + len(list(b)) - num_shared_ngrams 
  if num_all_ngrams != 0:
    sim = NGram.ngram_similarity(num_shared_ngrams, num_all_ngrams)
  else:
    sim = 0
  return sim

def debugmsg(msg):
  sys.stderr.write(msg)

list_of_ngrams = []

list_of_files = []
debugmsg("Creating ngram objects from %d files...\n"%(num_of_files))
fw_labels = open( outfile_labels, "w")
for i,fpath in enumerate(files):
  debugmsg("Phase 1: (%d/%d)\n"%(i,num_of_files))
  list_of_files.append( fpath )
  fw_labels.write("%d,%s\n"%(i,fpath))
  f = open( fpath, "r" )
  textbody = string.join(f.readlines(),"")
  f.close()
  list_of_ngrams.append( get_sets(n_of_ngram,textbody) )
fw_labels.close()

sim_mat = [ [1 for i in range(0,num_of_files)] for j in range(0,num_of_files) ]

fw_pairs = open( outfile_pairs, "w" )
debugmsg("Calculating similarities...\n")
for i in range(0,num_of_files):
  debugmsg("Phase 2: (%d/%d)\n"%(i,num_of_files))
  for j in range(0,i):
    #debugmsg("\t...[%d/%d]\n"%(j,i))
    sim_mat[i][j] = jaccard_distance(list_of_ngrams[i], list_of_ngrams[j])
    #sim_mat[i][j] = cosine_similarity_ngrams(list_of_ngrams[i], list_of_ngrams[j])
    if sim_mat[i][j] >= threshold:
      fw_pairs.write("%f,%s,%s\n"%(sim_mat[i][j],list_of_files[i],list_of_files[j]))
fw_pairs.close()

debugmsg("Completing a similality matrices...\n")
for i in range(0,num_of_files):
  debugmsg("Phase 3: (%d/%d)\n"%(i,num_of_files))
  for j in range(i+1,num_of_files):
    sim_mat[i][j] = sim_mat[j][i]

fw_simmat = open( outfile_simmat, "w")
for row in sim_mat:
  fw_simmat.write("%f"%(row[0]))
  for i in range(1,len(row)):
    fw_simmat.write(",%f"%(row[i]))
  fw_simmat.write("\n")
fw_simmat.close()

