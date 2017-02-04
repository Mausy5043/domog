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
  LMARG = 0.056
  LMPOS = 0.403
  MRPOS = 0.75
  RMARG = 0.96
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
    plt.figure(0)
    ax1 = plt.subplot2grid((3,3), (0,0), colspan=3)
    ax2 = plt.subplot2grid((3,3), (1,0), colspan=2)
    ax3 = plt.subplot2grid((3,3), (1, 2), rowspan=2)
    ax4 = plt.subplot2grid((3,3), (2, 0))
    ax5 = plt.subplot2grid((3,3), (2, 1))

    plt.suptitle("subplot2grid")

    #
    # fig = plt.figure()
    # fig.subplots_adjust(top=0.9, bottom=0.1, left=LMARG, right=RMARG)
    # # AX1
    # ax1 = fig.add_subplot(231)
    # ax1.set_ylabel('volts')
    # ax1.set_title('a sine wave')
    #
    # t = nmp.arange(0.0, 10.0, 0.01)
    # s = nmp.sin(2*nmp.pi*t) * nmp.random.randn()
    # line, = ax1.plot(t,
    #                  s,
    #                  color='blue',
    #                  lw=1)
    #
    # # AX2
    # ax2 = fig.add_subplot(234)
    # ax2.set_ylabel('volts')
    # ax2.set_title('a sine wave')
    #
    # t = nmp.arange(0.0, 1.0, 0.01)
    # s = nmp.sin(2*nmp.pi*t)
    # line, = ax2.plot(t,
    #                  s,
    #                  color='blue',
    #                  lw=2)
    #
    # # AX3
    # ax3 = fig.add_subplot(235)
    # ax3.set_ylabel('volts')
    # ax3.set_title('a sine wave')
    #
    # t = nmp.arange(0.0, 1.0, 0.01)
    # s = nmp.sin(2*nmp.pi*t)
    # line, = ax3.plot(t,
    #                  s,
    #                  color='red',
    #                  lw=3)
    #
    # # AX4
    # ax4 = fig.add_subplot(236)
    # ax4.set_ylabel('volts')
    # ax4.set_title('a sine wave')
    #
    # t = nmp.arange(0.0, 1.0, 0.01)
    # s = nmp.sin(2*nmp.pi*t)
    # line, = ax4.plot(t,
    #                  s,
    #                  color='green',
    #                  lw=4)

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
