#!/bin/bash

date=`date -d '1 day ago' +%Y%m%d `
python script/insert_database.py  $date settings

