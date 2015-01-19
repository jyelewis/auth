import sessionManager
import userManager
import pyForms.PageControllerClasses

import urllib
import urllib.parse

class controller(pyForms.PageControllerClasses.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "webpages/index.html"

	def onInit(self, ctrls):
		self.returnURL = None
		if 'returnURL' in self.request.get:
			self.returnURL = self.request.get['returnURL']

		self.pageTitle = "Authentication required"
		self.resetValidators = False
		if sessionManager.isAuthenticated(self.request):
			self.pageTitle = "Authentication control panel"
			ctrls.pnlDone.visible = True
			ctrls.pnlLogin.visible = False
			if self.returnURL is not None:
				self.page.response.redirect(appendUUIDToURL(self.returnURL, sessionManager.getSession(self.request)))

	def onLoad(self, ctrls):
		isAuthenticated = sessionManager.isAuthenticated(self.request)
		if isAuthenticated and self.page.request.url.split("?")[0].endswith("login"):
			self.page.response.redirect("/")
		elif not isAuthenticated and not self.page.request.url.split("?")[0].endswith("login"):
			self.page.response.redirect("/login")


		#reset error messages
		ctrls.divOldPasswordErr.visible = False
		ctrls.divPasswordsMatchErr.visible = False


	def onPrerender(self, ctrls):
		if self.resetValidators:
			ctrls.valTbxPasswordOld.isValid = True
			ctrls.valTbxPassword1.isValid = True
			ctrls.valTbxPassword2.isValid = True

		self.resetVaildators = False

		#reset password boxes
		ctrls.tbxPasswordOld.text = ""
		ctrls.tbxPassword1.text = ""
		ctrls.tbxPassword2.text = ""


	def btnLogin_click(self, ctrls):
		if userManager.isValidUser(ctrls.tbxUsername.text, ctrls.tbxPassword.text):
			sessionUUID = sessionManager.setSession(self.request, self.page.response, ctrls.tbxUsername.text, True, ctrls.chkRememberMe.checked)
			if self.returnURL is not None:
				self.page.response.redirect(appendUUIDToURL(self.returnURL, sessionUUID))
			else:
				self.page.response.redirect("/")
		else:
			ctrls.tbxPassword.text = ""
			ctrls.authFail.visible = True

	@property
	def username(self):
		user = sessionManager.getAuthenticatedUser(self.request)
		if user:
			return user['username']
		else:
			return ""

	#control panel button handlers
	def btnLogout_click(self, ctrls):
		self.page.response.redirect("/logout")

	def btnChangePassword_click(self, ctrls):
		ctrls.pnlChangePassword.visible = True
		ctrls.pnlAccountButtons.visible = False

	def btnCancelChangePassword_click(self, ctrls):
		ctrls.pnlChangePassword.visible = False
		ctrls.pnlAccountButtons.visible = True
		self.resetValidators = True

	def btnSavePassword_click(self, ctrls):
		user = sessionManager.getAuthenticatedUser(self.request)

		if user['password'] != ctrls.tbxPasswordOld.text:
			ctrls.divOldPasswordErr.visible = True
			return

		if ctrls.tbxPassword1.text != ctrls.tbxPassword2.text:
			ctrls.divPasswordsMatchErr.visible = True
			return

		#password can be changed
		userManager.changePassword(user['userID'], ctrls.tbxPassword1.text)
		self.btnCancelChangePassword_click(ctrls)



def appendUUIDToURL(url, sessionUUID):
	url_parts = list(urllib.parse.urlparse(url))
	query = dict(urllib.parse.parse_qsl(url_parts[4]))
	query['authSessionID'] = sessionUUID

	url_parts[4] = urllib.parse.urlencode(query)

	return urllib.parse.urlunparse(url_parts)





