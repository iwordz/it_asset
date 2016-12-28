#!/bin/sh
cmd=` ps -ef  | grep mysqld_safe | awk '{print $2}'`
;echo $cmd
for port in $cmd;do
 kill -9 $port
done
