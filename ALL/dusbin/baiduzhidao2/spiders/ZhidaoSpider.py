#coding=utf-8
import sys,re
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Response, Request
from baiduzhidao.items import ZhidaoQuestion,ZhidaoAnswer,RelatedQuestion,QuestionPic,AnswerPic, QuestionViewNum,RelatedTopic
from datetime import datetime
from .urlData import *
from .spider_common import *
import json as json_mod
from scrapy import signals,log
import urllib

class ZhidaoSpider(BaseSpider):
        name = "zhidao"
        allowed_domains = ["zhidao.baidu.com"]

	#url match pattern
        detail_page_pattern = re.compile(r'zhidao.baidu.com/question/([0-9]+).html')
	view_num_url_pattern = re.compile(r'cp.zhidao.baidu.com/v.php\?q=([0-9]+)')
        html_tag_pattern = re.compile(r'<[^>]+>')
	url_prefix = 'zhidao.baidu.com/question/'
        have_fetch_set=set()
        #construct the request from the start utls
        def start_requests(self):
                for url in start_urls:
                        yield self.make_requests_from_url(url)

        def parse_list_page(self, response):
                hxs = HtmlXPathSelector(response)
		meta=response.meta
		if not meta.get("keyword"):
			keyword_pattern = re.compile(r'zhidao.baidu.com/search\?word=(.+)')
			keyword = keyword_pattern.search(response.url).group(1)
			meta["keyword"]=unicode(urllib.unquote(keyword),"gbk")
                for url in hxs.select('.//a[@class="ti"]/@href').extract():
                        yield Request(url,meta = meta,callback = self.parse_detail_page,priority = 5)
                for url in hxs.select('.//div[@class="pager"]/a/@href').extract():
                        newUrl="http://zhidao.baidu.com"+url
			if not (newUrl in self.have_fetch_set):
				self.have_fetch_set.add(newUrl)
	                	yield Request(newUrl,meta = meta,callback = self.parse_list_page,priority = 5)
		
		
	def parse_viewnum_page(self, response):
        	questionId = self.view_num_url_pattern.search(response.url).group(1)
		viewNumInfo = QuestionViewNum()
		viewNumInfo['questionId'] = questionId
		viewNumInfo['viewNum'] = response.body
		yield viewNumInfo

	def parse_detail_page(self,response):
		hxs = HtmlXPathSelector(response)
                questionId = self.detail_page_pattern.search(response.url).group(1)
                guide = ZhidaoQuestion()
                title = first_item(hxs.select('.//span[@class="ask-title  "]/text()').extract())
                if not title:
                        return
                guide['title'] =  title.strip()
		guide['content'] =  "\n".join(hxs.select('.//pre[@class="line mt-10 q-content"]/text()').extract())

		if not guide['content']:
                        guide['content'] =  "\n".join(hxs.select('.//div[@class="line mt-10 q-content"]/p/text()').extract())
		
		guide['supplyContent'] =  first_item(hxs.select('.//pre[@class="line mt-10 q-supply-content"]/text()').extract())
		if not guide['supplyContent']:
                        guide['supplyContent'] =  "\n".join(hxs.select('.//div[@class="line mt-10 q-supply-content"]/p/text()').extract())
                
		guide['category'] =  first_item(hxs.select('.//div[@id="ask-info"]/span/a[@class="f-aid"]/text()').extract())
                guide['userName'] =  first_item(hxs.select('.//div[@id="ask-info"]/a[@class="user-name"]/text()').extract())
                guide['time'] = first_item(hxs.select('.//span[@class="grid-r ask-time"]/text()').extract())
                guide['questionId'] = questionId
                guide['url'] = response.url
		guide['keyword']=response.meta["keyword"]	
                yield guide
		
		for picUrl in hxs.select('//div[@id="wgt-ask"]/div/p/a/@href').extract():
			qp = QuestionPic()
			qp['questionId'] = questionId
			qp['picUrl'] = picUrl
			yield qp
		
		newUrl="http://cp.zhidao.baidu.com/v.php?q="+questionId
		yield Request(newUrl,callback = self.parse_viewnum_page,priority = 3)

		ba = hxs.select('.//div[@class="wgt-best "]')
		if ba:
			ba=ba[0]
			best=ZhidaoAnswer()
			best['questionId'] = questionId
			best['isBest'] = 1
			best['content'] = "\n".join(ba.select('.//div[@class="bd answer"]/div[@class="line content"]/pre/text()').extract())
			if not best['content']:
                                best['content'] =  "\n".join(ba.select('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/text()').extract())

			best['userName'] =  first_item(ba.select('..//div[@class="bd answer"]/div/div/p/a[@class="user-name"]/text()').extract())
                        if not best['userName']:
                                best['userName'] =  u"热心网友"
                        best['time'] =  ba.select('..//div[@class="hd line mb-10"]/span[@class="grid-r f-aid pos-time mt-20"]/text()').extract()[1].strip()
                        best['likeNum'] =  first_item(ba.select('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@data-evaluate').extract())
                        best['answerId'] = first_item(ba.select('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@id').re('evaluate-([0-9]+)'))
			yield best
			for picUrl in ba.select('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/a/@href').extract():
                                bap = AnswerPic()
                                bap['answerId'] = best['answerId']
                                bap['picUrl'] = picUrl
                                yield bap
	
		ra = hxs.select('.//div[@class="wgt-recommend "]')
                if ra:
                        ra=ra[0]
                        best=ZhidaoAnswer()
                        best['questionId'] = questionId
                        best['isBest'] = 2
                        best['content'] = "\n".join(ra.select('.//div[@class="bd answer"]/div[@class="line content"]/pre/text()').extract())
                        if not best['content']:
                                best['content'] =  "\n".join(ra.select('.//div[@class="bd answer"]/div/div[@class="recommend-text mb-10"]/p/text()').extract())

                        best['userName'] =  first_item(ra.select('..//div[@class="bd answer"]/div/div/p/a[@class="user-name"]/text()').extract())
                        if not best['userName']:
                                best['userName'] =  u"热心网友"
                        best['time'] =  ra.select('..//div[@class="hd line mb-10"]/span[@class="grid-r f-aid pos-time mt-20"]/text()').extract()[1].strip()
                        best['likeNum'] =  first_item(ra.select('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@data-evaluate').extract())
                        best['answerId'] = first_item(ra.select('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@id').re('evaluate-([0-9]+)'))
                        yield best
                        for picUrl in ra.select('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/a/@href').extract():
                                bap = AnswerPic()
                                bap['answerId'] = best['answerId']
                                bap['picUrl'] = picUrl
                                yield bap
	
		for node in hxs.select('//div[@id="wgt-answers"]/div/div[@class="line"]/div[contains(@class,"content")]'):
			answer = ZhidaoAnswer()
			answer['questionId'] = questionId
			answer['content']= "\n".join(node.select('.//pre/text()').extract())
			if not answer['content']:
	                        answer['content'] =  "\n".join(node.select('.//div[@class="answer-text mb-10"]/p/text()').extract())
			answer['userName'] =  first_item(node.select('..//div/a[@class="user-name"]/text()').extract())
			if not answer['userName']:
				answer['userName'] =  u"热心网友"
			answer['time'] =  node.select('..//div/span[@class="grid-r pos-time"]/text()').extract()[1].strip()
			answer['likeNum'] =  first_item(node.select('.//div/span[@class="evaluate"]/@data-evaluate').extract())
			answer['answerId'] =  first_item(node.select('.//div/span[@class="evaluate"]/@id').re('evaluate-([0-9]+)'))
			answer['isBest'] = 0 
			yield answer
			for picUrl in node.select('.//div[@class="answer-text mb-10"]/p/a/@href').extract():
	                        ap = AnswerPic()
        	                ap['answerId'] = answer['answerId']
                	        ap['picUrl'] = picUrl
                        	yield ap	
		
		for node in hxs.select('//div[@id="wgt-related"]/div/ul/li'):
                        rq = RelatedQuestion()
                        rq['questionId'] = questionId
			rq['relatedId'] = first_item(node.select('.//a/@data-qid').extract())
                        rq['time'] =  first_item(node.select('.//span/text()').extract())
                        rq['title'] =  self.html_tag_pattern.sub("",first_item(node.select('.//a').extract()))
			rq['likeNum'] = first_item(node.select('.//em/span/text()').extract())
			if not rq['likeNum']:
				rq['likeNum'] = 0
                        yield rq

		for node in hxs.select('//div[@id="wgt-topic"]/ul/li'):
                        rq = RelatedTopic()
                        rq['questionId'] = questionId
                        rq['relatedId'] = first_item(node.select('.//a/@href').re('([0-9]+).html'))
                        rq['time'] =  first_item(node.select('.//span[@class="grid-r f-aid"]/text()').extract())
                        rq['title'] =  first_item(node.select('.//a/text()').extract()).strip()
                        rq['likeNum'] = first_item(node.select('.//span[@class="ml-5 f-red"]/text()').extract())
                        if not rq['likeNum']:
                                rq['likeNum'] = 0
                        yield rq
        def parse(self, response):
                return self.parse_list_page(response)
