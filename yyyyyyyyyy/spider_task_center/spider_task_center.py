import tornado.ioloop
import tornado.web
import torndb
import json
from urllib import unquote

#*/1 * * * * sh /usr/local/services/spider_task_center/tools/run_spider_task_center.sh &
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("index.html", title="Spider Task Center", items=items)

class InsertTempHandler(tornado.web.RequestHandler):
    def get(self):
        sql = self.get_argument("sql")
        sql = unquote(sql)
        #sql = sql.replace('\'','\\\'').replace(', "',', \'').replace('", ','\', ').replace('");','\');')
        db.execute(sql)

class GetTaskHandler(tornado.web.RequestHandler):
    def get(self):
        spider_name = self.get_argument("spider_name")
        spider_type = self.get_argument("spider_type")
        if not spider_name:
            self.write(403)
        task_list = None

        if spider_type == "zhidao" and spider_name == "spider_test":
            task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=1 order by weight desc,id asc limit 1")
#           task_list = db.query("select id as taskId,productId,keyword from zhidao_spider_task where fetchStatus=0 order by rand() desc limit 1")
            for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"]) 
                db.execute(sub_sql)
                print sub_sql

        if spider_type == "zhidao" and spider_name != "spider_test":
            task_list = db.query("select id as taskId,productId,keyword from zhidao_spider_task where fetchStatus=0 and sourceId=1 and type=1 order by weight desc,id asc limit 1")
#           task_list = db.query("select id as taskId,productId,keyword from zhidao_spider_task where fetchStatus=0 order by rand() desc limit 1")
            for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"]) 
                db.execute(sub_sql)
                print sub_sql

        if spider_type == "kimissValue":
            task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=2 order by weight desc,id asc limit 1")
            for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"]) 
                db.execute(sub_sql)
                print sub_sql

        if spider_type == "lefeng_product" and spider_name == "spider1":
            task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=3 order by weight desc,id asc limit 1")
            for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"]) 
                db.execute(sub_sql)
                print sub_sql
	if spider_type == "jumeiProduct" and spider_name == "spider2" :
           task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=4 order by weight desc,id asc limit  1")
           for task in task_list:
                 sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"])
                 db.execute(sub_sql)
                 print sub_sql
        if spider_type == "tmall":
           task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=9 order by weight desc,id asc limit 1")
           for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"])
                db.execute(sub_sql)
                print sub_sql
        if spider_type == "tmall_fp_product" and spider_name != "spider100":
           task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=10 order by weight desc,id asc limit 1")
           for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"])
                db.execute(sub_sql)
                print sub_sql
        if spider_type == "tmall_fp_product" and spider_name == "spider100":
           task_list = db.query("select id as taskId,productId,keyword,type from zhidao_spider_task where fetchStatus=0 and sourceId=20 order by weight desc,id asc limit 1")
           for task in task_list:
                sub_sql='update zhidao_spider_task set fetchStatus=1,spiderName="%s" where id="%s"'%(spider_name,task["taskId"])
                db.execute(sub_sql)
                print sub_sql


        self.write(json.dumps(task_list))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/gettask", GetTaskHandler),
    (r"/insertTemp", InsertTempHandler),
])

if __name__ == "__main__":
    db=torndb.Connection("182.92.67.121", "zhidao", "root", "applen_(0)")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
