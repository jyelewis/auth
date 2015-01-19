import json
import sessionManager
import userManager
import tornado.web

class handler(tornado.web.RequestHandler):
	def get(self):
		authSessionID = self.get_argument('authSessionID', None)
		appID = self.get_argument('appID', None)
		retObj = {'authenticated': False, 'error': None}

		if authSessionID is None:
			retObj['error'] = 'No authSessionID was provided'
		else:
			userID = sessionManager.sessions[authSessionID]['userID']
			if authSessionID in sessionManager.sessions \
				and sessionManager.sessions[authSessionID]['isAuthenticated'] == True \
				and (appID is None or userManager.userIsAllowedApp(userID, appID)):

				retObj['authenticated'] = True
				user = userManager.userByID(userID)
				retObj['username'] = user['username']
				retObj['userID'] = user['userID']

		self.write(json.dumps(retObj))
		self.set_header("Content-Type", "text/plain")