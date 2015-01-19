import json
import uuid
import sys

authSessions = {}

if sys.version_info >= (3,0):
	import urllib
	import urllib.request

	def quote(text):
		return urllib.parse.quote(text)

	def request(url):
		return urllib.request.urlopen(url).read().decode('utf-8')

else:
	def quote(text):
		return urllib2.quote(text)

	import urllib2
	def request(url):
		return urllib2.urlopen(url).read().decode('utf-8')

class RequestAuthenticator:
	def __init__(self, server = None, appID = None):
		self.server = server
		self.appID = appID

		self.setAuthCookie = None
		self.getAuthCookie = None
		self.redirectFunction = None
		self.returnURL = None


	def authenticate(self):
		if self.isAuthenticated:
			return True #already authenticated

		#we know the auth sessionID hasnt come back yet because
		#that gets called before this function
		if self.returnURL is None:
			raise Exception("requestAuthenticator.returnURL not set")
			return False

		self.redirectFunction("http://" + self.server + "/login?returnURL=" + quote(self.returnURL))
		return None


	def handleAuthSessionID(self, authSessionID):
		if self.isAuthenticated:
			return True
		#validate authSessionID
		#try:
		validateURL  = "http://" + self.server + "/validateSession?"
		validateURL += "authSessionID="+quote(authSessionID)
		if self.appID is not None:
			validateURL += "&appID=" + quote(self.appID)

		validateSessionReply = request(validateURL)
		validateSessionReply = json.loads(validateSessionReply)
		#except:
		#	raise Exception("Error occoured while contacting server to validate authSessionID")


		if validateSessionReply['authenticated'] == True:
			#clearly the user currenlty has no authSessionCookie
			authSessionCookieID = str(uuid.uuid4())
			authSessions[authSessionCookieID] =	{
				 'userID': validateSessionReply['userID']
				,'username': validateSessionReply['username']
			}
			self.setAuthCookie(authSessionCookieID)
			self.getAuthCookie = lambda: authSessionCookieID
			self.redirectFunction(self.returnURL)
			return None
		else:
			#we have an unauthenticated user
			return False

	def logout(self):
		self.setAuthCookie("")
		self.redirectFunction("http://" + self.server + "/logout?returnURL=" + quote(self.returnURL))
		return not self.isAuthenticated


	@property
	def isAuthenticated(self):
		try:
			authCookie = self.getAuthCookie()
		except:
			authCookie = False


		return (authCookie is not None and authCookie in authSessions)


	@property
	def user(self):
		try:
			authCookie = self.getAuthCookie()
		except:
			authCookie = None

		if authCookie is None or authCookie not in authSessions:
			return None

		return authSessions[authCookie]





