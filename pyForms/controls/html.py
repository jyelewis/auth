import pyForms.ControlBase
import pyForms.parser

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)
		self.isSelfClosing = False

		self.head = findControl(self.children, 'head')
		self.body = findControl(self.children, 'body')

		#wrap the contents of the body inside a form tag
		formTag = pyForms.parser.GenericCtrl({
			'name': "form"
			,'attrs': { 'method': 'POST', 'id': 'pyForms__postbackForm', 'enctype': "multipart/form-data" }
			,'innerHTML': None
			,'pageInstance': self.pageInstance
			,'isSelfClosing': False
			,'customRegisterFunction': None
		})
		formTag.children = self.body.children
		
		#add a hidden field to the form to identify the page
		hiddenTag = pyForms.parser.GenericCtrl({
			'name': "input"
			,'attrs': {
				 'type': 'hidden'
				,'name': 'pyForms__postbackInstanceID'
				,'value': self.pageInstance.id
			}
			,'innerHTML': None
			,'pageInstance': self.pageInstance
			,'isSelfClosing': True
			,'customRegisterFunction': None
		})
		formTag.children.insert(0, hiddenTag)


		#add a script tag to the page head to create a post back function
		scriptTag = pyForms.parser.GenericCtrl({
			'name': "script"
			,'attrs': {
				 'type': 'text/ecmascript'
			}
			,'innerHTML': """function pyForms_postback(addName, addValue){
				if (addName){ 
					var input = document.createElement('input');
				    input.type = 'hidden';
				    input.name = addName
				    input.value = addValue || "1";
				    document.forms[0].appendChild(input)
			    }
				document.getElementById("pyForms__postbackForm").submit();
			}"""
			,'pageInstance': self.pageInstance
			,'isSelfClosing': False
			,'customRegisterFunction': None
		})
		self.head.children.append(scriptTag)


		self.body.children = [formTag]



def findControl(controls, tagName):
	for control in controls:
		if control.tagname == tagName:
			return control



