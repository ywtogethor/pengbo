#coding:UTF-8
import MySQLdb
import os

def getDBConn():
    global dbHost,dbUser,dbPasswd
    conn=MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPasswd,charset='utf8',db='zhidao')
    return conn
    
def getDBCursor():
    global conn
    try:
        conn.ping()
    except:        
        conn = connect()
    return conn.cursor()

def readFile(fileName):
    if os.path.isfile(fileName):
        return open(fileName).readlines()
    else:
        return []

def spiderTaskRun():
    cursor=getDBCursor()
    file_lock = "/data/db_api/spider.flag"
    if os.path.isfile(file_lock):
        os.popen("rm -rf " + file_lock).readlines()
        lines = readFile("/data/db_api/product_spider_task.sql")
        for line in lines:
            cursor.execute(line);
            cursor.execute("commit")

    file_lock = "/data/db_api/new_product_spider.flag"
    if os.path.isfile(file_lock):
        os.popen("rm -rf " + file_lock).readlines()
        lines = readFile("/data/db_api/new_product_spider_task.sql")
        for line in lines:
            cursor.execute(line);
            cursor.execute("commit")
#config
dbHost="182.92.67.121"
dbUser="root"
dbPasswd="applen_(0)"
#global data
conn=getDBConn()    #数据库连接
spiderTaskRun()
