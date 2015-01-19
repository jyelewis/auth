import userManager
import uuid
import datetime

sessions = {} #contains dictionary "authSessionID": (isAuthenticated: True, userID: 123)


def isAuthenticated(request):
	if 'authSessionID' not in request.cookies or request.cookies['authSessionID'] not in sessions: #has cookie and session exists
		return False

	return sessions[request.cookies['authSessionID']]['isAuthenticated'] #cookie exists, return state

def getAuthenticatedUser(request):
	if not isAuthenticated(request):
		return None
	return userManager.userByID(sessions[request.cookies['authSessionID']]['userID'])

def setSession(request, response, username, isAuthenticated = True, rememberMe = False):
	user = userManager.userByUsername(username)
	if user is None:
		return False

	if isAuthenticated:
		sessionUUID = str(uuid.uuid4())
		sessions[sessionUUID] = {'isAuthenticated': True, 'userID':userManager.userByUsername(username)['userID']}
		#set cookie 'authSessionID' = sessionUUID
		if rememberMe:
			expires = datetime.datetime.utcnow() + datetime.timedelta(days=7) #set for 7 days
		else:
			expires = None
		request.setCookie('authSessionID', sessionUUID, { 'expires': expires })
		return sessionUUID
	else:
		request.setCookie('authSessionID', "", { 'expires': datetime.datetime.utcnow() - datetime.timedelta(days=1) })

def getSession(request):
	if isAuthenticated(request):
		return request.cookies['authSessionID']
	else:
		return None




