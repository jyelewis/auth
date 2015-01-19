class PageController:
	def __init__(self, page):
		self.page = page

	def onInit(self, ctrls):
		pass

	def onLoad(self, ctrls):
		pass

	def onPrerender(self, ctrls):
		pass

	def setHTMLFile(self):
		raise NotImplementedError("setHTMLFile is not implemented")

	def pageCode(self):
		if not hasattr(self, 'HTMLFile'):
			self.setHTMLFile()

		if not hasattr(self, 'HTMLFile'):
			raise Exception("setHTMLFile didn't set self.HTMLFile !")

		file = open(self.HTMLFile, 'r')
		retValue = file.read()
		file.close()
		
		return retValue