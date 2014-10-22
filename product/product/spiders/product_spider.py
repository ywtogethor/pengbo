#coding:UTF-8
from scrapy.http import Request,Response
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from product.items import TotalItem,DetailItem,ContentItem,ImageItem
from scrapy.log import err
from product.urldata import haha
import re
import json   
import urllib2 

class ProductSpider(BaseSpider):
    name="product"
    allowed_domains=["lady.163.com"]
    start_urls=haha
   # start_urls=["http://cosmetic.lady.163.com/product/3000026021.html"]
   # num=3000026020
   # def kaka(self,response):
   #     string_a="http://cosmetic.lady.163.com/product/"
   #     string_b=".html"
   #     head=response.meta
   #     while self.num<3000026025:
   #         self.num+=1
   #         head['code']=self.num
   #         url_url=string_a+str(self.num)+string_b 
   #         yield Request(url_url,callback=self.messi,meta=head)
    def bell(self,response):
        he=response.meta
        content_a=urllib2.urlopen(response.url).read()
        jsonCode=json.loads(content_a)
        jsonCodeNum=jsonCode['data']['total']
        if jsonCodeNum>=8:
            page=jsonCodeNum/8
            list_number=range(page)
            list_number.remove(0)
            list_number.append(page)
            list_number.append(page+1)
            for letter in list_number:
                url_a="http://cosmetic.lady.163.com/post/post.json?productId="+str(he['code'])+"&page="+str(letter)+"&order=1"
                yield Request(url_a,callback=self.cluo,meta=he)
        if jsonCodeNum!=0 and jsonCodeNum<8:
            url_a="http://cosmetic.lady.163.com/post/post.json?productId="+str(he['code'])+"&page=1&order=1"
            yield Request(url_a,callback=self.cluo,meta=he)
    def cluo(self,response):
        h=response.meta
        content_b=urllib2.urlopen(response.url).read()
        json_code=json.loads(content_b)
        json_content=json_code['data']['content']
        jsonResponse=HtmlResponse(body=json_content,url='',encoding='utf-8')
        hxs=HtmlXPathSelector(jsonResponse)
        for letter in hxs.select("//div[@class='dataBox-main']"):
            detail=DetailItem()
            detail['productId']=h['code']
            detail_name=letter.select("./div[@class='hd ph-15']/div[@class='left']/span[1]/a/text()").extract()
            detail['name']=detail_name[0]
            detail_skin=letter.select("./div[@class='hd ph-15']/div[@class='left']/span[2]/text()").extract()
            detail_skin_a=detail_skin[0].replace(u"肤质：","")
            detail['skin']=detail_skin_a
            detail_age=letter.select("./div[@class='hd ph-15']/div[@class='left']/span[3]/text()").extract()
            detail_age_a=detail_age[0].replace(u"年龄：","")
            detail['age']=detail_age_a
            detail_time=letter.select("./div[@class='hd ph-15']/div[@class='right']/span/text()").extract()
            detail['time']=detail_time[0]
            detail_simpleContent=letter.select("./div[@class='bd ph-15']/p[@class='cDGray']/span/text()").extract()
            detail['simpleContent']=detail_simpleContent[0]
            detail_moduleId=letter.select("..//@id").extract()
            detail['moduleId']=detail_moduleId[0]
            detail_sign=letter.select("..//div[@class='dataBox-side']/i/text()").extract()
            if detail_sign:
                detail['sign']=detail_sign[0]
            else:
                detail['sign']="0"
            yield detail
            detail_url=letter.select("./div[@class='bd ph-15']/p[@class='cDGray']/a/@href").extract()
            detailUrl="http://cosmetic.lady.163.com"+ detail_url[0]
            yield Request(detailUrl,callback=self.jluo)
    def jluo(self,response):
        hxs=HtmlXPathSelector(response)
        content=ContentItem()
        image=ImageItem()
        content_a=hxs.select("//textarea[@id='content']").extract()
        content_b=content_a[0].replace("</p>","\n")
        content_c=content_b.replace("<br/>","\n")
       # content_c=content_b.replace("\n\n\n","\n")
       # content_d=content_c.replace("\n\n","\n")
       # content_e=content_d.replace("\n \n","\n")
        content_d=re.sub("<[^>]+>","",content_c)
        content_complexContent=re.sub("[\n ]*\n[ ]?","\n",content_d)
        content_complexContent_a=content_complexContent.strip(" ")
        content_complexContent_b=content_complexContent_a.strip("\n")
        content_complexContent_c=content_complexContent_b.strip(" ")
        content['complexContent']=content_complexContent_c.strip("\n")
        content_pattern_a=re.search("post/([0-9]+)\.html",response.url)
        content['moduleId']=content_pattern_a.group(1)
        yield content
       # image['moduleId']=content_pattern_a.group(1)
        for letter in hxs.select("//textarea[@id='content']"):
            if letter.select(".//img/@src").extract():
                image['moduleId']=content_pattern_a.group(1)
                image['src']=letter.select(".//img/@src").extract() 
                yield image
       #	letter= hxs.select("//div[@class='content']")[0]
       # if letter.select(".//img/@src").extract():
       #     for al in letter.select(".//img/@src").extract():
       #         image=ImageItem()
       #        image['moduleId']=content_pattern_a.group(1)
       #	        image['src']=al
       #	        yield image
    def messi(self,response):
        id=re.search("([0-9]+)\.html",response.url)
        hea=response.meta
        hea['code']=id.group(1)
        hxs=HtmlXPathSelector(response)
        total=TotalItem() 
        total_nameProduct=hxs.select("//div[@class='detailbox-main']/div[@class='clearfix']/h1").extract()
        total['productName']=re.sub("<[^>]+>","",total_nameProduct[0])
        total['productId']=hea['code']
        yield total
        newurl="http://cosmetic.lady.163.com/post/post.json?productId="+str(hea['code'])
        yield Request(newurl,callback=self.bell,meta=hea)
      
    def parse(self,response):
        return self.messi(response)
              
        
        
        
    

              
        
        
        
    
