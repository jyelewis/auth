import codecs
import html
import re
from html.parser import HTMLParser

import pyForms.controlManager
import pyForms.ControlBase



class GenericCtrl(pyForms.ControlBase.Base):
	def __init__(self, objData):
		super().__init__(objData)
		self.isSelfClosing = objData['isSelfClosing']


class TextCtrl(pyForms.ControlBase.Base):
	def __init__(self, text):
		self.text = text
		self.id = None
		self.tagname = None

	def render(self):
		return self.text

	#the default functionality wont work with this control
	def setPageInstance(self, page):
		pass

	def registerChildren(self):
		pass

	def registerID(self):
		pass

	def onRequest(self):
		pass

	def fireEvents(self):
		pass

	def parentConfigure(self, func):
		func(self)

	def onChildrenChange(self):
		pass



def parse(html, pageInstance, customRegisterFunction = None):
	#we define the class in here so it can access the pageInstance var
	class CustomHTMLParser(HTMLParser):
		def __init__(self):
			super().__init__()
			self.depth = 0
			self.curTag = None
			self.tags = []
			self.splitData = None
			self.tagVerify = []
			self.selfClosingTags = """
area
base
br
col
command
embed
hr
img
input
keygen
link
meta
param
source
track
wbr
			""".split("\n")
			

		def reset(self):
			super().reset()
			#self.interesting = re.compile('[<]') #we dont want the default amperstand the the 'intersting' re finds

		def handle_starttag(self, tag, attrs):
			if not self.splitData:
				self.splitData = self.rawdata.split("\n")

			self.tagVerify.append(tag)

			if self.curTag != None and self.curTag['startContentsPos'] == None:
				self.curTag['startContentsPos'] = self.getpos()
			
			self.depth += 1
			if self.depth == 1:
				self.curTag = {
					'name': tag.lower()
					,'attrs': dict(attrs)
					,'startContentsPos': None
					,'endContentsPos': None
					,'innerHTML': None
					,'isSelfClosing': None
					,'pageInstance': pageInstance
					,'customRegisterFunction': customRegisterFunction
				}
			if tag in self.selfClosingTags:
				self.handle_endtag(tag, True)

		def handle_endtag(self, tag, isHandlingSelfClosing = False):
			if isHandlingSelfClosing ^ (tag in self.selfClosingTags):
				return

			expecting = self.tagVerify.pop()
			if not isHandlingSelfClosing and expecting != tag:
				raise Exception("Error parsing HTML, " + tag + " ended before " + expecting)
				return

			self.depth -= 1

			if self.depth == 0:

				self.curTag['endContentsPos'] = self.getpos()

				if isHandlingSelfClosing:
					self.curTag['isSelfClosing'] = True
				else:
					if self.curTag['startContentsPos'] is None:
						self.curTag['startContentsPos'] = self.curTag['endContentsPos']
					self.curTag['isSelfClosing'] = False
					start = self.curTag['startContentsPos']
					end = self.curTag['endContentsPos']
					dataRows = self.splitData[start[0]-1:end[0]]
					dataRows[0] = dataRows[0][start[1]:]
					if start[0] == end[0]: #remember that this row has already had some content lopped off, account
						dataRows[-1] = dataRows[-1][:end[1]-start[1]]
					else:
						dataRows[-1] = dataRows[-1][:end[1]]

					self.curTag['innerHTML'] = "\n".join(dataRows)

				if 'server' in self.curTag['attrs']:
					if self.curTag['name'] in pyForms.controlManager.allControls:
						self.tags.append(pyForms.controlManager.allControls[self.curTag['name']](self.curTag))
					else:
						raise Exception("Control marked as server but no handler is registerd for '" + self.curTag['name'] + "'")
				else:
					self.tags.append(GenericCtrl(self.curTag))
				self.curTag = None

		def handle_data(self, data):
			if self.curTag != None and self.curTag['startContentsPos'] == None:
				self.curTag['startContentsPos'] = self.getpos()

			if self.depth == 0:
				self.tags.append(TextCtrl(data))

		def handle_entityref(self, data):
			self.handle_data("&" + data + ";")

		def handle_charref(self, data):
			self.handle_data("&#" + data + ";")

		def handle_comment(self, comment):
			if self.depth == 0:
				self.tags.append(TextCtrl("<!--" + comment + "-->"))

		def handle_decl(self, decl):
			if self.depth == 0:
				self.tags.append(TextCtrl("<!" + decl + ">"))


	parser = CustomHTMLParser()
	parser.feed(html)
	#create objects from tags
	return parser.tags
