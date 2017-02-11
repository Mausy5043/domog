#!/bin/bash

# this repo gets installed either manually by the user or automatically by
# a `*boot` repo.

# The hostname is in /etc/hostname prior to running `install.sh` here!
HOSTNAME=$(hostname)

echo -n "Started UNinstalling domog on "; date

pushd "${HOME}/domog"
  source ./includes

  if [ -e /etc/cron.d/domog ]; then
    sudo rm /etc/cron.d/domog
  fi

  echo "  Stopping all service daemons"
  for daemon in $srvclist; do
    echo "Stopping ${daemon}"
    eval "./again${daemon}d.py stop"
  done
popd

echo -n "Finished UNinstallation of domog on "; date
