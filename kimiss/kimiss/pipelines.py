# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from kimiss.items import TotalItem,ImageItem

class KimissPipeline(object):
    def process_item(self, item, spider):
        conn=MySQLdb.connect(host='192.168.1.128',user='root',passwd='111111',db='photo',charset='utf8')
        cu=conn.cursor() 
        if isinstance(item,TotalItem):
            cu.execute("insert into kimiss_total(productId,name,price,standard,category,series,function,time,detail,grass,family)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(long(item['productId']),item['name'],item['price'],item['standard'],item['category'],item['series'],item['function'],item['time'],item['detail'],int(item['grass']),int(item['family'])))
            cu.execute("commit")
        if isinstance(item,ImageItem):
                cu.execute("insert into kimiss_image(productId,src)values(%s,%s)",(long(item['productId']),item['src']))
                cu.execute("commit")
        return item

