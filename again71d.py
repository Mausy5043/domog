#!/usr/bin/env python3

# daemon71d.py creates a graph.

# import datetime
import configparser
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
mpl.use("Agg", warn=True)        # activate Anti-Grain Geometry library before importing pyplot
import matplotlib.pyplot as plt  # noqa

# constants
DEBUG       = False
IS_JOURNALD = os.path.isfile('/bin/journalctl')
MYID        = "".join(list(filter(str.isdigit, os.path.realpath(__file__).split('/')[-1])))
MYAPP       = os.path.realpath(__file__).split('/')[-2]
NODE        = os.uname()[1]

def timeme(method):
    def wrapper(*args, **kw):
        starttime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endtime = int(round(time.time() * 1000))
        print(endtime - starttime, 'ms')
        return result
    return wrapper


class MyDaemon(Daemon):
  def run(self):
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
def do_main(flock, nu):
  syslog_trace("* Lock", False, DEBUG)
  lock(flock)
  # ff wachten
  time.sleep(2)
  currentminute = int(time.strftime('%M'))
  currenthour   = int(time.strftime('%H'))
  # HOUR
  # data of last hour is updated every minute
  syslog_trace("* Get new data for hour", False, DEBUG)

  # DAY
  # data of the last day is updated every 30 minutes
  if (currentminute % 30) or nu:
    syslog_trace("* Get new data for day", False, DEBUG)
    syslog_trace("* min :  {0}".format(currentminute), False, DEBUG)
  # WEEK
  # data of the last week is updated every 4 hours
  if (currenthour % 6) or nu:
    syslog_trace("* Get new data for week", False, DEBUG)
    syslog_trace("* hour:  {0}".format(currenthour), False, DEBUG)
  # YEAR
  # data of the last year is updated at 01:xx
  if (currenthour % 12) or nu:
    syslog_trace("* Get new data for year", False, DEBUG)
    syslog_trace("* hour:  {0}".format(currenthour), False, DEBUG)

  syslog_trace("* Unlock", False, DEBUG)
  unlock(flock)
  syslog_trace("* Main Loop end", False, DEBUG)

@timeme
def lock(fname):
  open(fname, 'a').close()

@timeme
def unlock(fname):
  if os.path.isfile(fname):
    os.remove(fname)

def syslog_trace(trace, logerr, out2console):
  # Log a python stack trace to syslog
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
