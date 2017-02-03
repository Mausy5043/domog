#!/bin/bash

# Pull DAILY data from MySQL server.

datastore="/tmp/domog/mysql"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

interval="INTERVAL 25 HOUR "
host=$(hostname)

pushd "$HOME/domog" >/dev/null
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM ds18 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21d.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM dht22 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql22d.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM bmp183 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql23d.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM wind where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql29d.csv"

  #http://www.sitepoint.com/understanding-sql-joins-mysql-database/
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT ds18.sample_time, ds18.sample_epoch, ds18.temperature, wind.speed FROM ds18 INNER JOIN wind ON ds18.sample_epoch = wind.sample_epoch WHERE (ds18.sample_time) >=NOW() - INTERVAL 1 MINUTE;" | sed 's/\t/;/g;s/\n//g' > /tmp/sql2c.csv

######
datastore="/tmp/domog/mysql4python"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

  # Get day data for DS18 sensor (graph21)
  # DIV t : t/100 minutes
  # t=1200 12'
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature) \
   FROM ds18 \
   WHERE (sample_time >= NOW() - $interval) \
   GROUP BY sample_time DIV 1200;" \
  | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21d.csv"

popd >/dev/null
