#!/bin/bash
cd /usr/local/services/spider_task_center/
PIDS=`ps -ef |grep zhidao_dump_to_db |grep -v grep | wc -l`
if [ $PIDS != 1 ]; then
  echo "restart zhidao_dump_to_db"
  python zhidao_dump_to_db.py >>/usr/local/services/spider_task_center/log/zhidao_dump_to_db.log 2>&1 &
fi
