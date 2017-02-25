#!/bin/bash

# Pull DAILY data from MySQL server.

interval="INTERVAL 25 HOUR "
host=$(hostname)

pushd "$HOME/domog" >/dev/null
  datastore="/tmp/domog/mysql4python"

  if [ ! -d "${datastore}" ]; then
    mkdir -p "${datastore}"
  fi

  # Get day data for DS18 sensor (graph21)
  divider=1800
  # mysql -h sql.lan --skip-column-names -e \
  # "USE domotica; \
  #  SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature) \
  #  FROM ds18 \
  #  WHERE (sample_time >= NOW() - ${interval}) \
  #  GROUP BY (sample_epoch DIV ${divider});" \
  # | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql21d.csv"

  # Get data for DHT22 sensor (graph22)
  # mysql -h sql.lan --skip-column-names -e \
  # "USE domotica; \
  #  SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
  #                           MIN(humidity), AVG(humidity), MAX(humidity) \
  #  FROM dht22 \
  #  WHERE (sample_time >= NOW() - ${interval}) \
  #  GROUP BY (sample_epoch DIV ${divider});" \
  # | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql22d.csv"

  # Get data for BMP183 sensor (graph23)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
                            MIN(pressure), AVG(pressure), MAX(pressure) \
   FROM bmp183 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql23d.csv"

  # Get data for wind sensor (graph29)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(speed), AVG(speed), MAX(speed), \
                            MIN(direction), AVG(direction), MAX(direction) \
   FROM wind \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_epoch DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql29d.csv"

popd >/dev/null
