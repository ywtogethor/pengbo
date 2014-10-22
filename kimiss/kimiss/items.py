# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class KimissItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class TotalItem(Item):
    productId=Field()
    name=Field() 
    price=Field()
    standard=Field()
    category=Field()
    series=Field()
    function=Field()
    time=Field()
    detail=Field()
    grass=Field()
    family=Field()
class ImageItem(Item):
    productId=Field()
    src=Field()
