#!/bin/bash

# Graph the weatherdata.

# temporary directory
tmp=/tmp/domog
# semaphores
plot21=$tmp/21.plot
plot22=$tmp/22.plot
plot23=$tmp/23.plot
plot29=$tmp/29.plot
plot29r=$tmp/29r.plot

cd "$HOME/domog"
if [ ! -f ${plot21} ]; then
  echo ${plot21}
  ./graph21.py
  touch ${plot21}
  exit 0
fi
if [ ! -f ${plot22} ]; then
  echo ${plot22}
  ./graph22.py
  touch ${plot22}
  exit 0
fi
if [ ! -f ${plot23} ]; then
  echo ${plot23}
  ./graph23.py
  touch ${plot23}
  exit 0
fi
if [ ! -f ${plot29} ]; then
  echo ${plot29}
  ./graph29.py
  touch ${plot29}
  exit 0
fi
if [ ! -f ${plot29r} ]; then
  echo ${plot29r}
  ./graph29roos.py
  touch ${plot29r}
  rm ${plot21}
  rm ${plot22}
  rm ${plot23}
  rm ${plot29}
  rm ${plot29r}
fi
