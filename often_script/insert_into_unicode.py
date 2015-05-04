#coding:UTF-8
import os
import md5
import sys
import MySQLdb

class kaka:
    def __init__(self):
        conn = MySQLdb.connect(host="182.92.67.121",user="root",passwd="applen_(0)",db="spider",charset="utf8")    
        cu = conn.cursor()
        self.cu = cu
    def insert(self):
        variable = "\u4F60\u597D"
        variable = variable.decode("utf8")
        (self.cu).execute("insert into kk(test)values('"+str(variable)+"')")
        (self.cu).execute("commit")

if __name__ == "__main__":
    kaka = kaka()
    kaka.insert()
