import random

import pyForms.ControlBase

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		#render config
		self.tagname = "input"
		self.isSelfClosing = True
		self.attributes['type'] = 'checkbox'
		self.autoPostBackEvent = "change"

		self.name = str(random.randint(100,999))
		if self.id is not None:
			self.name = self.attributes['id'] + "_" + self.name

		if 'text' in self.attributes:
			self.text = self.attributes['text']

		self.checked = False
		if 'checked' in self.attributes:
			self.checked = (self.attributes['checked'] == "true")

		self.attributes['name'] = self.name
		self.checkHandler = self.getEventHandler("check")
		self._fireChangeEvent = False

	def onRequest(self):
		oldChecked = self.checked
		self.checked = (self.name in self.pageInstance.request.post)
		if oldChecked ^ self.checked: #checked status has changed
			self._fireChangeEvent = True


	def fireEvents(self):
		if self._fireChangeEvent and self.checkHandler:
			self.checkHandler()

	def render(self):
		if not self.visible:
			return ""
			
		if self.checked:
			self.attributes['checked'] = "checked"
		elif 'checked' in self.attributes:
			del self.attributes['checked']


		checkboxCode = super().render()

		if self.text is not None:
			if self.id is None:
				self.attributes['id'] = random.randint(100,999)
			checkboxCode += '<label for="'+ self.attributes['id'] +'">'+ self.text +'</label>'

		return checkboxCode





