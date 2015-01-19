server = None
appID = None

import urllib
import urllib.request
import urllib.parse
import json

def authenticateRequest(request, response):
	if server is None:
		raise Exception("auth.server was not set")

	#authenticate request ----------------------------------------------------------
	def showLogin():
		response.redirect("http://" + server + "/login?returnURL=" + urllib.parse.quote(request.url))

	if 'authSessionID' in request.get and 'auth_userdata' not in request.session:
		#get user data here
		try:
			validateURL  = "http://"+server+"/validateSession?"
			validateURL += "authSessionID="+urllib.parse.quote(request.get['authSessionID'])
			if appID is not None:
				validateURL += "&appID="+urllib.parse.quote(appID)

			validateSessionReply = urllib.request.urlopen(validateURL).read().decode('utf-8')
			validateSessionReply = json.loads(validateSessionReply)
		except:
			showLogin()

		if validateSessionReply['authenticated'] == True:
			request.session['auth_userdata'] =	{
				 'userID': validateSessionReply['userID']
				,'username': validateSessionReply['username']
			}
			#get rid of the get paremeter
			url_parts = list(urllib.parse.urlparse(request.url))
			query = dict(urllib.parse.parse_qsl(url_parts[4]))
			if 'authSessionID' in query:
				del query['authSessionID']

			url_parts[4] = urllib.parse.urlencode(query)
			response.redirect(urllib.parse.urlunparse(url_parts))
		else:
			#we have an unauthenticated user
			response.tornadoObj.set_status(403)
			response.tornadoObj.set_header("Content-Type", "text/plain")
			response.write("403: Access Denied \nYou are not authorised to use this application")
			response.isLocked = True

		return False


	if 'auth_userdata' not in request.session: #is touple (userID, username)
		showLogin()
		return False
	else:
		return True





