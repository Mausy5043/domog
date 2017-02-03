#!/usr/bin/env python3

# Graphing ambient temperature data from DS18 sensor

import matplotlib
matplotlib.use("Agg")

from cmath import rect, phase               # noqa
from matplotlib.dates import strpdate2num   # noqa
import numpy as np                          # noqa
import pylab as pl                          # noqa

def bytespdate2num(fmt, encoding='utf-8'):
  # convert datestring to proper format for numpy.loadtext()
  strconverter = strpdate2num(fmt)

  def bytesconverter(b):
      s = b.decode(encoding)
      return strconverter(s)
  return bytesconverter

def makegraph():
  C = np.loadtxt('/tmp/domog/mysql/sql29.csv', delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})


if __name__ == "__main__":
  makegraph()
