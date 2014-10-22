#coding:UTF-8
from newphoto.items import TotalItem
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.log import err
import re
import urllib
class NewphotoSpider(BaseSpider):
    name="newphoto"
    allowed_domain=["rayli.com.cn"]
    start_urls=["http://hzp.rayli.com.cn/brandlist/search/C_3_1.html"]
    set_url=[]
    def kaka(self):
        url=[]
        string_a="http://hzp.rayli.com.cn/brandlist/search/"
        mu=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        for letter in mu:
            url.append(string_a+letter+"_3_1.html")
        (self.set_url).extend(url)
        err("########################################")
        return url
    def messi(self,response):
        head=response.meta
        for letter in self.kaka():
            index=letter.find('search/')
            head['code']=letter[index+7]
            err("================================")
            yield Request(letter,callback=self.cluo,meta=head)
    def cluo(self,response):
        hea=response.meta
        hxs=HtmlXPathSelector(response)
        total=TotalItem()
        for letter in hxs.select("//div[@class='clear']/div[@class='ymppsy06 pleft30']/div[@class='ymppsy04']"):
            total_src=letter.select("./div[@class='ymppsy05']/a/img/@src").extract()
            total['src']=total_src[0]
            total_china=letter.select("./div[@class='txtCenter lh17 ptop3']/text()[1]").extract()
            total['china']=total_china[0]
            total_english=letter.select("./div[@class='txtCenter lh17 ptop3']/text()[2]").extract()
            total['english']=total_english[0]
            total['name']=total['china']+".jpg"
            total_hold=letter.select("./div[@class='lh20 pleft25 ptop5']/span[3]/text()").extract()
            if total_hold:
                total['hold']=total_hold[0]
            else:
                total['hold']="0"
            path="/dir/image_b/"+total['name']
            urllib.urlretrieve(total['src'],path)
            err("++++++++++++++++++++++++++++++++++++++++")
            yield total
        for lett in (hxs.select("//div[@class='ymppfy01 clear txtRright']/a[@class='ymppfy02']/text()").extract()):
            if re.search("[1-9]",lett):
                newurl= "http://hzp.rayli.com.cn/brandlist/search/"+hea['code']+"_3_"+lett+".html"
                err("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                if newurl not in self.set_url:
                    (self.set_url).append(newurl)
                    yield Request(newurl,callback=self.cluo,meta=hea)
    def parse(self,response):
        return self.messi(response)

