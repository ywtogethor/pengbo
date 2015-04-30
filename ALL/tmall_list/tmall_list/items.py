# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TmallListItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class ProductItem(Item):
    catId = Field()
    productId = Field()
    categoryName = Field()
    categoryId = Field()
