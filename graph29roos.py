#!/usr/bin/env python3

# Graphing windroos from Gilze-Rijen weatherstation data

import matplotlib
matplotlib.use("Agg")

from cmath import rect, phase               # noqa
from matplotlib.dates import strpdate2num   # noqa
import numpy as nmp                         # noqa

import matplotlib.pyplot as plt             # noqa
# following import is for debugging and profiling
import datetime                             # noqa

def kmh(ms):
  return nmp.multiply(ms, 3.6)

def d2r(deg):
  mlt = (1/360.) * nmp.pi * 2.
  return nmp.multiply(deg, mlt)

def bytespdate2num(fmt, encoding='utf-8'):
    # convert datestring to proper format for numpy.loadtext()
    strconverter = strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def makegraph29roos():
  datapath = '/tmp/domog/mysql4python'
  roosdata   = 'sql29roos.csv'
  C = nmp.loadtxt(datapath + '/' + roosdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})

  Wspd = kmh(nmp.array(C[:, 1]))                 # windspeeds
  Wdir = d2r(nmp.array(C[:, 2]))                 # windvector

  hrsmpls = 60                              # data contains this number of samples per hour
                                            # the graph will show one slice per hour  # noqa
  lenWdir = len(Wdir)
  last14  = Wdir[lenWdir - 1]
  last13  = Wspd[lenWdir - 1]
  # create intermediate arrays
  B13 = Wspd
  B14 = Wdir
  # make the array-lengths a multiple of <hrsmpls>
  for x in range(hrsmpls - lenWdir % hrsmpls):
    B13 = nmp.append(B13, last13)
    B14 = nmp.append(B14, last14)

  # Determine average speed and direction per 1-hour-period.
  radii = theta = width = nmp.array([])
  for x in range(0, lenWdir - 1, hrsmpls):
    radii = nmp.append(radii, nmp.mean(B13[x:x+5]))

    # Averaging of the bearings as per:
    # http://rosettacode.org/wiki/Averages/Mean_angle
    avg_theta = phase(sum(rect(1, d) for d in B14[x:x+hrsmpls-1])/hrsmpls)
    if (avg_theta < 0):
      avg_theta = avg_theta + (2 * nmp.pi)
    theta = nmp.append(theta, avg_theta)
    w = (nmp.pi - abs(nmp.max(B14[x:x+hrsmpls-1]) - nmp.min(B14[x:x+hrsmpls-1]) - nmp.pi))
    width = nmp.append(width, w)

  ahpla = 0.3

  plt.figure(0)
  fig = plt.gcf()
  DPI = fig.get_dpi()
  fig.set_size_inches(640.0/float(DPI), 640.0/float(DPI))

  # bar plot on a polar axis.
  # number of datapoints to show
  N = len(radii)
  ax = plt.subplot(111, polar=True)
  # 0deg position at the top
  ax.set_theta_zero_location("N")
  # 90deg position to the right; show compass bearings
  ax.set_theta_direction(-1)
  bars = ax.bar(theta, radii, width=width, bottom=0.0)
  # Use custom colors and opacity
  for r, bar in zip(list(range(N)), bars):
    bar.set_facecolor(plt.cm.hot((r / float(N))))
    bar.set_alpha(ahpla)
  # highlight the last bar (most recent value) by giving it a different color
  bar.set_facecolor(plt.cm.cool(1.))
  bar.set_alpha(1.)

  # plt.title('Windroos')

  plt.suptitle('Windroos [Gilze-Rijen] ( ' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ' )')
  plt.savefig('/tmp/domog/site/img/day29roos.png')


if __name__ == "__main__":

  makegraph29roos()
