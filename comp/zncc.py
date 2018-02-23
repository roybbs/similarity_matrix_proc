#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

"""
Calculate a characteristic form images called ZNCC.
(Zero-Normalized Cross Correlation?)
"""

def zncc(img1, img2):
  num_rows = len(img1)
  num_cols = len(img1[0])

  num_of_values = num_cols * num_rows

  IT = 0
  I  = 0
  T  = 0
  II = 0
  TT = 0

  for i in range(0,num_rows):
    for j in range(0,num_cols):
      IT = IT + (img1[i][j]*img2[i][j])
      I = I + img1[i][j]
      T = T + img2[i][j]

      II = II + (img1[i][j]**2)
      TT = TT + (img2[i][j]**2)

  u = num_of_values*IT - (I*T)
  d = math.sqrt( (num_of_values*II - (I**2))*(num_of_values*TT - (T**2)))
  return u / d



