#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
from scrapy.log import err
from scrapy.spider import BaseSpider
from kimissValue.items import TotalItem,DetailItem,ContentItem
from urldata import urldata
class KimissValueSpider(BaseSpider):
    name="kimissValue"
    allowed_domain=["kimiss.com"]
    start_urls=["http://product.kimiss.com/product/5711/1/"]
    urlAll=[]
    def messi(self,response):
        head=response.meta
        for letter in urldata:
            head['code']=letter
            url_url="http://product.kimiss.com/product/"+str(letter)+"/1/"
            yield Request(url_url,callback=self.kaka,meta=head)
    def kaka(self,response):
        total=TotalItem()
        detail=DetailItem()
        content=ContentItem()
        hxs=HtmlXPathSelector(response)
        hea=response.meta
        total['productId']=hea['code']
        total_veryGood=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[1]/td/div[4]/text()").extract()
        total['veryGood']=total_veryGood[0].replace(u"条","")
        total_good=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[2]/td/div[4]/text()").extract()
        total['good']=total_good[0].replace(u"条","")
        total_common=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[3]/td/div[4]/text()").extract()
        total['common']=total_common[0].replace(u"条","")
        total_bad=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[4]/td/div[4]/text()").extract()
        total['bad']=total_bad[0].replace(u"条","")
        total_veryBad=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[5]/td/div[4]/text()").extract()
        total['veryBad']=total_veryBad[0].replace(u"条","")
        yield total               
       # detail_exist=hxs.select("//div[@class='userm']")
       # detail_detail=hxs.select("//div[@class='user_box']")
       # for letter in detail_detail:
        detail_element=hxs.select("//div[@class='userm']").extract()
        err("==========================================")
        if detail_element:
            for letter in detail_element:
                detail['productId']=hea['code']
                detail_hair=re.search(u"<br[ ]*>([^<]+)发质",letter)
                if detail_hair:
                    detail['hair']=detail_hair.group(1)
                else:
                    detail['hair']=""    
                detail_skin=re.search(u"<br[^<]*>([^<]+)皮肤",letter)
                if detail_skin:
                    detail['skin']=detail_skin.group(1)
                else:
                    detail['skin']=""
                detail_age=re.search(u"<br[^<]+年龄:(.+)</div>",letter)
                if detail_age:
                    detail['age']=detail_age.group(1)
                else:
                    detail['age']=""
                yield detail
        content_element=hxs.select("//div[@class='comment_area']")
        for letter in content_element:
            content['productId']=hea['code']
            content_theme=letter.select("./div[@class='iwom']/span[1]/a/text()").extract()
            if content_theme:
                content['theme']=content_theme[0]
            else:
                content['theme']=""
            content_time=letter.select("./div[@class='iwom']/span[2]/text()").extract()
            if content_time:
                content['time']=content_time[0]  
            else:
                content['time']=""
            content_purchase=letter.select("./div[@class='buying'][1]/span[@class='comment_content']/text()").extract()
            if content_purchase:
                content_purchase_join=" ".join(content_purchase)
                content['purchase']=content_purchase_join
            else:
                content['purchase']=""
            content_effect=letter.select("./div[@class='buying'][2]/span/text()").extract()
            if content_effect:
                content_effectA=re.sub("<[^>]+>","",content_effect[0])
                content['effect']=content_effectA
            else:
                content['effect']=""
            yield content
        other_page=hxs.select("//div[@align='right']/div[@align='right']").extract()
        if other_page:
            other_page_a=other_page[0]
            other_page_b=other_page_a.strip()
            if "\n" in other_page_b:
                other_page_b=other_page_b.replace("\n","")
            result=re.search(u"当前页：[0-9]+/([0-9]+) 第",other_page_b)
            if result:
                page=result.group(1)
                list_page=range(2,int(page)+1)
                for letter in list_page:
                    url_url_url="http://product.kimiss.com/product/"+str(hea['code'])+"/"+str(letter)+"/"
                    if url_url_url not in self.urlAll:
                        (self.urlAll).append(url_url_url)
                        yield Request(url_url_url,callback=self.kaka,meta=hea)
    def parse(self,response):
        return self.messi(response)



        
     
