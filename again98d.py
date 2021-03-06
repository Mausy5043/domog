#!/usr/bin/env python3

# daemon98.py file post-processor.

import configparser
import os
import subprocess
import sys
import syslog
import time
import traceback

from libdaemon import Daemon
from random import randrange as rnd

# constants
DEBUG       = False
IS_JOURNALD = os.path.isfile('/bin/journalctl')
MYID        = "".join(list(filter(str.isdigit, os.path.realpath(__file__).split('/')[-1])))
MYAPP       = os.path.realpath(__file__).split('/')[-2]
NODE        = os.uname()[1]
SQLMNT      = rnd(0, 59)
SQLHR       = rnd(0, 23)
SQLHRM      = rnd(0, 59)
SQL_UPDATE_HOUR   = 3   # in minutes
SQL_UPDATE_DAY    = 12  # in minutes
SQL_UPDATE_WEEK   = 4   # in hours
SQL_UPDATE_YEAR   = 8   # in hours
GRAPH_UPDATE      = 6   # in minutes

# initialise logging
syslog.openlog(ident=MYAPP, facility=syslog.LOG_LOCAL0)

class MyDaemon(Daemon):
  def run(self):
    iniconf         = configparser.ConfigParser()
    inisection      = MYID
    home            = os.path.expanduser('~')
    s               = iniconf.read(home + '/' + MYAPP + '/config.ini')
    syslog_trace("Config file   : {0}".format(s), False, DEBUG)
    syslog_trace("Options       : {0}".format(iniconf.items(inisection)), False, DEBUG)
    syslog_trace("getsqlday.sh  runs every 30 minutes starting at minute {0}".format(SQLMNT), syslog.LOG_DEBUG, DEBUG)
    syslog_trace("getsqlweek.sh runs every 4th hour  starting  at hour   {0}".format(SQLHR), syslog.LOG_DEBUG, DEBUG)
    reportTime      = iniconf.getint(inisection, "reporttime")
    samplesperCycle = iniconf.getint(inisection, "samplespercycle")
    flock           = iniconf.get(inisection, "lockfile")

    scriptname      = iniconf.get(inisection, "lftpscript")

    sampleTime      = reportTime/samplesperCycle         # time [s] between samples

    getsqldata(home, 0, 0, True)

    while True:
      try:
        startTime   = time.time()

        do_mv_data(flock, home, scriptname)

        waitTime    = sampleTime - (time.time() - startTime) - (startTime % sampleTime)
        if (waitTime > 0):
          syslog_trace("Waiting  : {0}s".format(waitTime), False, DEBUG)
          syslog_trace("................................", False, DEBUG)
          time.sleep(waitTime)
      except Exception:  # Gotta catch em all
        syslog_trace("Unexpected error in run()", syslog.LOG_CRIT, DEBUG)
        syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, DEBUG)
        raise

def do_mv_data(flock, homedir, script):
  minit = int(time.strftime('%M'))
  nowur = int(time.strftime('%H'))
  # wait for processes to finish
  unlock(flock)  # remove stale lock
  time.sleep(4)

  # Retrieve data from MySQL database
  getsqldata(homedir, minit, nowur, False)
  if (minit % GRAPH_UPDATE) == 0:
    # Graph the data
    cmnd = homedir + '/' + MYAPP + '/mkgraphs.sh'
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
    cmnd = subprocess.check_output(cmnd)
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)

    try:
      # Upload the webpage and graphs
      if os.path.isfile('/tmp/' + MYAPP + '/site/default.md'):
        write_lftp(script)
        cmnd = ['lftp', '-f', script]
        syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
        cmnd = subprocess.check_output(cmnd, timeout=20)
        syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
    except subprocess.TimeoutExpired:
      syslog_trace("***TIMEOUT***:  {0}".format(cmnd), syslog.LOG_ERR, DEBUG)
      time.sleep(17*60)             # wait 17 minutes
      pass
    except subprocess.CalledProcessError:
      syslog_trace("***ERROR***:    {0}".format(cmnd), syslog.LOG_ERR, DEBUG)
      time.sleep(17*60)             # wait 17 minutes for the router to restart.
      pass

def getsqldata(homedir, minit, nowur, nu):
  # minit = int(time.strftime('%M'))
  # nowur = int(time.strftime('%H'))
  # data of last hour is updated every 10 minutes
  if (minit % SQL_UPDATE_HOUR) == 0 or nu:
    cmnd = homedir + '/' + MYAPP + '/getsqlhour.sh'
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
    cmnd = subprocess.call(cmnd)
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
  # data of the last day is updated every 30 minutes
  if ((minit % SQL_UPDATE_DAY) == (SQLMNT % SQL_UPDATE_DAY)) or nu:
    cmnd = homedir + '/' + MYAPP + '/getsqlday.sh'
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
    cmnd = subprocess.call(cmnd)
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
  # data of the last week is updated every <SQL_UPDATE_WEEK> hours
  if ((nowur % SQL_UPDATE_WEEK) == (SQLHR % SQL_UPDATE_WEEK) and (minit == SQLHRM)) or nu:
    cmnd = homedir + '/' + MYAPP + '/getsqlweek.sh'
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
    cmnd = subprocess.call(cmnd)
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)
  # data of the last year is updated at 01:xx
  if (nowur == SQL_UPDATE_YEAR and minit == SQL_UPDATE_DAY) or nu:
    cmnd = homedir + '/' + MYAPP + '/getsqlyear.sh'
    syslog_trace("...:  {0}".format(cmnd), True, DEBUG)  # temporary logging
    cmnd = subprocess.call(cmnd)
    syslog_trace("...:  {0}".format(cmnd), False, DEBUG)

def write_lftp(script):
  with open(script, 'w') as f:
    f.write('# DO NOT EDIT\n')
    f.write('# This file is created automatically by ' + MYAPP + '\n\n')
    f.write('# lftp script\n\n')
    f.write('set cmd:fail-exit yes;\n')
    f.write('open hendrixnet.nl;\n')
    f.write('cd 03.again/;\n')
    f.write('mirror --reverse --delete --verbose=3 -c /tmp/' + MYAPP + '/site/ . ;\n')
    f.write('\n')

def lock(fname):
  open(fname, 'a').close()
  syslog_trace("!..LOCK", False, DEBUG)

def unlock(fname):
  if os.path.isfile(fname):
    os.remove(fname)
    syslog_trace("!..UNLOCK", False, DEBUG)

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
