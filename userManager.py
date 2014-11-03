users = {1: {'userID': 1, 'username': 'jye.lewis', 'password': 'test'}}

def userByID(userID):
	if userID in users:
		return users[userID]
	else:
		return None


def userByUsername(username):
	for userID in users:
		if users[userID]['username'] == username:
			return users[userID]
	return None


def isValidUser(email, password):
	user = userByUsername(email)
	if user is not None:
		return user['password'] == password
	return False #email is incorrect