# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi 
import MySQLdb  
import MySQLdb.cursors
from scrapy import log
from baiduzhidao.items import ZhidaoQuestion,ZhidaoAnswer,RelatedQuestion,QuestionPic,AnswerPic, QuestionViewNum,RelatedTopic
class BaiduzhidaoPipeline(object):
	def __init__(self):  
		self.dbpool = adbapi.ConnectionPool('MySQLdb',  
					db = 'zhidao',  
					user = 'root',  
					passwd = 'applen_(0)',
			host='112.124.53.109',  
			cursorclass = MySQLdb.cursors.DictCursor,  
			charset = 'utf8',  
					use_unicode = True  
		) 
	def process_item(self, item, spider):
		if not item : return None
		if isinstance(item,ZhidaoQuestion):
			query = self.dbpool.runInteraction(self._question_insert, item)
		elif isinstance(item,ZhidaoAnswer):
			query = self.dbpool.runInteraction(self._answer_insert, item)
		elif isinstance(item,RelatedQuestion):
			query = self.dbpool.runInteraction(self._related_question_insert, item)
		elif isinstance(item,RelatedTopic):
			query = self.dbpool.runInteraction(self._related_topic_insert, item)
		elif isinstance(item,QuestionPic):
			query = self.dbpool.runInteraction(self._question_pic_insert, item)
		elif isinstance(item,AnswerPic):
			query = self.dbpool.runInteraction(self._answer_pic_insert, item)
		elif isinstance(item,QuestionViewNum):
			query = self.dbpool.runInteraction(self._question_view_update, item)
		query.addErrback(self.handle_error)  
		return item 


	def _question_insert(self, tx, item):
		if item.get('questionId'):
			tx.execute(
					"insert into  `question` (  `questionId`,  `url`,  `title`,  `content`,  `supplyContent`,  `category`,  `userName`,  `time`,`keyword`) values(%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s )",
						(item['questionId'],item['url'],item['title'],item['content'],item['supplyContent'],item['category'],item['userName'],item['time'],item['keyword'])
			)

	def _answer_insert(self, tx, item):
		if item.get('questionId'):
			tx.execute(
				"insert into  `answer` (`answerId`,`questionId`,`likeNum`,`content`,`userName`,`time`,`isBest`) values(%s ,%s ,%s ,%s ,%s ,%s,%s)",
                                (item['answerId'],item['questionId'],item['likeNum'],item['content'],item['userName'],item['time'],item['isBest'])
			)

	def _related_question_insert(self, tx, item):
		if item.get('questionId'):
			tx.execute(
				"insert into  `relatedQuestion` (  `relatedId`,  `questionId`,  `likeNum`,  `title`,  `time`) values(%s ,%s ,%s ,%s ,%s )",
				(item['relatedId'],item['questionId'],item['likeNum'],item['title'],item['time'])
			)
			
	def _related_topic_insert(self, tx, item):
		if item.get('questionId'):
			tx.execute(
				"insert into  `relatedTopic` (  `relatedId`,  `questionId`,  `likeNum`,  `title`,  `time`) values(%s ,%s ,%s ,%s ,%s )",
				(item['relatedId'],item['questionId'],item['likeNum'],item['title'],item['time'])
			)
			
	def _question_pic_insert(self, tx, item):
		if item.get('questionId'):
			tx.execute(
				"insert into  `questionPic` (  `questionId`,  `picUrl`) values(%s ,%s)",
				(item['questionId'],item['picUrl'])
			)
			
	def _answer_pic_insert(self, tx, item):
		if item.get('answerId'):
			tx.execute(
				"insert into  `answerPic` (  `answerId`,  `picUrl`) values(%s ,%s)",
				(item['answerId'],item['picUrl'])
			)
			
	def _question_view_update(self, tx, item):
		if item.get('questionId'):
			tx.execute(
				"update `question` set  `viewNum` = %s where `questionId` = %s",
				(item['viewNum'],item['questionId'])
			)
			
	def handle_error(self, e):
		log.err(e)	 

