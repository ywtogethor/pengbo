# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#coding:UTF-8
import MySQLdb
from value.items import TotalItem
class ValuePipeline(object):
    def process_item(self, item, spider):
        conn=MySQLdb.connect(host='192.168.1.138',user='root',passwd='111111',db='photo',charset='utf8')
        cu=conn.cursor()
        cu.execute("insert into value(name,valueNum,hold,idNum)values(%s,%s,%s,%s)",(item['name'],int(item['valueNum']),int(item['hold']),int(item['idNum'])))
        cu.execute("commit")
        return item
