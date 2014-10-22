from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.log import err
from value.items import TotalItem
import re
class ValueSpider(BaseSpider):
    name="value"
    allowed_domains=["pclady.com.cn"]
    start_urls=["http://cosme.pclady.com.cn/product/1.html"]
    num=140000
    def messi(self,response):
        while self.num<180000:
            head=response.meta
            self.num+=1
            head['code']=self.num
            url="http://cosme.pclady.com.cn/product/"+str(self.num)+".html"
            yield Request(url,callback=self.kaka,meta=head)
    def kaka(self,response):
        hxs=HtmlXPathSelector(response)
        total=TotalItem()
        hea=response.meta
        total_name=hxs.select("//div[@class='proMode']/dl/dd/h2/text()").extract()
        total['name']=total_name[0]
        total_valueNum=response.body
        total_search=re.search("\$\(\"#_comment_count\"\)\.html\('([0-9]+)'\);",total_valueNum)
        total['valueNum']= total_search.group(1)
        total['idNum']=hea['code']
        total_hold=hxs.select("//a[@class='heart1 pink']/text()").extract()
        total_hold_after=(total_hold[0].strip(")")).strip("(")
        total['hold']=total_hold_after
        yield total
    def parse(self,response):
        return self.messi(response) 

        
