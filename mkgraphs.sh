#!/bin/bash

# Graph the data.

LOCAL=$(date)
LOCALSECONDS=$(date -d "$LOCAL" +%s)
UTC=$(date -u -d "$LOCAL" +"%Y-%m-%d %H:%M:%S")  #remove timezone reference
UTCSECONDS=$(date -d "$UTC" +%s)
UTCOFFSET=$((LOCALSECONDS - UTCSECONDS))

./graph21.py
./graph22.py
./graph23.py
./graph29.py

pushd "$HOME/domog" >/dev/null
  #if [ $(wc -l < /tmp/domog/mysql/sql21d.csv) -gt 30 ]; then
    # time gnuplot -e "utc_offset='${UTCOFFSET}'" ./graph21.gp
  #fi
  #if [ $(wc -l < /tmp/domog/mysql/sql22d.csv) -gt 30 ]; then
    # time gnuplot -e "utc_offset='${UTCOFFSET}'" ./graph22.gp
  #fi
  #if [ $(wc -l < /tmp/domog/mysql/sql23d.csv) -gt 30 ]; then
    # time gnuplot -e "utc_offset='${UTCOFFSET}'" ./graph23.gp
  #fi

  if [ $(wc -l < /tmp/domog/mysql/sql29.csv) -gt 30 ]; then
    # time gnuplot -e "utc_offset='${UTCOFFSET}'" ./graph29.gp
    time ./graph29roos.py
    chmod 644 /tmp/domog/site/img/day29roos.png
    chmod 644 /tmp/domog/site/img/day29.png
  fi
popd >/dev/null
