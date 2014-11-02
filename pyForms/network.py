import random

sessions = {}

#These classes must be subclassed to generate objects for specific server frameworks

class Request():
	def __init__(self):
		self.url = None
		self.get = {}
		self.post = {}
		self.isValid = True

		self._isPostBack = None

		self._session = None

	@property
	def isPostBack(self):
		if self._isPostBack is None:
			self._isPostBack = ('pyForms__postbackInstanceID' in self.post)
		return self._isPostBack

	@property
	def session(self):
		if self._session is None:
			if 'pyForms__sessionID' in self.cookies and self.cookies['pyForms__sessionID'] in sessions:
				self._session = sessions[self.cookies['pyForms__sessionID']] #fetch existing session
			else:
				newSessionID = str(random.randint(100000,999999))
				self.setCookie('pyForms__sessionID', newSessionID)
				self._session = {}
				sessions[newSessionID] = self._session

		return self._session


class Response():
	def __init__(self):
		self.isLocked = False #set to false when a header locking function is used (redirect)

	def write(self):
		raise NotImplimentedError

	def end(self):
		pass

	def redirect(self):
		raise NotImplimentedError



