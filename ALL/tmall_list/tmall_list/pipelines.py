# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from tmall_list.items import ProductItem
from scrapy.log import err

class TmallListPipeline(object):
    def process_item(self, item, spider):
        conn = MySQLdb.connect(host='192.168.1.127',user='root',passwd='111111',db='photo',charset='utf8')
        cu = conn.cursor()
        if isinstance(item,ProductItem):
            cu.execute("insert into tmall_list(productId,categoryId,categoryName,catId)values(%s,%s,%s,%s)",(item['productId'],item['categoryId'],item['categoryName'],item['catId']))
        cu.execute("commit")
        return item





