#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from kimiss.items import TotalItem,ImageItem 
from scrapy.http import Request,Response
import data_a,data_b,data_c,data_d,data_i,data_j
import re
from scrapy.http.response.html import HtmlResponse
class KimissSpider(BaseSpider):
    name="kimiss"
    allowed_domain=["kimiss.com"] 
    start_urls=["http://product.kimiss.com/product/35176/"]
    num=1
    def kaka(self,response):
        err("==============================================================")
        while self.num<400000:
            url="http://product.kimiss.com/product/"+str(self.num)+"/"
            if self.num<=30000 and self.num not in data_a.list_a:
                yield Request(url,callback=self.cluo)
            if 30000<self.num<=60000 and self.num not in data_b.list_b:
                yield Request(url,callback=self.cluo)
            if 60000<self.num<=90000 and self.num not in data_c.list_c:
                yield Request(url,callback=self.cluo)
            if 90000<self.num<=120000 and self.num not in data_d.list_d:
                yield Request(url,callback=self.cluo)
            if 120000<self.num<=240000:
                yield Request(url,callback=self.cluo)
            if 240000<self.num<=270000 and self.num not in data_i.list_i:
                yield Request(url,callback=self.cluo)
            if 270000<self.num<=300000 and self.num not in data_j.list_j:
                yield Request(url,callback=self.cluo)
            if 30000<self.num<400000:
                yield Request(url,callback=self.cluo)
            self.num+=1
    def cluo(self,response):
        total=TotalItem()
        image=ImageItem()
        hxs=HtmlXPathSelector(response)
        exist=hxs.select("//div")
        if exist:
            total_productId=response.url
            mm=re.search("/product/([0-9]+)/",total_productId)
            total['productId']=mm.group(1)
            total_name=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='preview_title']/h1/a/text()").extract()
            total['name']=total_name[0]
            total_price=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='preview_brief']/em/text()").extract()
            if total_price:
               # total_priceA=total_price[0].replace(u"元","")
               # if total_priceA=="":
               #     total['price']=-1
               # if total_priceA!="":
               #     total['price']=float(total_priceA)
                total['price']=total_price[0]   
            else:
                total['price']=u"无"
            total_standard=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='preview_brief']").extract()
            if total_standard:
                total_standardA=total_standard[0]
                total_standardB=total_standardA.replace("\n","")
                total_standardC=total_standardB.replace(" ","")
                pattern_a=u"\uff1a.+\uff1a(.*)</div>"
                kk=re.search(pattern_a,total_standardC)
                if kk:
                    total['standard']=kk.group(1)
                else:
                    total['standard']=""
            else:
                total['standard']=""
            total_compile=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='previewD']/ul").extract()
            pattern_aa=u"产品品类：</span><a[^>]+>([^<]+)</a>"
            pattern_bb=u"所属系列：</span><a[^>]+>([^<]+)</a>"
            pattern_cc=u"产品功效：</span>(.+)</li>"
            pattern_dd=u"上市时间：</span><a[^>]+>([^<]+)</a>"
            total_category=re.search(pattern_aa,total_compile[0])
            if total_category:
                total['category']=total_category.group(1)
            else:
                total['category']=""
            total_series=re.search(pattern_bb,total_compile[0])
            if total_series:
                total['series']=total_series.group(1)
            else:
                total['series']=""
            total_compile_new=total_compile[0].replace("\n","")
            total_function=re.search(pattern_cc,total_compile_new)
            if total_function:
               # functionResponse=HtmlResponse(body=total_function.group(1),url='',encoding='utf-8')
               # hxx=HtmlXPathSelector(functionResponse)
               # total_function_a=hxx.select("//a/text()").extract()
               # total['function']=" ".join(total_function_a)
                total_function_content=total_function.group(1)
                err(total_function_content)
                err("=============================================================================")
                total_function_a=re.sub("<[^>]+>","",total_function_content)
                total_function_b=total_function_a.replace("&nbsp;"," ")
                total_function_c=total_function_b.strip()
                total['function']=total_function_c
            else:
                total['function']=""
            total_time=re.search(pattern_dd,total_compile[0])
            if total_time:
                total['time']=total_time.group(1)
            else:
                total['time']=""
            total_detail=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='previewE']/p/span/text()").extract()
            total_detail_a=total_detail[0].replace("\n\n","\n")
            total_detail_a=total_detail_a.strip()
            total_detail_a=total_detail_a.replace("\t"," ")
            total_detail_a=total_detail_a.replace("&nbsp;"," ")
            if total_detail: 
                total['detail']=total_detail_a
            else:
                total['detail']=""
            total_grass=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='previewF']/span[1]/i/text()").extract()
            total['grass']=total_grass[0]
            total_family=hxs.select("//div[@class='c1_left_1']/div[@class='preview_r']/div[@class='previewF']/span[2]/i/text()").extract()
            total['family']=total_family[0]
            yield total
            image['productId']=mm.group(1)
            image_src=hxs.select("//div[@class='c1_left_1']/div[@id='preview']/div[@class='scroll_all']/div[@class='bd']/ul/li/img/@src").extract()
            for letter in image_src:
                image['src']=letter
                err(image['src'])
                yield image
                                                  
    def parse(self,response):
        err("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44")
        return self.kaka(response)





        



























