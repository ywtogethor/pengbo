from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.log import err
from newvalue.items import TotalItem
import re
class NewvalueSpider(BaseSpider):
    name="newvalue"
    allowed_domains=["pclady.com.cn"]
    start_urls=["http://cosme.pclady.com.cn/product/1.html"]
    set_url=['http://cosme.pclady.com.cn/product/1.html']
    def kaka(self,response):
        hxs=HtmlXPathSelector(response)
        total=TotalItem()
        hea=response.meta
        total_name=hxs.select("//div[@class='proMode']/dl/dd/h2/text()").extract()
        total['name']=total_name[0]
        total_valueNum=hxs.select("//p[@class='color2']/span[2]/em/text()").extract()
        total['valueNum']=total_valueNum[0]
        total['idNum']=0
        total_hold=hxs.select("//a[@class='heart1 pink']/text()").extract()
        total_hold_after=(total_hold[0].strip(")")).strip("(")
        total['hold']=total_hold_after
        yield total
        for letter in hxs.select("//a/@href").extract():
            if re.search("cosme.pclady.com.cn/product/[0-9]+\.html",letter):
                if letter not in self.set_url:
                    (self.set_url).append('letter')
                    yield  Request(letter,callback=self.kaka)  
    def parse(self,response):
        return self.kaka(response)

