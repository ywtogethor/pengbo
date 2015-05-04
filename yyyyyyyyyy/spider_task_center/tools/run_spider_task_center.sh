#!/bin/bash
cd /usr/local/services/spider_task_center/
PIDS=`ps -ef |grep spider_task_center |grep -v grep | awk '{print $2}'`
if [ "$PIDS" ]; then
 python spider_task_center.py >/usr/local/services/spider_task_center/log/spider_task_center.log 2>&1 &
fi
