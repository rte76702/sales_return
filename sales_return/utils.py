
import frappe, pprint
from frappe import _
from frappe.utils import cint


def prevent_submission(doc, method):
	settings = frappe.get_doc('Returns Settings')
	if not cint(settings.enabled):
		return
	if frappe.db.get_default("hooked_%s_%s"%(doc.customer, doc.name)) == None:
		if doc.customer in [i.customer for i in settings.waiters_table]:
			frappe.db.set_default("hooked_%s_%s"%(doc.customer, doc.name), 1)
			doc.docstatus = 0
	else:
		if cint(frappe.db.get_default("hooked_%s_%s"%(doc.customer, doc.name))) == 1:
			doc.docstatus = 0

def prevent_delete(doc, method):
	if not cint(frappe.db.get_single_value('Returns Settings', 'enabled')):
		return
	if cint(frappe.db.get_default("hooked_%s_%s"%(doc.customer, doc.name))):
		frappe.throw(_("Cannot delete invoice now. Please reconcile Items in 'Sales Returns' first"))