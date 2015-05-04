#encoding=UTF-8
import MySQLdb
import codecs
import string
import datetime
import sys
import os

result_path = "/data/db_api/"

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    if (len(sys.argv) != 1):
        print "Usage : ...."
        sys.exit(1)
    db = MySQLdb.connect("rds4f83fd46d4210.mysql.aliyun.com", "dbnwebmaster1", "dbn120410", "dbnwebdb1", charset='utf8');
    cursor = db.cursor()

    # SQL 
    sql = 'select id,name from dbn_products where view_status=1 '
    cursor.execute(sql)
    results = cursor.fetchall()
    result_file = file(result_path + "products.data", 'w')
    for row in results:
        result_file.write(str(row[0]) + '\n')
        result_file.write(str(row[1]).replace("\n"," ") + '\n')
    result_file.close()
    db.close();

