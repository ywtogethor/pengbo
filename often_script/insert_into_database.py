#coding:UTF-8
import MySQLdb

class insert:
    num = 1
    total = 78
    def __init__(self):
        conn = MySQLdb.connect(host="182.92.67.121",user="root",passwd="applen_(0)",db="zhidao",charset="utf8")
        cu = conn.cursor()
        self.cu = cu
    def insert_data(self):
        while self.num<=self.total:
            (self.cu).execute("insert into zhidao_spider_task(keyword,productId,weight,fetchStatus,sourceId)values(\"%s\",%s,%s,%s,%s)" % ("52830008",self.num,1,0,8))
            (self.cu).execute("commit")
            self.num = self.num+1

if __name__ == "__main__":
    ins = insert()
    ins.insert_data()
        
