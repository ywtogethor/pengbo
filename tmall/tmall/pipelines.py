# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from tmall.items import ProductItem
from scrapy.log import err

class TmallPipeline(object):
    def process_item(self, item, spider):
        conn = MySQLdb.connect(host='192.168.1.123',user='root',passwd='111111',db='photo',charset='utf8')
        cu = conn.cursor()
        if isinstance(item,ProductItem):
            cu.execute("insert into tmall_tmall(productId,name,promote_price,origin_price,send_address,standard,url)values(%s,%s,%s,%s,%s,%s,%s)",(long(item['productId']),item['name'],float(item['promote_price']),item['origin_price'],item['send_address'],item['standard'],item['url']))
        cu.execute("commit")
        return item

