import pyForms.ControlBase

class Class(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)
		self.isSelfClosing = False

		self.control = None #this will be given by the validationgroup
		if 'control' in self.attributes:
			self.controlID = self.attributes['control']
			del self.attributes['control']
		else:
			self.controlID = None

		self.isValid = True

		self.clientCode = "return true;"
		self.serverValidator = lambda: True

		self.tagname = "span"
		self.attributes['style'] = "display:none;"

		self.hasInited = False


	def onRequest(self):
		#show error thingy if there is an error thingy
		if self.pageInstance.request.isPostBack:
			self.isValid = self.serverValidator()
			self.pageInstance.request.isValid = self.isValid

	def render(self):
		if not self.hasInited:
			self.initValidator()
			self.hasInited = True

		if self.isValid:
			self.attributes['style'] = "display:none;"
		else:
			self.attributes['style'] = ""
		return super().render()
