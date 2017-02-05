#!/bin/bash

# Pull WEEKLY data from MySQL server.

datastore="/tmp/domog/mysql"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

interval="INTERVAL 8 DAY "
host=$(hostname)

pushd "${HOME}/domog" >/dev/null
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM ds18   where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21w.csv"
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM dht22  where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql22w.csv"
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM bmp183 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql23w.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM wind   where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql29w.csv"

  #http://www.sitepoint.com/understanding-sql-joins-mysql-database/
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT ds18.sample_time, ds18.sample_epoch, ds18.temperature, wind.speed FROM ds18 INNER JOIN wind ON ds18.sample_epoch = wind.sample_epoch WHERE (ds18.sample_time) >=NOW() - INTERVAL 1 MINUTE;" | sed 's/\t/;/g;s/\n//g' > $datastore/sql2c.csv

  ######
  datastore="/tmp/domog/mysql4python"

  if [ ! -d "$datastore" ]; then
    mkdir -p "$datastore"
  fi

  # Get week data for DS18 sensor (graph21)
  # DIV t : t/100 minutes
  # t=6000 60'
  divider=12000
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature) \
   FROM ds18 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_time DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql21w.csv"

  # Get data for DHT22 sensor (graph22)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
                            MIN(humidity), AVG(humidity), MAX(humidity) \
   FROM dht22 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_time DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql22w.csv"

  # Get data for BMP183 sensor (graph23)
  mysql -h sql.lan --skip-column-names -e \
  "USE domotica; \
   SELECT MIN(sample_time), MIN(temperature), AVG(temperature), MAX(temperature), \
                            MIN(pressure), AVG(pressure), MAX(pressure) \
   FROM bmp183 \
   WHERE (sample_time >= NOW() - ${interval}) \
   GROUP BY (sample_time DIV ${divider});" \
  | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql23w.csv"

popd >/dev/null
