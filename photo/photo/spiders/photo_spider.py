#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from photo.items import TotalItem
from scrapy.http import Request
from scrapy import log
import urllib
class PhotoSpider(BaseSpider):
    name="photo"
    allowed_domains=["ileehoo.com"]
    start_urls=["http://hzp.ileehoo.com/brand/B_0_1.html"]
    set_url=[]
    def mm(self):
       string_url=[]
       string_a="http://hzp.ileehoo.com/brand/"
       string_b="_0_1.html#searchbrandlist"
       list_a=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
       for letter in list_a:
           string_c=string_a+letter+string_b
           string_url.append(string_c)
       (self.set_url).extend(string_url)
       return string_url
    def nn(self,response):
        hxs=HtmlXPathSelector(response)
        for letter in self.mm():
            log.err("===========================")
            yield Request(letter,callback=self.kaka)
         
    def kaka(self,response): 
        total=TotalItem()   
       # image=ImageItem()
        hxs=HtmlXPathSelector(response)
        for letter in hxs.select("//div[@class='con']/div[@class='listimg']"):
            total_china=letter.select("./div[@class='tit']/a[1]/text()").extract()
            total['china']=total_china[0].strip(" ")
            total_english=letter.select("./div[@class='tit']/a[2]/text()").extract()
            total['english']=total_english[0].strip(" ")
            total_hold=letter.select("./div[@class='lis']/span[3]/text()").extract()
            total['hold']=total_hold[0]
            total_src=letter.select("./div[@class='']/a/img/@src").extract()
            total['src']=total_src[0]
            total['name']=total['china']+".jpg"
         #  image['url']=letter.select("./div[@class='']/a/img/@src")
         #  for letter_a in total['src']:
            path="/dir/image/"+total['name']
            urllib.urlretrieve(total['src'],path)
            yield total
        newurl=hxs.select("//div[@class='page']/a/@href").extract()
        if newurl:
            for letter in newurl:
                if letter not in self.set_url:
                    (self.set_url).append(letter)    
                    yield  Request(letter,callback=self.kaka)
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        return self.nn(response)
