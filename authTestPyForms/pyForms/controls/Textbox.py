import random
import cgi
import pyForms.ControlBase

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)
		self.autoPostBackEvent = "blur"
		self.text = ""
		self.name = str(random.randint(100,999))
		if self.id is not None:
			self.name = self.attributes['id'] + "_" + self.name

		self.type = "singleline"
		if "type" in self.attributes:
			self.type = self.attributes['type']
			del self.attributes['type'] #dont keep it around

		if "text" in self.attributes:
			self.text = self.attributes['text']
			del self.attributes['text'] #dont keep it around

		self.changeHandler = self.getEventHandler("change")

		#this is used to know to fire the change event (and holds the old text)
		self._changeEventOldText = None

	def onRequest(self):
		if self.name in self.pageInstance.request.post:
			oldText = self.text
			self.text = self.pageInstance.request.post[self.name]
			if self.text != oldText:
				self._changeEventOldText = oldText

	def fireEvents(self):
		if self._changeEventOldText is not None and self.changeHandler:
			self.changeHandler(self._changeEventOldText)
		self._changeEventOldText = None

	def render(self):
		#setup for tag
		self.attributes['name'] = self.name

		if self.type.lower() in ["singleline", "password"]:
			self.attributes['type'] = "text" if self.type.lower() == "singleline" else "password"
			self.tagname = "input"
			self.isSelfClosing = True
			self.attributes['value'] = self.text
		elif self.type.lower() == "textarea":
			self.tagname = "textarea"
			self.isSelfClosing = False
			self.innerHTML = cgi.escape(self.text)
		else:
			raise Exception("Textbox type '" + self.type + "' is not valid")
		return super().render()