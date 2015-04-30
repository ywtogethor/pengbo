#coding:UTF-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from strawberrynet.items import BrandItem,ProductItem 
class StrawberrynetPipeline(object):
    def process_item(self, item, spider):
        conn=MySQLdb.connect(host='192.168.1.123',user='root',passwd='111111',charset='utf8',db='photo')
        cu=conn.cursor()
        if isinstance(item,BrandItem):
            cu.execute("insert into strawberrynet_brand(chinaBrand,englishBrand,category,brandId)values(%s,%s,%s,%s)",(item['chinaBrand'],item['englishBrand'],item['category'],item['brandId']))
        if isinstance(item,ProductItem):
            cu.execute("insert into strawberrynet_product(name,price,standard,introduce,productId,brandId)values(%s,%s,%s,%s,%s,%s)",(item['name'],item['price'],item['standard'],item['introduce'],long(item['productId']),item['brandId']))
        cu.execute("commit")            
        return item
