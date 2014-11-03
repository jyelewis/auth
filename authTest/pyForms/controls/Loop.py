import random

import pyForms.ControlBase
import pyForms.parser

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		rawInnerHTML = obj['innerHTML']
		obj['innerHTML'] = None #make sure the children arent processed
		super().__init__(obj)
		self.rawInnerHTML = rawInnerHTML

		self._dataSource = []
		
		self.loops = []

		self.configureLoopHandler = self.getEventHandler("configureLoop")


	@property
	def dataSource(self):
		return self._dataSource

	@dataSource.setter
	def dataSource(self, newValue):
		self._dataSource = newValue
		self.update()

	#overloads so it works with loop controls
	def parentConfigure(self, func):
		func(self)
		for loop in self.loops:
			for control in loop[2]:
				control.parentConfigure(func)

	def update(self):
		self.loops = []

		for item in self.dataSource:
			self._appendToLoops(item)


	def reconfigure(self):
		if self.configureLoopHandler:
			for index, item in enumerate(self.loops):
				self.loops[index][0] = index #update indexes
				self.configureLoopHandler(item[3], item[1], item[0])

	def remove(self, index):
		del self.dataSource[index]
		del self.loops[index]

	def append(self, item):
		self.dataSource.append(item)
		self._appendToLoops(item)


	def _appendToLoops(self, item):
		controlsDict = {}
		controlsReference = ControlsReference(controlsDict)

		index = len(self.loops)

		def customRegisterFunction(controlToRegister):
			nonlocal index
			if controlToRegister.id is not None:
				controlToRegister.attributes['id'] = self.id + "_" + controlToRegister.id + "_" + str(index) + str(random.randint(100000, 999999))
				controlsDict[controlToRegister.id] = controlToRegister

		controls = pyForms.parser.parse(self.rawInnerHTML, self.pageInstance, customRegisterFunction)
		self.loops.append([
			 index
			,item
			,controls
			,controlsReference
		])

		if self.configureLoopHandler:
			self.configureLoopHandler(controlsReference, item, index)

	def onRequest(self):
		#forward to all children
		for loop in self.loops:
			for control in loop[2]:
				control.onRequest()

	def fireEvents(self):
		#forward to all children
		for loop in self.loops:
			for control in loop[2]:
				control.fireEvents()

	def render(self):
		renderCode = ""
		for loop in self.loops:
			renderCode += "".join([x.render() for x in loop[2]])
		return renderCode



class ControlsReference:
	def __init__(self, controlsDict):
		self.controlsDict = controlsDict

	def __getattr__(self, controlID):
		if controlID in self.controlsDict:
			return self.controlsDict[controlID]
		else:
			return None






