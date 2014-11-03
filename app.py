import sys

import pyForms
import tornado.ioloop
import tornado.web

import webpages.login
loginPage = pyForms.Page(webpages.login.controller)

import validateSession


application = tornado.web.Application([
    (r"/login", pyForms.tornadoHandler(loginPage)),
    (r"/validateSession", validateSession.handler)
    
])

portNumber = sys.argv[1] if len(sys.argv) > 1 else 8888
application.listen(portNumber)
tornado.ioloop.IOLoop.instance().start()




