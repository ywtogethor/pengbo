#coding:UTF-8
import os.path
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define,options

define("port",default=7999,help="run on the given port",type=int)

class PaperHandler_a(tornado.web.RequestHandler):
    def get(self):
        self.render("paper_a.html")

class Paperhandler_b(tornado.web.RequestHandler):
    def get(self):
        self.render("paper_b.html",aa="123",bb=456)
#class IndexHandler(tornado.web.RequestHandler):
#    def post(self):
#        num1=self.get_argument("num1")
#        num2=self.get_argument("num2")
#        num3=self.get_argument("num3")
#        num4=self.get_argument("num4")
#        self.render("index.html",aa=num1,bb=num2,cc=num3,dd=num4)

class PaperModule_a(tornado.web.UIModule):
    def render(self):
        return "<h1>hello world!</h1>"
class PaperModule_b(tornado.web.UIModule):
    def render(self):
        return "<h2>hello world!</h2>"
def main():
    tornado.options.parse_command_line()
    application=tornado.web.Application(handlers=[(r"/",PaperHandler_a),(r"/a",Paperhandler_b)],
           template_path=os.path.join(os.path.dirname(__file__),"templates"),
           static_path=os.path.join(os.path.dirname(__file__),"static"),
           ui_modules={'hello_a':PaperModule_a,'hello_b':PaperModule_b}
)  
    http_server=tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__=="__main__":
    main()
