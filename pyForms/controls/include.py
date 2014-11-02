import pyForms.ControlBase
import pyForms.PageClasses

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		#memory jog: Page contains reference to controller - Creates pageInstances on request
		#page tells the contoller to do stuff (init, onLoad, setHTMLFile etc)

		#if a controller is provided use a blank page
		self.page = None
		if 'controller' in self.attributes:
			if not 'class' in self.attributes:
				self.attributes['class'] = "Controller"


			controllerModule = getattr(__import__(self.attributes['controller'], globals(), locals(), [], 0), self.attributes['controller'].split(".")[-1])
			controller = getattr(controllerModule, self.attributes['class'])
			self.page = pyForms.PageClasses.Page(controller)

			del self.attributes['controller'] #be gone
			del self.attributes['class'] #be gone

		self.includePageInstance = None #dont set this until first render so it/page can be set manually

	def render(self):
		if self.includePageInstance is None:
			self.includePageInstance = pyForms.PageClasses.PageInstance(self.page)

		return self.includePageInstance.renderRequest(self.pageInstance.request, self.pageInstance.response)