server = "local.jyelewis.com:8090"

import urllib
import urllib.request
import urllib.parse
import json

def requireAuthentication(func):
	def onLoad_withAuth(self, ctrls):
		def showLogin():
			self.page.response.redirect("http://" + server + "/login?returnURL=" + urllib.parse.quote(self.request.url))

		if 'authSessionID' in self.request.get and 'auth_userdata' not in self.request.session:
			#get user data here
			try:
				validateSessionReply = urllib.request.urlopen("http://"+server+"/validateSession?authSessionID="+urllib.parse.quote(self.request.get['authSessionID'])).read().decode('utf-8')
				validateSessionReply = json.loads(validateSessionReply)
			except:
				showLogin()
				return

			if validateSessionReply['authenticated'] == True:
				self.request.session['auth_userdata'] =	{
					 'userID': validateSessionReply['userID']
					,'username': validateSessionReply['username']
				}
				#get rid of the get paremeter
				url_parts = list(urllib.parse.urlparse(self.request.url))
				query = dict(urllib.parse.parse_qsl(url_parts[4]))
				if 'authSessionID' in query:
					del query['authSessionID']

				url_parts[4] = urllib.parse.urlencode(query)
				print(urllib.parse.urlunparse(url_parts))
				self.page.response.redirect(urllib.parse.urlunparse(url_parts))


			else:
				showLogin()
				return


		if 'auth_userdata' not in self.request.session: #is touple (userID, username)
			showLogin()
		else:
			func(ctrls)

	return onLoad_withAuth

def getUserdata(pageController):
	if 'auth_userdata' in pageController.request.session:
		return pageController.request.session['auth_userdata']
	return None

def isLoggedIn(pageController):
	return 'auth_userdata' in pageController.request.session