import json
import sessionManager
import userManager
import tornado.web

class handler(tornado.web.RequestHandler):
	def get(self):
		authSessionID = self.get_argument('authSessionID', None)
		retObj = {'authenticated': False, 'error': None}
		if authSessionID is None:
			retObj['error'] = 'No authSessionID was provided'
		else:
			if authSessionID in sessionManager.sessions and sessionManager.sessions[authSessionID]['isAuthenticated'] == True:
				retObj['authenticated'] = True
				user = userManager.userByID(sessionManager.sessions[authSessionID]['userID'])
				retObj['username'] = user['username']
				retObj['userID'] = user['userID']

		self.write(json.dumps(retObj))
		self.set_header("Content-Type", "text/plain")