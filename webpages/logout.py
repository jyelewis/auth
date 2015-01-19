import pyForms.PageControllerClasses

import sessionManager

class controller(pyForms.PageControllerClasses.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "webpages/logout.html"

	def onLoad(self, ctrls):
		returnURL = None
		if 'returnURL' in self.request.get:
			returnURL = self.request.get['returnURL']

		user = sessionManager.getAuthenticatedUser(self.page.request)
		if user is None:
			self.page.response.redirect("/login")
			return
		sessionManager.setSession(self.page.request, self.page.response, user['username'], False)

		if returnURL is not None:
			self.page.response.redirect(returnURL)
		else:
			self.page.response.redirect("/login")