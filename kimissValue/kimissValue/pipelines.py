# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from kimissValue.items import TotalItem,DetailItem,ContentItem
class KimissvaluePipeline(object):
    def process_item(self, item, spider):
        conn=MySQLdb.connect(host='192.168.1.123',user='root',passwd='111111',db='photo',charset='utf8')
        cu=conn.cursor()
        if isinstance(item,TotalItem):
            cu.execute("insert into kimissValue_total(productId,veryGood,good,veryBad,bad,common)values(%s,%s,%s,%s,%s,%s)",(item['productId'],int(item['veryGood']),int(item['good']),int(item['veryBad']),int(item['bad']),int(item['common'])))
            cu.execute("commit")
        if isinstance(item,DetailItem):
            cu.execute("insert into kimissValue_detail(productId,hair,skin,age)values(%s,%s,%s,%s)",(item['productId'],item['hair'],item['skin'],item['age']))
            cu.execute("commit")
        if isinstance(item,ContentItem):
            cu.execute("insert into kimissValue_content(productId,purchase,time,effect,theme)values(%s,%s,%s,%s,%s)",(item['productId'],item['purchase'],item['time'],item['effect'],item['theme']))
            cu.execute("commit")
        return item

