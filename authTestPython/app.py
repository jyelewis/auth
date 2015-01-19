import tornado.ioloop
import tornado.web
import sys

import auth

def getAuth(self):
	authHandler = auth.RequestAuthenticator("auth.jyelewis.com", "com.jyelewis.testing")
	authHandler.setAuthCookie = lambda value: self.set_cookie("TestAuth", value)
	authHandler.getAuthCookie = lambda		: self.get_cookie("TestAuth", None)
	authHandler.redirectFunction = lambda url: self.redirect(url)
	authHandler.returnURL = "http://localhost:8888"

	if self.get_argument("authSessionID", None) is not None:
		return authHandler if authHandler.handleAuthSessionID(self.get_argument("authSessionID")) else None

	if authHandler.authenticate() is None:
		return None

	return authHandler if authHandler.isAuthenticated else False

class MainHandler(tornado.web.RequestHandler):
	def get(self):
			auth = getAuth(self)
			if auth:
				self.write("Hello, " + auth.user['username'])
			elif auth == False:
				print("denied")
				self.write("403: Access denied")

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
			auth = getAuth(self)
			if auth:
				auth.returnURL = "http://localhost:8888/logout"
				if auth.logout():
					self.redirect("/")
				

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/logout", LogoutHandler),
])

port = sys.argv[1] if len(sys.argv) > 1 else 8888

if __name__ == "__main__":
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()