#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from tmall.items import ProductCommonItem,ProductImgItem,ProductDetailItem
import re
import json
import HTMLParser

class TmallSpider(BaseSpider):
    name = "tmall"
    allowed_domain = ["tmall"]
    start_urls = ["http://detail.tmall.com/item.htm?id=35579706942&cat_id=11111"]
    categoryId_list = [52810007]
    
    def product(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        html_parser = HTMLParser.HTMLParser()
        common = ProductCommonItem()
        img = ProductImgItem()
        detail = ProductDetailItem()        
        # 爬取产品详情页公共信息
        re_product_url = re.search("id=([0-9]+)",response.url)
        re_cat_url = re.search("cat_id=([0-9]+)",response.url)
        common['productId'] = re_product_url.group(1)
        common['catId'] = re_cat_url.group(1)
        common['url'] = response.url
        common_send_address = hxs.select("//input[@name='region']/@value").extract()
        common['send_address'] = common_send_address[0]
        common_name = hxs.select("//input[@name='title']/@value").extract()
        common['name'] = html_parser.unescape(common_name[0])
        err("========================")
        common_one = common['name'].encode("utf8")
        err(type(common_one))
        err(common_one)
        err("========================")
        re_brand = re.search("brand\":\"([^,]*)\"",response.body)
        if re_brand:
            common_brand= re_brand.group(1)
            common['brand'] = html_parser.unescape(common_brand)
        else:
            common['brand'] = ""       
        common_description = hxs.select("//div[@class='tb-detail-hd']/p/text()").extract()
        common['description'] = common_description[0].strip() 
        common_parameter = hxs.select("//ul[@id='J_AttrUL']/li/text()").extract()
        common['parameter'] = self.process_data(common_parameter)        
        yield common
        # 爬取产品详情页品牌图片
        img['productId'] = common['productId']
        brand_little_img_list = hxs.select("//ul[@class='tb-thumb tm-clear']/li")
        for letter in brand_little_img_list:
            brand_little_img = letter.select("./a/img/@src").extract()        
            img['brand_little_img'] = brand_little_img[0]
            img['brand_big_img'] = self.process_img(img['brand_little_img'])
            yield img
        # 爬取产品详情页详情信息
        detail['productId'] = img['productId']
        detail_all = re.search("skuMap\":(.*)},\"valLoginIndicator\"",response.body)        
        detail_data = detail_all.group(1)   
        detail_dict = json.loads(detail_data)
        if len(detail_dict) > 0:
            for letter in detail_dict:
                detail_detail = detail_dict[letter]
                detail['skuId'] = detail_detail['skuId']
                detail['origin_price'] = detail_detail['price']
                detail['stock'] = detail_detail['stock']
                letter = letter.replace(";","")
                if hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/@title").extract():
                    detail_color_name = hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/@title").extract()
                    detail['color_name'] = detail_color_name[0] 
                else:
                    detail['color_name'] = ""
                if hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li[@data-value='"+letter+"']/a/span/text()").extract():
                    detail_standard = hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li[@data-value='"+letter+"']/a/span/text()").extract()
                    detail['standard'] = detail_standard[0]  
                else:
                    detail['standard'] = ""
                if hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/a/@style").extract():
                    detail_little_img = hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/a/@style").extract()
                    re_img = re.search("background:url\(([^)]*)\)",detail_little_img[0])
                    detail['color_little_img'] = re_img.group(1)
                    detail['color_big_img'] = self.process_img(detail['color_little_img'])
                else:
                    detail['color_little_img'] = ""
                    detail['color_big_img'] = ""
                yield detail    
       # origin_price_re = re.search('defaultItemPrice\":\"([^"]*)\",',response.body)
       # product['origin_price'] = origin_price_re.group(1)
    
    def process_img(self,img):
        if img.find("60x60")!=-1:
            img = img.replace("60x60","430x430")
            return img 
        if img.find("40x40")!=-1:
            img = img.replace("40x40","430x430")
            return img
        return img
     
    def process_data(self,data):
        list_dict = []
        for letter in data:
            letter = letter.replace(":","@@")
            letter = letter.replace(u"：","@@")
            aa = letter.split("@@")
            list_dict.append((aa[0],aa[1]))
        json_data = json.dumps(dict(list_dict))  
        json_data = json_data.encode("utf8")
        #json_date = json_data.replace("\\\\","\\") 
        return json_data
   
    def cluo(self,response):
        hxs = HtmlXPathSelector(response)
        url_price = hxs.select("//div[@class='product']/div[@class='product-iWrap']")
        for letter in url_price:
            url_one = letter.select("./div[@class='productImg-wrap']/a[1]/@href").extract()
            price_one = letter.select("./p[@class='productPrice']/em/@title").extract()
            head = response.meta
            head["price"] = price_one[0]
            yield Request("http:"+url_one[0],callback=self.product,meta=head)
 
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
        return self.product(response)
    














