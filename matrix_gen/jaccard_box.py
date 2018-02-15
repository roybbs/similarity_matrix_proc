import re
from itertools import chain
import nltk
from nltk.util import ngrams # This is the ngram magic.

re_sent_ends_naive = re.compile(r'[.\n]')
re_stripper_alpha = re.compile('[^a-zA-Z]+')
re_stripper_naive = re.compile('[^a-zA-Z\.\n]')

splitter_naive = lambda x: re_sent_ends_naive.split(re_stripper_naive.sub(' ', x))

def get_sets(N,txt):
    if not txt: return None
    sentences = (x.split() for x in splitter_naive(txt) if x)
    ng = (ngrams(x, N) for x in sentences if len(x) >= N)
    return set(list(chain(*ng)))

def jaccard_distance(a, b):
# a and b are sets.
    if len(a|b) != 0:
      return 1.0 * len(a&b)/len(a|b)
    else:
      return 0.0

