#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from tmall.items import ProductItem
import re

class TmallSpider(BaseSpider):
    name = "tmall"
    allowed_domain = ["tmall"]
    start_urls = ["http://list.tmall.com/search_product.htm?spm=a220m.1000858.1000721.1.WX8VnJ&cat=52810007&sort=s&style=g&search_condition=7&from=sn_1_cat&active=1&industryCatId=52808006#J_crumbs"]
    categoryId_list = [52810007,52830009,52808006,52826013,52826010,52826011,52834006,52828008,52834007,52826012,52816006,52804007,52830008,52818007,52804006,52814009,52840005,52812008]
    
    def kaka(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        product = ProductItem()
        re_url = re.search("id=([0-9]+)&skuId",response.url)
        product['productId'] = re_url.group(1)
        product['url'] = response.url
        product['promote_price'] = hea["price"]
        origin_price_re = re.search('defaultItemPrice\":\"([^"]*)\",',response.body)
        product['origin_price'] = origin_price_re.group(1)
        product_send_address = hxs.select("//input[@name='region']/@value").extract()
        product['send_address'] = product_send_address[0]
        product_standard = hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li/a/span/text()").extract()
        if product_standard:
            product['standard'] = product_standard[0]
        else:
            product['standard'] = ""
        product_name = hxs.select("//input[@name='title']/@value").extract()
        product['name'] = product_name[0]
        yield product

    def cluo(self,response):
        hxs = HtmlXPathSelector(response)
        url_price = hxs.select("//div[@class='product']/div[@class='product-iWrap']")
        for letter in url_price:
            url_one = letter.select("./div[@class='productImg-wrap']/a[1]/@href").extract()
            price_one = letter.select("./p[@class='productPrice']/em/@title").extract()
            head = response.meta
            head["price"] = price_one[0]
            yield Request("http:"+url_one[0],callback=self.kaka,meta=head)
 
    def messi(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        totalPage = hxs.select("//input[@name='totalPage']/@value").extract()
        num = 1
        while num <= int(totalPage[0]):
            url = hea["cat"]+"&s="+str((num-1)*60)
            yield Request(url,callback=self.cluo)
            num = num+1 
   
    def haha(self,response):
        hxs =  HtmlXPathSelector(response)
        for letter in self.categoryId_list:
            head = response.meta
            head["cat"] = "http://list.tmall.com/search_product.htm?cat="+str(letter)
            yield Request("http://list.tmall.com/search_product.htm?cat="+str(letter),callback=self.messi,meta=head)
    def parse(self,response):
        return self.haha(response)
    














