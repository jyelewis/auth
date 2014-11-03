import binascii
import tornado.web

import pyForms.network

class Request(pyForms.network.Request):
	@classmethod
	def fromTornado(cls, tornadoObj):
		request = cls(tornadoObj)

		#these are taking the same feed. Which has all arguments, fix when smarter
		allArgs = {}
		for key in tornadoObj.request.arguments:
			#this cannot be efficent
			allArgs[key] = tornadoObj.request.arguments[key][0].decode("utf-8")

		allFiles = {}
		for key in tornadoObj.request.files:
			#this cannot be efficent
			file = tornadoObj.request.files[key][0]
			fileDict = {}
			fileDict['contents'] = file['body']
			fileDict['contentType'] = file['content_type']
			fileDict['filename'] = file['filename']
			allFiles[key] = fileDict

		allCookies = {}
		for key in tornadoObj.request.cookies:
			allCookies[key] = tornadoObj.request.cookies[key].value.replace("__space__", "")

		request.get  = allArgs
		request.post = allArgs
		request.files = allFiles
		request.cookies = allCookies

		request.url = tornadoObj.request.protocol + "://" + tornadoObj.request.host + tornadoObj.request.uri
		return request

	def __init__(self, tornadoObj):
		self.tornadoObj = tornadoObj
		super().__init__()

	def setCookie(self, name, value, args = {}):
		defaultArgs = {
			 'expires': None
			,'domain': None
			,'path': "/"
		}
		args = dict(list(defaultArgs.items()) + list(args.items())) #fill with defaults
		#tornado seems to have problems encoding some characters
		#GOOGLE THIS PROBLEM WHEN YOU NEXT HAVE INTERNET AND GET A REAL FIX
		value = value.replace(" ", "__space__")
		self.tornadoObj.set_cookie(name, value, args['domain'], args['expires'], args['expires'])

	def clearCookie(self, name, domain = None, path = "/"):
		self.tornadoObj.clear_cookie(name, path, domain)



class Response(pyForms.network.Response):
	@classmethod
	def fromTornado(cls, tornadoObj):
		response = cls(tornadoObj)
		return response

	def __init__(self, tornadoObj):
		super().__init__()
		self.tornadoObj = tornadoObj

	def write(self, content):
		if not self.isLocked:
			self.tornadoObj.write(content)
		else:
			print("WARNING: write called after response locked")

	def redirect(self, location):
		if not self.isLocked:
			self.isLocked = True #redirect locks response
			self.tornadoObj.redirect(location)



def tornadoHandler(page): #returns handler class
	class pyFormsTornadoRequestHandler(tornado.web.RequestHandler):
		def get(self):
			request = Request.fromTornado(self)
			response = Response.fromTornado(self)
			page.handleRequest(request, response)

		def post(self):
			self.get()

	return pyFormsTornadoRequestHandler






