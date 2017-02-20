#!/usr/bin/env python3

# daemon71d.py creates a graph.

import configparser
import datetime
import MySQLdb as mdb
import os
# import platform
# import shutil
import sys
import syslog
import time
import traceback

from libdaemon import Daemon

# import numpy as np
import matplotlib as mpl
mpl.use("Agg", warn=True)         # activate Anti-Grain Geometry library before importing pyplot
import matplotlib.pyplot as plt   #noqa

# constants
PLOT_TITLE      = "Temperature DS18B20"
PLOT_Y1LABEL    = "Temperature [degC]"
PLOT_Y2LABEL    = ""

DEBUG           = False
IS_JOURNALD     = os.path.isfile('/bin/journalctl')
MYID            = "".join(list(filter(str.isdigit, os.path.realpath(__file__).split('/')[-1])))
MYAPP           = os.path.realpath(__file__).split('/')[-2]
NODE            = os.uname()[1]

LOCATEDMONDAYS  = mpl.dates.WeekdayLocator(mpl.dates.MONDAY)      # find all mondays
LOCATEDMONTHS   = mpl.dates.MonthLocator()                        # find all months
LOCATEDDAYS     = mpl.dates.DayLocator()                          # find all days
LOCATEDHOURS    = mpl.dates.HourLocator()                         # find all hours
LOCATEDMINUTES  = mpl.dates.MinuteLocator()                       # find all minutes


def timeme(method):
  """
  Execution timer.
  Used as decoration to determine execution time of functions.
  For profiling and debugging purposes.
  """
  def wrapper(*args, **kw):
      starttime = int(round(time.time() * 1000))
      result = method(*args, **kw)
      endtime = int(round(time.time() * 1000))
      print(endtime - starttime, 'ms')
      return result
  return wrapper


class MyDaemon(Daemon):
  """Definition of daemon."""
  def run(self):
    """Overload definition of run."""
    iniconf         = configparser.ConfigParser()
    inisection      = MYID
    home            = os.path.expanduser('~')
    s               = iniconf.read(home + '/' + MYAPP + '/config.ini')
    syslog_trace("Config file   : {0}".format(s), False, DEBUG)
    syslog_trace("Options       : {0}".format(iniconf.items(inisection)), False, DEBUG)
    reportTime      = iniconf.getint(inisection, "reporttime")
    samplesperCycle = iniconf.getint(inisection, "samplespercycle")
    flock           = iniconf.get(inisection, "lockfile")
    sampleTime      = reportTime/samplesperCycle        # time [s] between samples

    init_axes()
    do_main(flock, True)  # get all data and graphs on start-up

    while True:
      try:
        startTime   = time.time()

        do_main(flock, False)

        waitTime    = sampleTime - (time.time() - startTime) - (startTime % sampleTime)
        if (waitTime > 0):
          syslog_trace("Waiting  : {0}s".format(waitTime), False, DEBUG)
          syslog_trace("................................", False, DEBUG)
          time.sleep(waitTime)
      except Exception:  # Gotta catch em all
        syslog_trace("Unexpected error in run()", syslog.LOG_CRIT, DEBUG)
        syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, DEBUG)
        raise


@timeme
def total_hour_query():
  """Query the database to get the data for the past hour"""
  syslog_trace("* Get data for past hour", False, DEBUG)

@timeme
def total_day_query():
  """Query the database to get the data for the past day"""
  syslog_trace("* Get data for past day", False, DEBUG)

@timeme
def total_week_query():
  """Query the database to get the data for the past week"""
  syslog_trace("* Get data for past week", False, DEBUG)

@timeme
def total_year_query():
  """Query the database to get the data for the past year"""
  syslog_trace("* Get data for past year", False, DEBUG)

@timeme
def update_hour_query():
  """Query the database and update the data for the past hour"""
  syslog_trace("* Get update for past hour", False, DEBUG)

@timeme
def update_day_query():
  """Query the database and update the data for the past day"""
  syslog_trace("* Get update for past day", False, DEBUG)

@timeme
def update_week_query():
  """Query the database and update the data for the past week"""
  syslog_trace("* Get update for past week", False, DEBUG)

@timeme
def update_year_query():
  """Query the database and update the data for the past year"""
  syslog_trace("* Get update for year hour", False, DEBUG)

@timeme
def update_hour_graph():
  """(Re)draw the axes of the hour graph"""
  syslog_trace("* (Re)draw graph for past hour", False, DEBUG)

@timeme
def update_day_graph():
  """(Re)draw the axes of the day graph"""
  syslog_trace("* (Re)draw graph for past day", False, DEBUG)

@timeme
def update_week_graph():
  """(Re)draw the axes of the week graph"""
  syslog_trace("* (Re)draw graph for past week", False, DEBUG)

@timeme
def update_year_graph():
  """(Re)draw the axes of the year graph"""
  syslog_trace("* (Re)draw graph for year hour", False, DEBUG)


