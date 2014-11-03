import sessionManager
import userManager
import pyForms.PageController

import urllib
import urllib.parse

class controller(pyForms.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "webpages/login.html"

	def onInit(self, ctrls):
		self.returnURL = None
		if 'returnURL' in self.request.get:
			self.returnURL = self.request.get['returnURL']

		if sessionManager.isAuthenticated(self.request):
			ctrls.pnlDone.visible = True
			ctrls.pnlLogin.visible = False
			if self.returnURL is not None:
				self.page.response.redirect(appendUUIDToURL(self.returnURL, sessionManager.getSession(self.request)))


	def btnLogin_click(self, ctrls):
		if userManager.isValidUser(ctrls.tbxUsername.text, ctrls.tbxPassword.text):
			sessionUUID = sessionManager.setSession(self.request, self.page.request, ctrls.tbxUsername.text)
			if self.returnURL is not None:
				self.page.response.redirect(appendUUIDToURL(self.returnURL, sessionUUID))
			else:
				ctrls.pnlDone.visible = True
				ctrls.pnlLogin.visible = False

		else:
			ctrls.tbxPassword.text = ""
			ctrls.authFail.visible = True
		



def appendUUIDToURL(url, sessionUUID):
	url_parts = list(urllib.parse.urlparse(url))
	query = dict(urllib.parse.parse_qsl(url_parts[4]))
	query['authSessionID'] = sessionUUID

	url_parts[4] = urllib.parse.urlencode(query)

	return urllib.parse.urlunparse(url_parts)





