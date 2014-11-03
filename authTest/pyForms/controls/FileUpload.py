import random

import pyForms.ControlBase

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		#render config
		self.tagname = "input"
		self.isSelfClosing = True
		self.attributes['type'] = 'file'

		self.name = str(random.randint(100,999))
		if self.id is not None:
			self.name = self.attributes['id'] + "_" + self.name

		self.attributes['name'] = self.name
		self.uploadHandler = self.getEventHandler("upload")

		self.file = None

	def onRequest(self):
		if self.name in self.pageInstance.request.files:
			self.file = self.pageInstance.request.files[self.name]

	def fireEvents(self):
		if self.name in self.pageInstance.request.files and self.uploadHandler:
			self.uploadHandler()

	def render(self):
		return super().render()