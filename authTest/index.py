import pyForms.PageController

import auth

class controller(pyForms.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "index.html"

	@auth.requireAuthentication
	def onLoad(self):
		pass

	@property
	def username(self):
		if auth.isLoggedIn(self):
			return auth.getUserdata(self)['username']
		else:
			return 'No one...'