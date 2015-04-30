#coding:UTF-8

import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("123")


if __name__ == "__main__":
    app = tornado.web.Application(
     handlers = [(r'/',IndexHandler)]

)
    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()
