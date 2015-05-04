#coding:UTF-8
from scrapy.http import Request,Response
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider 
from scrapy.log import err
import re
import json
import HTMLParser
from tmall_fp_product.items import ProductCommonItem,ProductImgItem,ProductDetailItem,ProductSizeItem,ProductSaleValueItem


class TmallFpProductSpider(BaseSpider): 
    name = "tmall_fp_product"
    allow_domain = ["tmall"]
    start_urls = ["http://better.tmall.hk/search.htm"]
    seller_name = ["better","purplelabel","qcf69","sukistar","hkyuhe"]

    def product(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        html_parser = HTMLParser.HTMLParser()
        common = ProductCommonItem()
        img = ProductImgItem()
        detail = ProductDetailItem()
        # 爬取产品详情页公共信息
        re_product_url = re.search("id=([0-9]+)",response.url)
        #re_cat_url = re.search("cat_id=([0-9]+)",response.url)
        common['productId'] = re_product_url.group(1)
        #common['catId'] = re_cat_url.group(1)
    #    common['taskId'] = hea['taskId']
        common['url'] = response.url
        common_send_address = hxs.select("//input[@name='region']/@value").extract()
        if common_send_address:
            common['send_address'] = common_send_address[0]
        else:
            common['send_address'] = ""
        common_name = hxs.select("//input[@name='title']/@value").extract()
        if common_name:
            common['name'] = html_parser.unescape(common_name[0])
        else:
            common['name'] = ""
        re_brand = re.search("brand\":\"([^,]*)\"",response.body)
        if re_brand:
            common_brand= re_brand.group(1)
            common['brand'] = html_parser.unescape(common_brand)
        else:
            common['brand'] = ""
        common_description = hxs.select("//div[@class='tb-detail-hd']/p/text()").extract()
        if common_description:
            common['description'] = common_description[0].strip()
        else:
            common['description'] = ""
        common_parameter = hxs.select("//ul[@id='J_AttrUL']/li/text()").extract()
        if  common_parameter:
            common['parameter'] = self.process_data(common_parameter)
        else:
            common['parameter'] = ""
        common["shop_name"] = hea["seller_shop_name"]
        yield common
        # 爬取产品详情页品牌图片
        img['productId'] = common['productId']
       # img['taskId']= common['taskId']
        brand_little_img_list = hxs.select("//ul[@class='tb-thumb tm-clear']/li")
        for letter in brand_little_img_list:
            brand_little_img = letter.select("./a/img/@src").extract()
            if brand_little_img:
                img['brand_little_img'] = brand_little_img[0]
                img['brand_big_img'] = self.process_img(img['brand_little_img'])
            else:
                img['brand_little_img'] = ""
                img['brand_big_img'] = ""
            yield img
        # 爬取产品详情页详情信息
        detail['productId'] = img['productId']
       # detail['taskId'] = img['taskId']
        detail_all = re.search("skuMap\":(.*)},\"valLoginIndicator\"",response.body)
        if detail_all:
            detail_data = detail_all.group(1)
            detail_dict = json.loads(detail_data)
            for letter in detail_dict:
                detail_detail = detail_dict[letter]
                detail['skuId'] = long(detail_detail['skuId'])
                detail['origin_price'] = detail_detail['price']
                detail['stock'] = int(detail_detail['stock'])
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
        else:
            detail['skuId'] = 0
            detail_origin_price = re.search('defaultItemPrice\":\"([^"]*)\",',response.body)
            if detail_origin_price:
                detail['origin_price'] = detail_origin_price.group(1)
            else:
                detail['origin_price'] = 0
            detail_stock = re.search('quantity\":([0-9]*),',response.body)
            if detail_stock:
                detail['stock'] = detail_stock.group(1)
            else:
                detail['stock'] = 0
            detail['standard'] = ""
            detail['color_name'] = ""
            detail['color_little_img'] = ""
            detail['color_big_img'] = ""
            yield detail

    def process_img(self,img):
        if img.find("60x60")!=-1:
            img = img.replace("60x60","430x430")
            return img
        if img.find("40x40")!=-1:
            img = img.replace("40x40","430x430")
            return img
        return img
    def process_data(self,data):
        html_parser = HTMLParser.HTMLParser()
        data = html_parser.unescape(data)
        list_dict = []
        for letter in data:
            letter = letter.replace(":","@@")
            letter = letter.replace(u"：","@@")
            aa = letter.split("@@")
            list_dict.append((aa[0],aa[1]))
        json_data = json.dumps(dict(list_dict), ensure_ascii=False)
        return json_data

    def parse_product_list(self,response):
        head = response.meta
        hxs = HtmlXPathSelector(response)
        product_detail_url = hxs.select("//dd[@class='thumb']/../dt[@class='photo']/a/@href").extract()
        for letter in product_detail_url:
            yield Request("http:"+letter,callback=self.product,meta=head)
    
   
    def get_product_page(self,response):
        err("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        hea = response.meta
        hxs = HtmlXPathSelector(response)
        list_page_num = hxs.select("//b[@class='ui-page-s-len']/text()").extract()
        list_page_num = list_page_num[0].split("/")[1] 
        for le in range(1,int(list_page_num)+1):
            product_list_url = hea["list_url"] + "?pageNo=" + str(le)
            yield Request(product_list_url,callback=self.parse_product_list,meta=hea)

        

    def product_list(self,response):
        err("**************************")
        head = response.meta
        for letter in self.seller_name:
            list_url = "http://"+letter+".tmall.hk/search.htm"
            head["list_url"] = list_url
            head["seller_shop_name"] = self.get_seller_shop_name(letter)
            yield  Request(list_url,callback=self.get_product_page,meta=head)
    
    def get_seller_shop_name(self,data):  
        if data == "purplelabel":
            return "紫色标签海外专营店"
        if data == "better":
            return "蓓佳海外专营店"
        if data == "qcf69":
            return "台北浅草风海外专营店"
        if data == "sukistar":
            return "采妍国际海外旗舰店"
        if data == "hkyuhe":
            return "喻贺化妆品海外专营店"
    
  
    def parse(self,response):
        err("==============================")
        return self.product_list(response)
