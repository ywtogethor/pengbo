#encoding=UTF-8
import codecs
import string
import datetime
import sys
import os
import httplib
import string
import re
import time

gQuestionResultSql = 'update dbn_products set questionNum=%s where id=%s;\n'
gTopicResultSql = 'update dbn_products set topicNum=%s where id=%s;\n'
gSpiderTaskResultSql = 'insert into zhidao_spider_task(keyword,productId,fetchStatus,sourceId) values (\'%s\',%s,0,1);\n'
result_path = "/data/db_api/"
result_file = file(result_path + "product_question_cnt.sql", 'w')
spider_task_result_file = file(result_path + "product_spider_task.sql", 'w')

class Product:
  product_id_ = ""
  product_name_ = ""
  def Stem(self):
    self.product_name_ = self.product_name_\
                         .replace("\\([^)]*\\)", "")\
                         .replace("\\([^）]*）", "") \
                         .replace("（[^)]*\\)", "")\
                         .replace("（[^）]*）", "")\
                         .replace("【[^】]*】", "")\
                         .strip();

# 加载产品数据
def LoadProducts(filename):
  input_file = open(filename)
  product_id = input_file.readline()
  product_name = input_file.readline()
  while product_id and product_name:
    pro = Product()
    pro.product_id_ = product_id.replace("\n", "").replace("\r", "")
    pro.product_name_ = product_name.replace("\n", "").replace("\r", "")
    pro.Stem()
    GetProductAnswerCnt(pro); 
    time.sleep(1)
    product_id = input_file.readline()
    product_name = input_file.readline()
  result_flag_file = file(result_path + "finish.flag", 'w')
  result_flag_file = file(result_path + "spider.flag", 'w')
  result_flag_file.write(str(time.strftime(ISOTIMEFORMAT, time.localtime())))
  result_flag_file.close()
  print ">>>>>>>>>>>>>>>>>处理产品数量：" + str(len(kAllProducts)) + "个>>>>>>>>>>>>>>>>>" 

# 读取问题，并关联产品
def GetProductAnswerCnt(product):
  try:
    httpClient = httplib.HTTPConnection('api.dabanniu.com', 80, timeout = 10)
    product_api_url = '/v2/getRelatedContentByProduct.do?productId=' + str(product.product_id_)
    httpClient.request('GET', product_api_url)
    response = httpClient.getresponse()
    data = response.read()
    #print data
    match = re.search(r'totalNumber":(.*?),', data)
    topic_num_match = re.search(r'topicNumber":(.*?),', data)
    if match:
      question_cnt = match.group(1)
      #print str(question_cnt) 
      if question_cnt != 0 and question_cnt != '0':
        result_file.write(gQuestionResultSql % (question_cnt, product.product_id_))
      else:
        spider_task_result_file.write(gSpiderTaskResultSql % (product.product_name_, product.product_id_))
    
    if topic_num_match:
      topic_cnt = topic_num_match.group(1)
      if topic_cnt != 0 and topic_cnt != '0':
        result_file.write(gTopicResultSql % (topic_cnt, product.product_id_))
      result_file.flush()
  except Exception,e:
    print e
  
# main
if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding('UTF-8')
  LoadProducts(result_path + "products.data")
  result_file.close()
  spider_task_result_file.close()
