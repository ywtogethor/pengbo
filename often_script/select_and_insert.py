#coding:UTF-8
import MySQLdb

class insert:
    def __init__(self):
        conn = MySQLdb.connect(host="182.92.67.121",user="root",passwd="applen_(0)",db="zhidao",charset="utf8")
        cu = conn.cursor()
        self.cu = cu
        con = MySQLdb.connect(host="192.168.1.127",user="root",passwd="111111",db="photo",charset="utf8")
        cur = con.cursor()
        self.cur = cur

    def insert_data(self):
        print "------------------"
        (self.cur).execute("select productId,catId from tmall_all")
        all_result = self.cur.fetchall()
        for productId,catId in all_result:
            (self.cu).execute("insert into zhidao_spider_task(keyword,productId,weight,fetchStatus,sourceId)values(\"%s\",%s,%s,%s,%s)" % (str(catId),productId,1,0,9))
            (self.cu).execute("commit")
            print "=========================="
 
if __name__ == "__main__":
    ins = insert()
    ins.insert_data()


