#!/bin/bash

# Pull HOURLY data from MySQL server.

datastore="/tmp/domog/mysql"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

interval="INTERVAL 70 MINUTE "
host=$(hostname)

pushd "$HOME/domog" >/dev/null
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM ds18 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21h.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM dht22 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql22h.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM bmp183 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql23h.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM wind where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql29h.csv"

  #http://www.sitepoint.com/understanding-sql-joins-mysql-database/
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT ds18.sample_time, ds18.sample_epoch, ds18.temperature, wind.speed FROM ds18 INNER JOIN wind ON ds18.sample_epoch = wind.sample_epoch WHERE (ds18.sample_time) >=NOW() - INTERVAL 1 MINUTE;" | sed 's/\t/;/g;s/\n//g' > $datastore/sql2c.csv

  # retrieve data for windrose
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM wind where (sample_time) >=NOW() - INTERVAL 50 HOUR;" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql29.csv"

######
datastore="/tmp/domog/mysql4python"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

  # Get hour data for DS18 sensor (graph21)
  # DIV t : t/100 minutes
  # t=100 1'
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
  SELECT MIN(sample_time),temperature \
  FROM ds18 \
  WHERE (sample_time >= NOW() - $interval) \
  GROUP BY sample_time DIV 100;" \
  | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21h.csv"

popd >/dev/null
