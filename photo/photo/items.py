# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PhotoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
class TotalItem(Item):
    src=Field()
    china=Field()
    english=Field()
    hold=Field()
    name=Field()
#class ImageItem(Item):
 #  url=Field()
