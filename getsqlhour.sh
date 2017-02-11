#!/bin/bash

# Pull HOURLY data from MySQL server.

interval="INTERVAL 70 MINUTE "
host=$(hostname)

pushd "$HOME/domog" >/dev/null
  datastore="/tmp/domog/mysql4python"

  if [ ! -d "${datastore}" ]; then
    mkdir -p "${datastore}"
  fi

  # Get hour data for DS18 sensor (graph21)
  divider=60
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), AVG(temperature) \
   FROM ds18 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql21h.csv"

  # Get data for DHT22 sensor (graph22)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), AVG(temperature), AVG(humidity) \
   FROM dht22 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql22h.csv"

  # Get data for BMP183 sensor (graph23)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), AVG(temperature), AVG(pressure) \
   FROM bmp183 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql23h.csv"

  # Get data for wind sensor (graph29)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), AVG(speed), AVG(direction) \
   FROM wind \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql29h.csv"

  # Get data for windroos (graph29roos)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT sample_time, speed, direction \
   FROM wind \
   WHERE (sample_time >= NOW() - INTERVAL 50 HOUR);" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql29roos.csv"

popd >/dev/null