@timeme
def do_main(flock, nu):
  """Main loop: Calls the various subroutines when needed."""
  syslog_trace("* Lock", False, DEBUG)
  lock(flock)
  currentminute = int(time.strftime('%M'))
  currenthour   = int(time.strftime('%H'))

  # HOUR
  # data of last hour is updated every minute
  if nu:
    total_hour_query()
  else:
    update_hour_query()
  update_hour_graph()

  # DAY
  # data of the last day is updated every 30 minutes
  if (currentminute % 30) == 0 or nu:
    syslog_trace("* Get new data for day", False, DEBUG)
    syslog_trace("* min :  {0}".format(currentminute), False, DEBUG)
    if nu:
      total_day_query
    else:
      update_day_query
    update_day_graph()

  # WEEK
  # data of the last week is updated every 4 hours
  if (currenthour % 6) == 0 and (currentminute == 1) or nu:
    syslog_trace("* Get new data for week", False, DEBUG)
    syslog_trace("* hour:  {0}".format(currenthour), False, DEBUG)
    if nu:
      total_week_query
    else:
      update_week_query
    update_week_graph()

  # YEAR
  # data of the last year is updated at 01:11
  if (currenthour == 1) and (currentminute == 11) or nu:
    syslog_trace("* Get new data for year", False, DEBUG)
    syslog_trace("* hour:  {0}".format(currenthour), False, DEBUG)
    if nu:
      total_year_query
    else:
      update_year_query
    update_year_graph()


  plt.savefig('/tmp/domog/site/img/day71.png', format='png')
  syslog_trace("* Unlock", False, DEBUG)
  unlock(flock)
  syslog_trace("* Main Loop end", False, DEBUG)

@timeme
def init_axes():
  """Initialise the figure and its axes."""
  global FIG
  global AX1
  global AX2
  global AX3
  global AX4

  LMARG = 0.056
  # LMPOS = 0.403
  # MRPOS = 0.75
  RMARG = 0.96
  plt.figure(0)
  FIG = plt.gcf()
  DPI = FIG.get_dpi()
  FIG.set_size_inches(1280.0/float(DPI), 640.0/float(DPI))

  # configure the figure
  plt.subplots_adjust(left=LMARG, bottom=None, right=RMARG, top=None,  wspace=0.01, hspace=None)
  plt.suptitle(PLOT_TITLE + ' ( ' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ' )')

  # figure contains three axes:
  # two rows by three columns
  # top row: YEAR                 full width
  # btm row: WEEK - DAY - HOUR    each 1/3rd of the width
  AX1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)
  AX2 = plt.subplot2grid((2, 3), (1, 0))
  AX3 = plt.subplot2grid((2, 3), (1, 1))
  AX4 = plt.subplot2grid((2, 3), (1, 2))

  # #######################
  # AX1 = [YEAR]
  AX1.set_ylabel(PLOT_Y1LABEL)
  AX1.set_xlabel('past year')
  AX1.grid(True)
  # AX1.xaxis.set_major_locator(LOCATEDMONTHS)
  # AX1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %Y'))
  # AX1.grid(which='major', alpha=0.5)
  # AX1.xaxis.set_minor_locator(LOCATEDMONDAYS)
  # AX1.grid(which='minor', alpha=0.2)
  # AX1.legend(loc='upper left', fontsize='x-small')

  # #######################
  # AX2 = [WEEK]
  AX2.set_ylabel(PLOT_Y1LABEL)
  AX2.set_xlabel('past week')
  AX2.grid(True)
  # AX2.xaxis.set_major_locator(LOCATEDDAYS)
  # AX2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%a %d'))
  # AX2.grid(which='major', alpha=0.5)
  # AX2.grid(which='minor', alpha=0.2)

  # #######################
  # AX3 = [DAY]
  AX3.set_xlabel('past day')
  AX3.set_yticklabels([])
  AX3.grid(True)
  # AX3.xaxis.set_major_formatter(mpl.dates.DateFormatter('%R'))
  # AX3.grid(which='major', alpha=0.5)
  # AX3.xaxis.set_minor_locator(LOCATEDHOURS)
  # AX3.grid(which='minor', alpha=0.2)

  # #######################
  # AX4 = [HOUR]
  AX4.set_xlabel('past hour')
  AX4.set_yticklabels([])
  AX4.grid(True)
  # AX4.xaxis.set_major_formatter(mpl.dates.DateFormatter('%R'))
  # AX4.grid(which='major', alpha=0.5)
  # AX4.xaxis.set_minor_locator(LOCATEDMINUTES)
  # AX4.grid(which='minor', alpha=0.2)

def lock(fname):
  """Create a lockfile."""
  open(fname, 'a').close()

def unlock(fname):
  """Remove the lockfile."""
  if os.path.isfile(fname):
    os.remove(fname)

def syslog_trace(trace, logerr, out2console):
  """Log a python stack trace to syslog."""
  log_lines = trace.split('\n')
  for line in log_lines:
    if line and logerr:
      syslog.syslog(logerr, line)
    if line and out2console:
      print(line)


if __name__ == "__main__":
  daemon = MyDaemon('/tmp/' + MYAPP + '/' + MYID + '.pid')

  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    elif 'foreground' == sys.argv[1]:
      # assist with debugging.
      print("Debug-mode started. Use <Ctrl>+C to stop.")
      DEBUG = True
      syslog_trace("Daemon logging is ON", syslog.LOG_DEBUG, DEBUG)
      daemon.run()
    else:
      print("Unknown command")
      sys.exit(2)
    sys.exit(0)
  else:
    print("usage: {0!s} start|stop|restart|foreground".format(sys.argv[0]))
    sys.exit(2)
