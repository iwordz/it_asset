#!/bin/sh
mysql_dir="./to/path/mysql_path/bin/"
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
nohup python manage.py runserver 0.0.0.0:8000 & 
