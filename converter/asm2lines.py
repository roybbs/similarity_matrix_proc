#!/usr/bin/python

import re
import argparse

parser = argparse.ArgumentParser(description='Parse IDA assembly code to the format of my ngram-comparison.')
parser.add_argument('-i', dest='infile',  required=True, type=str, help='IDA assembly file (*.asm)')
parser.add_argument('-o', dest='outfile', required=True, type=str, help='Output file')

args    = parser.parse_args()
infile  = args.infile
outfile = args.outfile

in_f = open(infile, "r")
out_f = open(outfile, "w")

asms_in_func = []
for line in in_f:
  g = re.match("\t\t([a-zA-Z]+)", line)
  if g is not None:
    asms_in_func.append( g.group(1) )
    continue

  g = re.match("\s*[#;!] End of function", line)
  if g is not None:
    if len(asms_in_func) != 0:
      out_f.write(asms_in_func[0])
      for i in range(1,len(asms_in_func)):
        out_f.write(" " + asms_in_func[i])
      out_f.write("\n")
    asms_in_func = []


if len(asms_in_func) != 0:
  out_f.write(asms_in_func[0])
  for i in range(1,len(asms_in_func)):
    out_f.write(" " + asms_in_func[i])
  out_f.write("\n")
  asms_in_func = []

in_f.close()
out_f.close()

