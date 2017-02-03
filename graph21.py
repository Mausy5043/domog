#!/usr/bin/env python3

# Graphing ambient temperature data from DS18 sensor

import matplotlib as mpl
mpl.use("Agg")                              # activate Anti-Grain Geometry library

from matplotlib.dates import strpdate2num   # noqa
import matplotlib.pyplot as plt             # noqa
import numpy as nmp                         # noqa

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
  HR = nmp.loadtxt(datapath + '/' + hrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  DY = nmp.loadtxt(datapath + '/' + dydata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  WK = nmp.loadtxt(datapath + '/' + wkdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  YR = nmp.loadtxt(datapath + '/' + yrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})

  # decide if there's enough data for a graph
  # rule-of-thumb is to require more than 30 points available for the day-graph
  if len(DY) > 30:
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('volts')
    ax1.set_title('a sine wave')

    t = nmp.arange(0.0, 1.0, 0.01)
    s = nmp.sin(2*nmp.pi*t)
    line, = ax1.plot(t,
                     s,
                     color='blue',
                     lw=2)

    # Fixing random state for reproducibility
    nmp.random.seed(19680801)

    ax2 = fig.add_axes([0.15, 0.1, 0.7, 0.3])
    n, bins, patches = ax2.hist(nmp.random.randn(1000),
                                50,
                                facecolor='yellow',
                                edgecolor='yellow')
    ax2.set_xlabel('time (s)')

    plt.savefig('/tmp/domog/site/img/day21.new.png')

    pass


if __name__ == "__main__":
  # For debugging and profiling
  startTime = datetime.datetime.now()

  makegraph()

  # For debugging and profiling
  elapsed = datetime.datetime.now() - startTime
  print(" Graphing completed in %s" % (elapsed))
  print("")

  # Anatomy of a graph:
  #
  #                TITLE
  # +-------------------------------------+
  # |                                     | Y2-axis
  # |               YR                    |
  # |                                     |
  # +-------------------------------------+
  #                 MM
  # +-------------+-----------+-----------+
  # |             |           |           | Y2-axis
  # |      WK     |    DY     |    HR     |
  # |             |           |           |
  # +-------------+-----------+-----------+
  #      Wdy dd       hr:00       hh:mm
  # ^             ^           ^           ^
  # LMARG         LMPOS       MRPOS       RMARG
  # spacing:      (+0.001)    (+0.001)
  # Positions of split between graphs
  # LMARG = 0.056
  # LMPOS = 0.403
  # MRPOS = 0.75
  # RMARG = 0.96
