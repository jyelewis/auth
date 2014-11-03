import userManager
import uuid

sessions = {} #contains dictionary "authSessionID": (isAuthenticated: True, userID: 123)


def isAuthenticated(request):
	if 'authSessionID' not in request.cookies or request.cookies['authSessionID'] not in sessions: #has cookie and session exists
		return False

	return sessions[request.cookies['authSessionID']]['isAuthenticated'] #cookie exists, return state

def getAuthenticatedUser(request):
	if not isAuthenticated(request):
		return None
	return userManager.userByID(sessions[request.cookies['authSessionID']]['username'])

def getSessionIDByUserID(userID):
	for sessionID in sessions:
		if sessions[sessionID]['userID'] == userID:
			return sessionID
	return None

def setSession(request, response, username, isAuthenticated = True):
	user = userManager.userByUsername(username)
	if user is None:
		return False

	currentSessionID = getSessionIDByUserID(user['userID'])
	
	if currentSessionID is not None:
		sessionUUID = currentSessionID
		sessions[currentSessionID]['isAuthenticated'] = isAuthenticated
	else:
		sessionUUID = str(uuid.uuid4())
		sessions[sessionUUID] = {'isAuthenticated': isAuthenticated, 'userID':userManager.userByUsername(username)['userID']}
		#set cookie 'authSessionID' = sessionUUID
		response.setCookie('authSessionID', sessionUUID, {
			 'expires': None
			,'domain': ""
			,'path': "/"
		})

	

	return sessionUUID

def getSession(request):
	if isAuthenticated(request):
		return request.cookies['authSessionID']
	else:
		return None




