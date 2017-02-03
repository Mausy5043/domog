#!/bin/bash

# Pull YEARLY data from MySQL server.

######
datastore="/tmp/domog/mysql4python"

interval="INTERVAL 370 DAY "

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

pushd "$HOME/domog" >/dev/null
  # Get year data for DS18 sensor (graph21)
  # DIV t : t/100 minutes
  # t=18000 3h
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature) \
   FROM ds18 \
   WHERE (sample_time >= NOW() - $interval) \
   GROUP BY sample_time DIV 18000;" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql21w.csv"

  # Get week data for BMP183 sensor (graph23)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), \
   MIN(pressure), AVG(pressure), MAX(pressure), \
   MIN(temperature), AVG(temperature), MAX(temperature) \
   FROM bmp183 \
   WHERE (sample_time >= NOW() - $interval) \
   GROUP BY sample_time DIV 18000;" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql23w.csv"

popd >/dev/null
