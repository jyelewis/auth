import pyForms.ControlBase
from pyForms.validators import Base

import pyForms.controls.Textbox

class Control(Base.Class):
	def __init__(self, obj):
		super().__init__(obj)
		self.min = None
		if 'min' in self.attributes:
			self.min = float(self.attributes['min'])
			del self.attributes['min']

		self.max = None
		if 'max' in self.attributes:
			self.max = float(self.attributes['max'])
			del self.attributes['max']



	def initValidator(self):
		if not type(self.control) is pyForms.controls.Textbox.Control:
			raise Exception("Non textbox control given to range validator")
			return

		self.serverValidator = self.ctrl_textbox
		#client code is set in render



	def ctrl_textbox(self):
		if self.control.text == "":
			return True
		try:
			val = float(self.control.text)
			if self.min is not None and val <= self.min or self.max is not None and val >= self.max:
				return False
			return True
		except ValueError:
			return False

	def render(self):
		self.clientCode  = "if (currentElement.value == '') {return true;} \n"
		self.clientCode += "if (isNaN(currentElement.value)) {return false;} \n"
		if self.min is not None:
			self.clientCode += "if (parseFloat(currentElement.value) < "+ str(self.min) +") {return false;} \n"
		if self.max is not None:
			self.clientCode += "if (parseFloat(currentElement.value) > "+ str(self.max) +") {return false;} \n"
		self.clientCode += "return true;"
		return super().render()






