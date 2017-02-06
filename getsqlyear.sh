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
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY YEAR(sample_time), MONTH(sample_time), DAY(sample_time);" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql21y.csv"

  # Get data for DHT22 sensor (graph22)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
                            MIN(humidity), AVG(humidity), MAX(humidity) \
   FROM dht22 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY YEAR(sample_time), MONTH(sample_time), DAY(sample_time);" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql22y.csv"

  # Get data for BMP183 sensor (graph23)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
                            MIN(pressure), AVG(pressure), MAX(pressure) \
   FROM bmp183 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY YEAR(sample_time), MONTH(sample_time), DAY(sample_time);" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql23y.csv"

  # Get data for wind sensor (graph29)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(speed), AVG(speed), MAX(speed), \
                            MIN(direction), AVG(direction), MAX(direction) \
   FROM wind \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY YEAR(sample_time), MONTH(sample_time), DAY(sample_time);" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql29y.csv"

popd >/dev/null
