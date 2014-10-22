# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class TotalItem(Item):
    productId=Field()
    productName=Field()

class DetailItem(Item):
    productId=Field()
    name=Field()
    skin=Field()
    age=Field()
    time=Field()
    simpleContent=Field()
    moduleId=Field()
    sign=Field()

class ContentItem(Item):
    moduleId=Field()
    complexContent=Field()

class ImageItem(Item):
    moduleId=Field()
    src=Field()
