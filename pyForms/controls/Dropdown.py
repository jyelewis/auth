import cgi
import random

import pyForms.ControlBase
import pyForms.parser

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		#render config
		self.tagname = "select"
		self.isSelfClosing = False

		self.autoPostBackEvent = "change"

		self.name = str(random.randint(100,999))
		if self.id is not None:
			self.name = self.attributes['id'] + "_" + self.name

		self.attributes['name'] = self.name
		
		self.dataSource = []

		for child in self.children:
			if not isinstance(child, pyForms.parser.GenericCtrl):
				continue

			if child.tagname != "option":
				raise Exception("Non option tag inside select control")
				return

			if 'value' in child.attributes:
				self.dataSource.append((child.rawInnerHTML, child.attributes['value']))
			else:
				self.dataSource.append(child.rawInnerHTML)

		self.selectedIndex = None if len(self.dataSource) == 0 else 0

		self.changeHandler = self.getEventHandler("change")
		self._fireChangeEvent = False

	@property
	def selectedValue(self):
		return getItemValue(self.dataSource[self.selectedIndex])
		

	@selectedValue.setter
	def selectedValue(self, newValue):
		for index, item in enumerate(self.dataSource):
			if getItemValue(item) == newValue:
				self.selectedIndex = index

	@property
	def selectedItem(self):
		return self.dataSource[self.selectedIndex]

	@property
	def selectedText(self):
		return getItemText(self.dataSource[self.selectedIndex])

	def onRequest(self):
		if self.name in self.pageInstance.request.post:
			oldIndex = self.selectedIndex
			self.selectedIndex = int(self.pageInstance.request.post[self.name])
			if self.selectedIndex != oldIndex:
				self._fireChangeEvent = True
		else:
			selectedIndex = None


	def fireEvents(self):
		if self._fireChangeEvent and self.changeHandler:
			self.changeHandler()

			
	def render(self):
		if not self.visible:
			return ""

		self.children = []
		for index, item in enumerate(self.dataSource):
			attrs = {'value': str(index)}
			if self.selectedIndex == index:
				attrs['selected'] = 'selected'
			self.children.append(pyForms.parser.GenericCtrl({
				'name': 'option'
				,'attrs': attrs
				,'startContentsPos': None
				,'endContentsPos': None
				,'innerHTML': cgi.escape(str(getItemText(item)))
				,'isSelfClosing': None
				,'pageInstance': self.pageInstance
				,'customRegisterFunction': None
			}))

		return super().render()


def getItemValue(item):
	if isinstance(item, tuple):
		return item[1]
	else:
		return None

def getItemText(item):
	if isinstance(item, tuple):
		return item[0]
	else:
		return item



