import pyForms.controlManager


from pyForms.validators import required
pyForms.controlManager.registerControl("validator:required", required.Control)

from pyForms.validators import range as rangeValidator
pyForms.controlManager.registerControl("validator:range", rangeValidator.Control)