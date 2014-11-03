import sys

import pyForms
import tornado

import index
controllerPage = pyForms.Page(index.controller)

#START WEB SERVERY STUFF
import tornado.ioloop
import tornado.web


application = tornado.web.Application([
    (r"/", pyForms.tornadoHandler(controllerPage)),
])

portNumber = sys.argv[1] if len(sys.argv) > 1 else 8888
application.listen(portNumber)
tornado.ioloop.IOLoop.instance().start()