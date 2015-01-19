import sys

import pyForms
import tornado

pyForms.auth.server = "auth.jyelewis.com"
pyForms.auth.appID = "com.jyelewis.testing"

import index
controllerPage = pyForms.Page(index.controller, True) #controller, requireAuth

#START WEB SERVERY STUFF
import tornado.ioloop
import tornado.web


application = tornado.web.Application([
    (r"/", pyForms.tornadoHandler(controllerPage)),
])

portNumber = sys.argv[1] if len(sys.argv) > 1 else 8888
application.listen(portNumber)
tornado.ioloop.IOLoop.instance().start()