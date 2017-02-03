#!/usr/bin/env python3

# Graphing ambient temperature data from DS18 sensor

import matplotlib
matplotlib.use("Agg")

from cmath import rect, phase               # noqa
from matplotlib.dates import strpdate2num   # noqa
import numpy as np                          # noqa
import pylab as pl                          # noqa

# following import is for debugging and profiling
import datetime                             # noqa

def bytespdate2num(fmt, encoding='utf-8'):
  # convert datestring to proper format for numpy.loadtext()
  strconverter = strpdate2num(fmt)

  def bytesconverter(b):
      s = b.decode(encoding)
      return strconverter(s)
  return bytesconverter

def makegraph():
  datapath = '/tmp/domog/mysql4python'
  hrdata   = 'sql21h.csv'
  dydata   = 'sql21d.csv'
  wkdata   = 'sql21w.csv'
  yrdata   = 'sql21y.csv'
  HR = np.loadtxt(datapath + '/' + hrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  DY = np.loadtxt(datapath + '/' + dydata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  WK = np.loadtxt(datapath + '/' + wkdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  YR = np.loadtxt(datapath + '/' + yrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})


if __name__ == "__main__":

  # For debugging and profiling
  startTime = datetime.datetime.now()

  makegraph()

  # For debugging and profiling
  elapsed = datetime.datetime.now() - startTime
  print " Graphing completed in %s" % (elapsed)
  print ""
