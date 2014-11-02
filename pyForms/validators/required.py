import pyForms.ControlBase
from pyForms.validators import Base

import pyForms.controls.Textbox

class Control(Base.Class):
	def initValidator(self):
		if type(self.control) is pyForms.controls.Textbox.Control:
			self.serverValidator = self.ctrl_textbox
			self.clientCode = "return currentElement.value != ''; "

		elif type(self.control) is pyForms.controls.Checkbox.Control:
			self.serverValidator = self.ctrl_checkbox
			self.clientCode = "return currentElement.checked == true;"

		elif type(self.control) is pyForms.controls.Dropdown.Control:
			self.serverValidator = self.ctrl_dropdown
			self.clientCode = "return currentElement.selectedIndex != 0;"

		elif type(self.control) is pyForms.controls.FileUpload.Control:
			self.serverValidator = self.ctrl_file
			self.clientCode = "return currentElement.files.length != 0;"

	


	def ctrl_textbox(self):
		return len(self.control.text) > 0

	def ctrl_checkbox(self):
		return self.control.checked

	def ctrl_dropdown(self):
		return self.control.selectedIndex != 0

	def ctrl_file(self):
		return self.control.file is not None







