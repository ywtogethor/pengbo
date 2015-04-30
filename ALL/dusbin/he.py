#coding:UTF-8
import MySQLdb
import re
class connect:
    def link(self):       
        conn = MySQLdb.connect(host='182.92.67.121',user='root',passwd='applen_(0)',db='spider',charset='utf8')
        cu = conn.cursor()
        return cu
    def local(self):     
        conn = MySQLdb.connect(host='192.168.1.123',user='root',passwd='111111',db='photo',charset='utf8')
        cu = conn.cursor()  
        return cu
    def num(self):          
        result_list = []
        connect = self.local()
        connect.execute("select productId,brand from tmall_to_makeup_nobrand") 
        result = connect.fetchall()
        for id,brand in result:
            if brand:
                result_list.append(id)
        print len(result_list)
class child(connect):
    number=0
    def kaka(self):
        link = self.link()
        local = self.local()
        link.execute("select productId,brand from tmall_to_makeup")
        result = link.fetchall()
        for id,brand in result:
            if id in self.num():
                self.number = self.number+1
                local.execute("update tmall_to_makeup_nobrand set brand=%s where productId=%s",(brand,id))
                local.execute("commit")       
                local.execute("select brand from tmall_to_makeup_nobrand where productId=%s",(id))
                kk=local.fetchall()
                print self.number
                print kk
                            
if __name__=="__main__":
    conn = connect()
    conn.num()   
   # ch = child()
   # ch.kaka()
