#!/usr/bin/env python3

# Graphing ambient temperature & humidity data from DHT22 sensor

import matplotlib as mpl
mpl.use("Agg")                              # activate Anti-Grain Geometry library

import matplotlib.pyplot as plt             # noqa
import numpy as np                          # noqa
import datetime                             # noqa

def bytespdate2num(fmt, encoding='utf-8'):
  # convert datestring to proper format for numpy.loadtext()
  strconverter = mpl.dates.strpdate2num(fmt)

  def bytesconverter(b):
      s = b.decode(encoding)
      return strconverter(s)
  return bytesconverter

def makegraph22():
  LMARG = 0.056
  # LMPOS = 0.403
  # MRPOS = 0.75
  RMARG = 0.96
  datapath = '/tmp/domog/mysql4python'
  hrdata   = 'sql22h.csv'
  dydata   = 'sql22d.csv'
  wkdata   = 'sql22w.csv'
  yrdata   = 'sql22y.csv'
  HR = np.loadtxt(datapath + '/' + hrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  DY = np.loadtxt(datapath + '/' + dydata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  WK = np.loadtxt(datapath + '/' + wkdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})
  YR = np.loadtxt(datapath + '/' + yrdata, delimiter=';', converters={0: bytespdate2num("%Y-%m-%d %H:%M:%S")})

  Ymin = min(np.nanmin(WK[:, 1], 0), np.nanmin(DY[:, 1], 0), np.nanmin(HR[:, 1], 0)) - 1
  Ymax = max(np.nanmax(WK[:, 3], 0), np.nanmax(DY[:, 3], 0), np.nanmax(HR[:, 1], 0)) + 1

  Y2min = min(np.nanmin(WK[:, 4], 0), np.nanmin(DY[:, 4], 0), np.nanmin(HR[:, 2], 0)) - 1
  Y2max = max(np.nanmax(WK[:, 6], 0), np.nanmax(DY[:, 6], 0), np.nanmax(HR[:, 2], 0)) + 1

  locatedmondays = mpl.dates.WeekdayLocator(mpl.dates.MONDAY)      # find all mondays
  locatedmonths  = mpl.dates.MonthLocator()                        # find all months
  locateddays    = mpl.dates.DayLocator()                          # find all days
  locatedhours   = mpl.dates.HourLocator()                         # find all hours
  locatedminutes = mpl.dates.MinuteLocator()                       # find all minutes

  fourhours  = (4. / 24.)
  tenminutes = (1. / 6. / 24.)

  # decide if there's enough data for a graph
  # rule-of-thumb is to require more than 30 points available for the day-graph
  if len(DY) > 30:
    plt.figure(0)
    fig = plt.gcf()
    DPI = fig.get_dpi()
    fig.set_size_inches(1280.0/float(DPI), 640.0/float(DPI))

    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)
    ax2 = plt.subplot2grid((2, 3), (1, 0))
    ax3 = plt.subplot2grid((2, 3), (1, 1))
    ax4 = plt.subplot2grid((2, 3), (1, 2))

    plt.subplots_adjust(left=LMARG, bottom=None, right=RMARG, top=None,  wspace=0.01, hspace=None)
    plt.suptitle('Humidity & Temperature DHT22 ( ' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ' )')

    # #######################
    # [YEAR]
    ax1.set_xlabel('past year')
    ax1.set_xlim([YR[1, 0], YR[-1, 0]])
    #
    t = np.array(YR[:, 0])
    ax1.set_xticklabels(t)
    ax1.xaxis.set_major_locator(locatedmonths)
    ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %Y'))
    ax1.grid(which='major', alpha=0.5)
    ax1.xaxis.set_minor_locator(locatedmondays)
    ax1.grid(which='minor', alpha=0.2)
    #
    s = np.array(YR[:, 2])
    slo = np.array(YR[:, 1])
    shi = np.array(YR[:, 3])
    u = np.array(YR[:, 5])
    ulo = np.array(YR[:, 4])
    uhi = np.array(YR[:, 6])
    #
    line01, = ax1.plot(t, s, color='red', lw=1, label='Temperature [degC]')
    ax1.fill_between(t, slo, shi, interpolate=True, color='red', alpha=0.2)
    ax1.set_ylabel('Temperature [degC]', color='red')
    ax1.tick_params('y', colors='red')

    ar1 = ax1.twinx()
    line11, = ar1.plot(t, u, color='blue', lw=1, label='Humidity [%]')
    ar1.fill_between(t, ulo, uhi, interpolate=True, color='blue', alpha=0.2)
    ar1.set_ylabel('Humidity [%]', color='blue')
    ar1.tick_params('y', colors='blue')

    ax1.legend(loc='upper left', fontsize='x-small')

    # #######################
    # [WEEK]
    minor_ticks = np.arange(np.ceil(WK[1, 0]/fourhours)*fourhours, WK[-1, 0], fourhours)
    ax2.set_xlabel('past week')
    ax2.set_ylim([Ymin, Ymax])
    ax2.set_xlim([WK[1, 0], WK[-1, 0]])
    #
    t = np.array(WK[:, 0])
    ax2.set_xticklabels(t, size='small')
    ax2.xaxis.set_major_locator(locateddays)
    ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%a %d'))
    ax2.grid(which='major', alpha=0.5)
    ax2.set_xticks(minor_ticks, minor=True)
    ax2.grid(which='minor', alpha=0.2)
    #
    s = np.array(WK[:, 2])
    slo = np.array(WK[:, 1])
    shi = np.array(WK[:, 3])
    u = np.array(WK[:, 5])
    ulo = np.array(WK[:, 4])
    uhi = np.array(WK[:, 6])
    #
    line02, = ax2.plot(t, s, linestyle='-', color='red', lw=2)
    ax2.fill_between(t, slo, shi, interpolate=True, color='red', alpha=0.2)
    ax2.set_ylabel('Temperature [degC]', color='red')
    ax2.tick_params('y', colors='red')

    ar2 = ax2.twinx()
    ar2.set_ylim([Y2min, Y2max])
    ar2.set_yticklabels([])
    line12, = ar2.plot(t, u, linestyle='-', color='blue', lw=2)
    ar2.fill_between(t, ulo, uhi, interpolate=True, color='blue', alpha=0.2)
    ar2.tick_params('y', colors='blue')

    # #######################
    # [DAY]
    major_ticks = np.arange(np.ceil(DY[1, 0]/fourhours)*fourhours, DY[-1, 0], fourhours)
    ax3.set_xlabel('past day')
    ax3.grid(True)
    ax3.set_ylim([Ymin, Ymax])
    ax3.set_xlim([DY[1, 0], DY[-1, 0]])
    #
    t = np.array(DY[:, 0])
    ax3.set_xticklabels(t, size='small')
    ax3.set_yticklabels([])
    ax3.set_xticks(major_ticks)
    ax3.xaxis.set_major_formatter(mpl.dates.DateFormatter('%R'))
    ax3.grid(which='major', alpha=0.5)
    ax3.xaxis.set_minor_locator(locatedhours)
    ax3.grid(which='minor', alpha=0.2)
    #
    s = np.array(DY[:, 2])
    slo = np.array(DY[:, 1])
    shi = np.array(DY[:, 3])
    u = np.array(DY[:, 5])
    ulo = np.array(DY[:, 4])
    uhi = np.array(DY[:, 6])
    line03, = ax3.plot(t, s, marker='.', linestyle='', color='red', lw=2)
    ax3.fill_between(t, slo, shi, interpolate=True, color='red', alpha=0.2)
    ax3.tick_params('y', colors='red')

    ar3 = ax3.twinx()
    ar3.set_ylim([Y2min, Y2max])
    ar3.set_yticklabels([])
    line13, = ar3.plot(t, u, marker='.', linestyle='', color='blue', lw=2)
    ar3.fill_between(t, ulo, uhi, interpolate=True, color='blue', alpha=0.2)
    ar3.tick_params('y', colors='blue')

    # #######################
    # AX4 [HOUR]
    major_ticks = np.arange(np.ceil(HR[1, 0]/tenminutes)*tenminutes, HR[-1, 0], tenminutes)
    ax4.set_xlabel('past hour')
    ax4.set_ylim([Ymin, Ymax])
    ax4.set_xlim([HR[1, 0], HR[-1, 0]])
    #
    t = np.array(HR[:, 0])
    ax4.set_xticklabels(t, size='small')
    ax4.set_yticklabels([])
    ax4.set_xticks(major_ticks)
    ax4.xaxis.set_major_formatter(mpl.dates.DateFormatter('%R'))
    ax4.grid(which='major', alpha=0.5)
    ax4.xaxis.set_minor_locator(locatedminutes)
    ax4.grid(which='minor', alpha=0.2)
    #
    s = np.array(HR[:, 1])
    u = np.array(HR[:, 2])
    line04, = ax4.plot(t, s, marker='.', linestyle='', color='red', lw=2)
    ax4.tick_params('y', colors='red')

    ar4 = ax4.twinx()
    ar4.set_ylim([Y2min, Y2max])
    line14, = ar4.plot(t, u, marker='.', linestyle='', color='blue', lw=2)
    ar4.set_ylabel('Humidity [%]', color='blue')
    ar4.tick_params('y', colors='blue')

    plt.savefig('/tmp/domog/site/img/day22.png', format='png')


if __name__ == "__main__":
  # For debugging and profiling
  startTime = datetime.datetime.now()
  print("")

  makegraph22()

  # For debugging and profiling
  elapsed = datetime.datetime.now() - startTime
  print(" Graphing completed in {0}".format(elapsed))
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
