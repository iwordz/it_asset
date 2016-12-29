#!/bin/sh
mysql_dir="./mysql5.7/bin/"
it_asset_dir="./it_asset/"
cd $mysql_dir
./mysqladmin -uroot -p12345678
;cmd=` ps -ef  | grep mysqld_safe | awk '{print $2}'`
;echo $cmd
;for port in $cmd;do
; kill -9 $port
;done
./mysqld_safe &
echo "sleep 3 second"
sleep 3
cd $it_asset_dir
python manage.py runserver 0.0.0.0:8000 & 
