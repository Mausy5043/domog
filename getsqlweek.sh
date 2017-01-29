#!/bin/bash

# Pull WEEKLY data from MySQL server.

datastore="/tmp/domog/mysql"

if [ ! -d "$datastore" ]; then
  mkdir -p "$datastore"
fi

interval="INTERVAL 8 DAY "
host=$(hostname)

pushd "${HOME}/domog" >/dev/null
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM ds18 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql21w.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM dht22 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql22w.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM bmp183 where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql23w.csv"
  mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT * FROM wind where (sample_time >=NOW() - $interval);" | sed 's/\t/;/g;s/\n//g' > "$datastore/sql29w.csv"

  #http://www.sitepoint.com/understanding-sql-joins-mysql-database/
  #mysql -h sql.lan --skip-column-names -e "USE domotica; SELECT ds18.sample_time, ds18.sample_epoch, ds18.temperature, wind.speed FROM ds18 INNER JOIN wind ON ds18.sample_epoch = wind.sample_epoch WHERE (ds18.sample_time) >=NOW() - INTERVAL 1 MINUTE;" | sed 's/\t/;/g;s/\n//g' > $datastore/sql2c.csv

  #
  mysql -h sql.lan --skip-column-names -e \
     "USE domotica; \
      SELECT YEAR(sample_time), MONTH(sample_time), DAY(sample_time), HOUR(sample_time),\
      MIN(pressure), AVG(pressure), MAX(pressure), \
      MIN(temperature), AVG(temperature), MAX(temperature) \
      FROM bmp183 \
      WHERE sample_time >= NOW() - $interval \
      GROUP BY YEAR(sample_time), MONTH(sample_time), DAY(sample_time), HOUR(sample_time);" \
      | sed 's/\t/;/g;s/\n//g' > "${datastore}/sql29x.csv"

popd >/dev/null
