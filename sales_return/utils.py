
import frappe, pprint


def prevent_submission(doc, method):
	print '\n\n\n\nSubmitted SINV:\n', doc.name, '\n***********************\n\n\n\n'
	settings = frappe.get_doc('Return Settings')
	returns  = frappe.get_doc('Sales Returns')
	if not frappe.utils.cint(settings.enabled):
		return
	if not doc.name in [i.docname for i in returns.docs_table]:
		if doc.customer in [i.customer for i in settings.waiters_table]:
			d_row = {
				'customer': doc.customer,
				'docname': doc.customer
			}
			returns.append('docs_table', d_row)
			returns.save()
			doc.docstatus = 0
	else:
		print '\n\n\n\nWHAT NOw\n\n\n\n\n'
		return
