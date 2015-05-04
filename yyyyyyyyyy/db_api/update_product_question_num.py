#coding:UTF-8
import MySQLdb
import os

def getDBConn():
    global dbHost,dbUser,dbPasswd
    conn=MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPasswd,charset='utf8',db='dbnwebdb1')
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

def questionRun():
    cursor=getDBCursor()
    file_lock = "/data/db_api/finish.flag"
    if os.path.isfile(file_lock):
        os.popen("rm -rf " + file_lock).readlines()
        lines = readFile("/data/db_api/product_question_cnt.sql")
        for line in lines:
            print line
            cursor.execute(line);
            cursor.execute("commit")
#config
dbHost="rds4f83fd46d4210.mysql.aliyun.com"
dbUser="dbnwebmaster1"
dbPasswd="dbn120410"
#global data
conn=getDBConn()    #数据库连接
questionRun()
