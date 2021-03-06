#!/bin/bash

# Use stop.sh to stop all daemons in one go
# You can use update.sh to get everything started again.

pushd "${HOME}/domog"
  source ./includes

  # Check if SVC daemons are running
  for daemon in $srvclist; do
    # command the daemon to stop regardless if it is running or not.
    eval "./again${daemon}d.py stop"
    # kill off any rogue daemons by the same name (it happens sometimes)
    if [ "$(pgrep -fc again${daemon}d.py)" -ne 0 ]; then
      kill "$(pgrep -f again${daemon}d.py)"
    fi
    # log the activity
    logger -p user.err -t domog "  * Daemon ${daemon} Stopped."
    # force rm the .pid file
    rm -f "/tmp/domog/${daemon}.pid"
  done
popd

echo
echo "To re-start all daemons, use:"
echo "./update.sh"
