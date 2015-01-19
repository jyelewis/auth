import pyForms.ControlBase
import pyForms.parser

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)
		self.isSelfClosing = False

	def render(self):
		if not self.visible:
			return ""
		return self.innerHTML



