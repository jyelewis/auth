import random

import pyForms.ControlBase

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		#render config
		self.tagname = "input"
		self.isSelfClosing = True
		self.attributes['type'] = 'submit'

		self.name = str(random.randint(100,999))
		if self.id is not None:
			self.name = self.attributes['id'] + "_" + self.name

		self.attributes['name'] = self.name
		self.clickHandler = self.getEventHandler("click")

	@property
	def text(self):
		return self.innerHTML

	@text.setter
	def text(self, newVal):
		self.innerHTML = newVal

	def fireEvents(self):
		if self.name in self.pageInstance.request.post and self.clickHandler:
			self.clickHandler()

	def render(self):
		self.attributes['value'] = self.innerHTML
		return super().render()