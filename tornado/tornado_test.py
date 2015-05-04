#coding:UTF-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
import os

#define("port",default=8888,help="run on the given port",type=int)
def return_value():
    return "你在干什么"

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        a = self.get_argument("op","456")
        self.write(a+' hello world!')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("kk.html")

class OptionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cc.html",a="大家好好好好好好")

class BothHandler(tornado.web.RequestHandler):
    def get(self):
        a = "C罗"
        self.render("both.html",a=a,b=return_value())  

class MmHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mm.html") 

if __name__ == "__main__":
  #  tornado.options.parse_command_line()
    app = tornado.web.Application(
         handlers=[(r"/kaka/", IndexHandler),(r"/main/",MainHandler),(r"/cc/",OptionHandler),(r"/both/",BothHandler),(r"/mm/",MmHandler)],
         template_path = os.path.join(os.path.dirname(__file__),"templates"),
         static_path = os.path.join(os.path.dirname(__file__),"static"),
   )
  #  http_server = tornado.httpserver.HTTPServer(app)
  #  http_server.listen(options.port)
    app.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
