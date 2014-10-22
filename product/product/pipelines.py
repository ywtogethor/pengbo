# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from product.items import TotalItem,ContentItem,ImageItem,DetailItem

class ProductPipeline(object):
    def process_item(self, item, spider):
        conn=MySQLdb.connect(host='192.168.1.128',user='root',passwd='111111',db='photo',charset='utf8')
        cu=conn.cursor()
       # if not item :
       #     return None
        if isinstance(item,TotalItem):
            cu.execute("insert into product_total(productId,productName)values(%s,%s)",(item['productId'],item['productName']))
            cu.execute("commit")
        if isinstance(item,DetailItem):
            cu.execute("insert into product_detail(productId,name,skin,age,time,simpleContent,sign,moduleId)values(%s,%s,%s,%s,%s,%s,%s,%s)",(item['productId'],item['name'],item['skin'],item['age'],item['time'],item['simpleContent'],item['sign'],long(item['moduleId'])))
            cu.execute("commit")
        if isinstance(item,ContentItem):
            cu.execute("insert into product_content(moduleId,complexContent)values(%s,%s)",(long(item['moduleId']),item['complexContent']))
            cu.execute("commit")
        if isinstance(item,ImageItem):
            for letter in item['src']:
                cu.execute("insert into product_image(moduleId,src)values(%s,%s)",(long(item['moduleId']),letter))
                cu.execute("commit")
        return item



