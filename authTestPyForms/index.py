import pyForms.PageController


class controller(pyForms.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "index.html"


	@property
	def username(self):
		if self.page.isLoggedIn:
			return self.page.userData['username']
		else:
			return 'No one...'

	def btnLogout_click(self, ctrls):
		self.page.logout()