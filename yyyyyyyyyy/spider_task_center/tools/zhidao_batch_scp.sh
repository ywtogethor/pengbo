#!/bin/bash
#contab 
#* 5 * * * /usr/local/services/spider_task_center/tools/batch_scp.sh >/usr/local/services/spider_task_center/log/scp_log.txt 2>&1 &
dest_dir="/data/zhidao/"
date=$(date +%Y%m%d -d '1 days ago')
#date="20141020"
echo "======================start batch scp:$date================="
for line in $(cat /usr/local/services/spider_task_center/conf/zhidao_spider_iplist.txt)
do
  username_host=$line
  dest_filename=$dest_dir$date"_"$line".tar.gz"
  src_filename="~/app-root/data/zhidao/$date/$date.tar.gz"
  /usr/local/services/spider_task_center/tools/scp.exp $username_host $src_filename $dest_filename 
  /usr/local/services/spider_task_center/tools/scp.exp $username_host "$src_filename.md5" "$dest_filename.md5" 
  touch "/data/zhidao/$date.finish"
done
echo "======================finsh batch scp================="
