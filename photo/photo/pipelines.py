# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#coding:UTF-8
from photo.items import TotalItem
import MySQLdb
class PhotoPipeline(object):
    def process_item(self, item, spider):
        conn= MySQLdb.connect(host='192.168.1.138',user='root',passwd='111111',db='photo',charset='utf8')
        cu=conn.cursor()
        cu.execute("insert into photo(china,english,src,name,hold)values(%s,%s,%s,%s,%s)",(item['china'],item['english'],item['src'],item['name'],item['hold']))
        cu.execute("commit")
        return item
        
