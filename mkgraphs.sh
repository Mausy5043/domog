#!/bin/bash

# Graph the data.

LOCAL=$(date)
LOCALSECONDS=$(date -d "$LOCAL" +%s)
UTC=$(date -u -d "$LOCAL" +"%Y-%m-%d %H:%M:%S")  #remove timezone reference
UTCSECONDS=$(date -d "$UTC" +%s)
UTCOFFSET=$((LOCALSECONDS - UTCSECONDS))

pushd "$HOME/domog" >/dev/null
  ./graph21.py
  ./graph22.py
  ./graph23.py
  ./graph29.py
  ./graph29roos.py
popd >/dev/null
