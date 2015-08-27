from common.base import Application
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from applications.url import handlers
from common.jinja2_tornado import JinjaLoader
import os

define("port", default=8090, help="run on the given port", type=int)
tornado.options.parse_command_line()

static_path = os.path.join(os.path.dirname(__file__), "static")
template_path = os.path.join(os.path.dirname(__file__), "templates")
template_loader = JinjaLoader(template_path)

settings = dict(
    template_loader=template_loader,
    template_path=template_path,
    static_path=static_path,
    xsrf_cookies=True,
    xheaders=True,
    cookie_secret="kIr8erDNTQO2tWQFrys+bNi1Q858ykuSsXj4t1MjTIk=",
    login_url='/login',
    debug=True,
)

if __name__ == '__main__':
    try:
        app = Application(handlers, **settings)
        app.listen(options.port)
        http_server = tornado.httpserver.HTTPServer(app)
        tornado.ioloop.IOLoop.current().start()
    except Exception, e:
        print e
