#encoding=UTF-8
import MySQLdb
import codecs
import string
import datetime
import sys
import os
import time

gSpiderTaskResultSql = 'insert into zhidao_spider_task(keyword,productId,fetchStatus,sourceId,type) values (\'%s\',%s,0,1,1);\n'
result_path = "/data/db_api/"
result_file = file(result_path + "new_product_spider_task.sql", 'w')

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    if (len(sys.argv) != 1):
        print "Usage : ...."
        sys.exit(1)
    db = MySQLdb.connect("rds4f83fd46d4210.mysql.aliyun.com", "dbnwebmaster1", "dbn120410", "dbnwebdb1", charset='utf8');
    cursor = db.cursor()

    # SQL 
    now_timestamp = int(time.time()) - 3600*24
    timeArray = time.localtime(now_timestamp)
    now_date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sql = 'select id,name from dbn_products where view_status=1 and id>120000 and modifyTime >=\'' + str(now_date) + '\''
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print str(row[0]) + " " + str(row[1])
        result_file.write(gSpiderTaskResultSql % (str(row[1]), str(row[0]))) 
    
    result_flag_file = file(result_path + "new_product_spider.flag", 'w')
    result_flag_file.close()
    result_file.close()
    db.close();

