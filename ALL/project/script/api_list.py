#coding:UTF-8
import requests

url = "api.dabanniu.com/v2/listFeatureTopicComments.do"
params = {"featureTopicId":260,"rCommentId":0,"pre":20,"mark":0}
response = requests.request("get",url,params = params)
print response.text
