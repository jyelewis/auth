import sys

import pyForms
import tornado.ioloop
import tornado.web

import webpages.index
indexPage = pyForms.Page(webpages.index.controller)

import webpages.logout
logoutPage = pyForms.Page(webpages.logout.controller)

import validateSession


application = tornado.web.Application([
	(r"/", pyForms.tornadoHandler(indexPage)),
    (r"/login", pyForms.tornadoHandler(indexPage)),
    (r"/logout", pyForms.tornadoHandler(logoutPage)),
    (r"/validateSession", validateSession.handler),
    (r'/Resources/(.*)', tornado.web.StaticFileHandler, {'path': "Resources/"})
])

portNumber = sys.argv[1] if len(sys.argv) > 1 else 8888
application.listen(portNumber)
tornado.ioloop.IOLoop.instance().start()




