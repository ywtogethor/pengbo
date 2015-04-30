#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from tmall_list.items import ProductItem
import re
import json
import HTMLParser

class TmallListSpider(BaseSpider):
    name = "tmall_list"
    allowed_domain = ["tmall"]
    start_urls = ["http://s.m.tmall.com/search_data.htm?cat=52806009"]
    categoryId_list = [52816008,52806009,52810008,52820004,52822007,52830011,52808007,52838006,52830010,52816007,52814011,52814010,52810009]
    
    def detail(self,response):
        product = ProductItem()
        head = response.meta
        product_list_dict = json.loads(response.body)       
        if product_list_dict.get("listItem"):
            for letter in product_list_dict["listItem"]:
                if letter.get("item_id"):
                    product['productId'] = long(letter['item_id'])
                    product['categoryId'] = head['categoryId'] 
                    product['categoryName'] = self.get_name(product['categoryId'])
                    product['catId'] = 52830008
                    yield product
                      
  
    def main(self,response):
        num = 1
        head = response.meta
        re_page = re.search("totalPage\": ([0-9]*) ,",response.body)
        total_page = int(re_page.group(1))
        while num <= total_page:
            url_address = "http://s.m.tmall.com/search_data.htm?cat="+str(head['categoryId'])+"&p="+str(num)
            num = num + 1
            yield Request(url_address,callback=self.detail,meta=head)    
   
    def category(self,response):
        head = response.meta
        for letter in self.categoryId_list:
            head['categoryId'] = letter
            letter = "http://s.m.tmall.com/search_data.htm?cat="+str(letter)
            yield Request(letter,callback=self.main,meta=head)         
    
    def get_name(self,data):
        if data == 52816008:
            return "粉底隔离"
        if data == 52806009:
            return "眼线/眉笔/唇线"
        if data == 52810008:
            return "唇膏" 
        if data == 52820004:
            return "唇彩"
        if data == 52822007:
            return "BB霜"
        if data == 52830011:
            return "眼影"
        if data == 52808007:
            return "睫毛膏"
        if data == 52838006:
            return "指甲油"
        if data == 52830010:
            return "粉饼"     
        if data == 52816007:
            return "腮红"
        if data == 52814011:
            return "遮瑕"
        if data == 52814010:
            return "蜜粉"
        if data == 52810009:
            return "彩妆套装"


    def parse(self,response):
        return self.category(response)





