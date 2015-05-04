#coding:UTF-8
import random
import time
import os
import re
from hashlib import md5
import MySQLdb

def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()
    
def getDBConn():
    global dbHost,dbUser,dbPasswd,dbName
    conn=MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPasswd,charset='utf8',db=dbName)
    return conn
    
def getDBCursor():
    global conn
    try:
        conn.ping()
    except:        
        conn = connect()
    return conn.cursor()
    
def insertQA():
    global dataDir,finishFilePattern,conn
    cursor=getDBCursor()
    filelist = os.listdir(dataDir)
    finishTime = None
    for fileName in filelist:
        finishFileMatch=finishFilePattern.match(fileName)
        if finishFileMatch:
            finishTime = finishFileMatch.group(1)
            break
    zipPackageList = []
    if finishTime:
        print "finded new package " + finishTime
        processFile = dataDir + finishTime + ".process"
        mysqlProcessList=readProcessFile(processFile)
        packagePattern = "^" + finishTime+"(.*).tar.gz$"
        for fileName in filelist:
            if re.search(packagePattern,fileName):
                fileMd5 = md5_file(dataDir + fileName)
                realMd5 = readmd5(dataDir + fileName + ".md5")
                if fileMd5 == realMd5:
                    zipPackageList.append(fileName)
                else:
                    print fileName + " md5 error"
        if zipPackageList and len(zipPackageList)>0:
            for zipPackageName in zipPackageList:
                zipPackageFilePath = dataDir + zipPackageName
                unzipFilePath = zipPackageFilePath.replace('.tar.gz','/')
                os.popen("rm -rf " + unzipFilePath).readlines()
                print "rm -rf " + unzipFilePath
                mkdirResult = os.popen("mkdir " + unzipFilePath).readlines()
                print "mkdir " + unzipFilePath
                unzipResult = os.popen('tar -zxvf ' + zipPackageFilePath+" -C "+unzipFilePath).readlines()
                print 'tar -zxvf ' + zipPackageFilePath + " -C "+unzipFilePath
                #print unzipResult
                if os.path.isdir(unzipFilePath):
                    mysqlFileList=os.listdir(unzipFilePath)
                    for mysqlFile in mysqlFileList:
                        if re.search("^(.*).sql$",mysqlFile):
                            tempSqlFilePath=unzipFilePath + mysqlFile
                            tempSqlFilePathStr = tempSqlFilePath + "\n"
                            if tempSqlFilePathStr in mysqlProcessList:
                                print tempSqlFilePath + " is readed"
                                continue
                            replaceFile(tempSqlFilePath)
                            lines = open(tempSqlFilePath).readlines()
                            for s in lines:
                                sqlResult=None
                                try:
                                    cursor.execute(s)
                                except:       
                                    print s
                            cursor.execute("commit")
                            fp = open(processFile,'a')  
                            fp.write(tempSqlFilePath + "\n")
                            fp.close()
                            #print "source "+unzipFilePath + mysqlFile + ";"
                            #cursor.execute("source "+unzipFilePath + mysqlFile + ";")
                            #insertMysqlResult = os.popen("mysql -u" + dbUser+" -p" + dbPasswd + " -D" + dbName + "<" + unzipFilePath + mysqlFile ).readlines()
                            #print "mysql -u\"" + dbUser+"\" -p\"" + dbPasswd + "\" -D\"" + dbName + "\"<" + unzipFilePath + mysqlFile
                            #print insertMysqlResult
                else:
                    print unzipFilePath+" is not dir"
        os.remove(dataDir + finishTime + ".finish")
        print "rm " + dataDir + finishTime + ".finish"
    else:
        print "not finded new package"  
        
def readProcessFile(fileName):
    if os.path.isfile(fileName):
        return open(fileName).readlines()
    else:
        return []

def replaceFile(fileName):
    lines = open(fileName).readlines()
    sqlCount=0
    if len(lines)>=8:
        for findex in range(8):
            sqlCount=sqlCount+lines[findex].count('", "')
    if sqlCount<5:
        return
    
    #打开文件，读入每一行
    fp = open(fileName,'w')  
    #打开你要写得文件pp2.txt
    for s in lines:       
        fp.write( s.replace('\'','\\\'').replace(', "',', \'').replace('", ','\', ').replace('");','\');'))   
        # replace是替换，write是写入
    fp.close()

def readmd5(md5File):
    if os.path.isfile(md5File):
        fileObject = open(md5File, 'rb')
        try:
            chunk = fileObject.read(32)
            if not chunk:
                return ""
            return chunk
        finally:
             fileObject.close( )
    return ""
#config
dbHost = "182.92.67.121"
dbName = "zhidao"
dbUser = "root"
dbPasswd = "applen_(0)"
finishFilePattern = re.compile(r'(.*).finish')
#dataDir = "d:/test/"
dataDir="/data/zhidao/"
conn=getDBConn()    #数据库连接
#global data
insertQA()
