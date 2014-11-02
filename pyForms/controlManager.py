allControls = {}

def registerControl(controlName, control):
	controlName = controlName.lower()
	if controlName in allControls:
		raise Exception(controlName + "is already regestered")
	allControls[controlName] = control


#register controls
import pyForms.controls.Textbox
registerControl("Textbox", pyForms.controls.Textbox.Control)

import pyForms.controls.Button
registerControl("Button", pyForms.controls.Button.Control)

import pyForms.controls.html
registerControl("html", pyForms.controls.html.Control)

import pyForms.controls.Panel
registerControl("Panel", pyForms.controls.Panel.Control)

import pyForms.controls.Loop
registerControl("Loop", pyForms.controls.Loop.Control)

import pyForms.controls.Checkbox
registerControl("Checkbox", pyForms.controls.Checkbox.Control)

import pyForms.controls.validationGroup
registerControl("validationGroup", pyForms.controls.validationGroup.Control)

import pyForms.controls.Dropdown
registerControl("Dropdown", pyForms.controls.Dropdown.Control)

import pyForms.controls.FileUpload
registerControl("FileUpload", pyForms.controls.FileUpload.Control)

import pyForms.controls.LinkButton
registerControl("LinkButton", pyForms.controls.LinkButton.Control)

import pyForms.controls.include
registerControl("include", pyForms.controls.include.Control)


