#coding:UTF-8
import sys
import time
import os
import logging
import django

def read_log(date):
    keyword_tuple_list =[]
    log_file = "/data/log/dbn-"+date+".log"
    resource=open(log_file)
    content=resource.readline()
    while content:
        if "keyword" in content:
            re_keyword = re.search("\"keyword\":\"([^,]+)\"",content)   
            re_userId = re.search("([^|]+)\|/[^|]+\.do",content) 
            keyword_result = re_keyword.group(1)
            userId_result = re_userId.group(1)
            if keyword_result!=" " and userId_result!='null':
                keyword_userId = (keyword_result,userId_result) 
                keyword_tuple_list.append(keyword_userId)
        content=resource.readline()
    remove_repeat(keyword_tuple_list,date)


def remove_repeat(parameter,date):
    keyword_list = []
    keyword_norepeat_tuple_list = list(set(parameter))
    for keyword in keyword_norepeat_tuple_list:
        keyword_list.append(keyword[0])
    search_insert(keyword_list,date)

def search_insert(parameter,date):
    num = 0
    keyword_norepeat_list = list(set(parameter))
    print keyword_norepeat_list
    for letter in keyword_norepeat_list:
        for le in parameter:
            if le == letter:
                num+=1
        p = SearchStat(keyword=letter,number=num,date=date)
        p.save()
        num = 0
    
if __name__=="__main__" :
    os.environ['DJANGO_SETTINGS_MODULE'] = sys.argv[2]
    currentdir = os.path.dirname(__file__)
    parrentdir = os.path.dirname(os.path.dirname(currentdir))
    sys.path.append(parrentdir)

    from apps.search.models import SearchStat 
    django.setup()
   # date = time.strftime('%Y%m%d',time.localtime))
    read_log(sys.argv[1])
   # logger = logging.getLogger("kaka")
   # logger.setLevel(logging.INFO)
   # handler = logging.FileHanlder("/data/log/new.log",'w')
   # formatter =logging.Formatter('%(asctime)s - %(name)s -%(levelname)s -%(message)s')
   # handler.setFormatter(formatter)
   # logger.addHandler(handler)
    


           
