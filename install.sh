#!/bin/bash

# this repo gets installed either manually by the user or automatically by
# a `*boot` repo.

ME=$(whoami)

echo -n "Started installing domog on "; date
minit=$(echo $RANDOM/555 |bc)
echo "MINIT = $minit"

install_package()
{
  # See if packages are installed and install them.
  package=$1
  status=$(dpkg-query -W -f='${Status} ${Version}\n' $package 2>/dev/null | wc -l)
  if [ "$status" -eq 0 ]; then
    sudo apt-get -yuV install $package
  fi
}

sudo apt-get update
# LFTP package
install_package "lftp"

# Python 3 package and associates
install_package "python3"
install_package "build-essential"
install_package "python3-dev"
install_package "python3-pip"
install_package "python3-numpy"
install_package "python3-matplotlib"

# gnuPlot packages
#install_package "python-numpy"
install_package "gnuplot"
install_package "gnuplot-nox"

# MySQL support
install_package "mysql-client"
install_package "libmysqlclient-dev"

pushd "$HOME/domog"
  # To suppress git detecting changes by chmod:
  git config core.fileMode false
  # set the branch
  if [ ! -e "$HOME/.domog.branch" ]; then
    echo "v4" > "$HOME/.domog.branch"
  fi

  # Create the /etc/cron.d directory if it doesn't exist
  sudo mkdir -p /etc/cron.d
  # Set up some cronjobs
  echo "# m h dom mon dow user  command" | sudo tee /etc/cron.d/domog
  # echo "$minit  * *   *   *   $ME    $HOME/domog/update.sh 2>&1 | logger -p info -t domog" | sudo tee --append /etc/cron.d/domog
  # after a reboot we allow for 120s for the network to come up:
  echo "@reboot               $ME    sleep 180; $HOME/domog/update.sh 2>&1 | logger -p info -t domog" | sudo tee --append /etc/cron.d/domog
popd

echo -n "Finished installation of domog on "; date
