
import frappe, pprint
from frappe import _


def prevent_submission(doc, method):
	from frappe.utils import cint

	print '\n\n\n\nSubmitted SINV:\n', doc.name, '\n***********************\n\n\n\n'
	settings = frappe.get_doc('Returns Settings')
	returns  = frappe.get_doc('Sales Returns')
	if not doc.name in [i.docname for i in returns.docs_table]:
		if not cint(settings.enabled):
			return
		if doc.customer in [i.customer for i in settings.waiters_table]:
			d_row = {
				'customer': doc.customer,
				'docname': doc.name
			}
			returns.append('docs_table', d_row)
			returns.save()
			doc.docstatus = 0
	else:
		doc_row = [i for i in returns.docs_table if i.docname == doc.name]
		doc_row = doc_row[0] if doc_row else frappe._dict({'allow_submit': 1})
		if not cint(doc_row.allow_submit):
			doc.docstatus = 0

def prevent_delete(doc, method):
	returns  = frappe.get_doc('Sales Returns')
	doc_row = [i for i in returns.docs_table if i.docname == doc.name]
	doc_row = doc_row[0] if doc_row else frappe._dict()
	if doc_row.docname:
		frappe.throw(_("Cannot delete invoice now. Please reconcilce Items in 'Sales Returns' first"))