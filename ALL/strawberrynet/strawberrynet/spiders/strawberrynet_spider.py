#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from strawberrynet.items import ProductItem,BrandItem
import re
class StrawberrynetSpider(BaseSpider):
    name = "strawberrynet"
    allowed_domain = ["strawberrynet.com"]
    start_urls=["http://cn.strawberrynet.com/main.aspx"]
    url_front="http://cn.strawberrynet.com"
    url_back="/ajaxMenuBrand.aspx?index="  
    num = 0
    def messi(self,response):
        letters_list=["1","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        for letter in letters_list:
            yield Request(self.url_front+self.url_back+letter,callback=self.bell)
    def bell(self,response):
        hxs=HtmlXPathSelector(response)
        head = response.meta
        brand_url_list=hxs.select("//div[@class='column']/a[1]/@href").extract()
        if "" in brand_url_list:
            brand_url_list=list(set(brand_url_list))
            brand_url_list.remove("") 
        for letter in brand_url_list:
            self.num+=1
            brandId = self.num
            head['code']=brandId
            yield Request(self.url_front+letter,self.cluo,meta=head)
    def cluo(self,response):
        hxs=HtmlXPathSelector(response)
        brand = BrandItem()
        hea=response.meta
        brand['brandId']=hea['code']
        brand_category=hxs.select("//nav[@class='breadcrumbs']/ul/li[2]/a/text()").extract()
        brand['category']=brand_category[0]
        brand_brand=hxs.select("//nav[@class='breadcrumbs']/ul/li[3]/span/text()").extract()
        if "  " in brand_brand[0]:
            brand_brand_list=brand_brand[0].split("  ")    
            brand['chinaBrand']=brand_brand_list[0]
            brand['englishBrand']=brand_brand_list[1]
        else:
            brand['chinaBrand']=brand_brand[0]
            brand['englishBrand']=""
        yield brand
        product_url_list=hxs.select("//div[@class='img-holder']/a/@href").extract()   
        for letter in product_url_list:
            yield Request(self.url_front+letter,callback=self.kaka,meta=hea)
    def kaka(self,response):
        product = ProductItem()
        hxs=HtmlXPathSelector(response)
        he = response.meta
       # product_id_pattern="/([0-9]+)/"
        product_object=hxs.select("//div[@class='product-frame']/div[@class='table-holder']/table[@class='table-info']/tbody/tr/td[@class='discount']")
        err("===========================================")
        for index in range(len(product_object)):
           # product_productId=re.search(product_id_pattern,response.url)
            product_productId=product_object[index].select("./../td[@class='first']/div[1]/@id").extract()
            product['productId']=product_productId[0].replace("radio_","")
            product['brandId']=he['code']
            product_name=hxs.select("//div[@class='product-frame']/h2/text()").extract()
            product['name']=product_name[0]
            product_price=product_object[index].select("./../td[@class='last price']/text()").extract()
            product_price_one=product_price[0].replace(u"¥","")
            if "," in product_price_one:
                product['price']=product_price_one.replace(",","")
            else:
                product['price']=product_price_one
            product_standard=product_object[index].select("./../td[@class='first']/div[2]/label/text()").extract()
            product['standard']=product_standard[0].strip()
            product_introduce=hxs.select("//div[@class='tab-content']/div[@id='tab1_3']/div["+str(index+1)+"]/ul[@class='desc-ul']/li/text()").extract()
            product['introduce']="\n".join(product_introduce)
            yield product
        
    def parse(self,response):
        return self.messi(response)    
