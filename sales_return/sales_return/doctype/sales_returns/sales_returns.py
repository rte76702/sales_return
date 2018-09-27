# -*- coding: utf-8 -*-
# Copyright (c) 2018, rte76702 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals
from frappe.utils import cint

class SalesReturns(Document):
	
	def get_invoices(self):
		sinvs = frappe.get_all('Sales Invoice',filters={'docstatus':0, 'customer':self.waiter})
		sinvs = [frappe.get_doc('Sales Invoice', i) for i in sinvs if \
					cint(frappe.db.get_default("hooked_%s_%s"%(self.waiter, i.name)))]
		
		resp = []
		total = 0
		self.set('invoice_items', [])
		self.set('items_found', 0)
		for inv in sinvs:
			for item in inv.items:
				self.append('invoice_items', {
					'sales_invoice':inv.name,
					'item_code':item.item_code,
					'qty':item.qty,
					'amount':item.net_amount,
					'rate': item.rate
				})
				total += item.net_amount
		self.total_amount = total
		if self.invoice_items:
			self.items_found = 1
		else:
			frappe.msgprint('No pending Sales Invoices')

	def submit_invoices(self):
		invoices = list(set([i.sales_invoice for i in self.invoice_items]))
		for invoice in invoices:
			inv = frappe.get_doc('Sales Invoice', invoice)
			item_qtys = {i.item_code:i.qty for i in self.invoice_items if i.sales_invoice == invoice}
			for item in inv.items:
				if not item.item_code in item_qtys.keys():
					frappe.throw('Item %s in original invoice not found in reconciled invoice'%item.item_code)
				item.qty = item_qtys[item.item_code]
			inv._action = ''
			if inv.payments:
				inv.payments[0].amount = inv.grand_total
			else:
				payment = inv.append('payments', {})
				payment.update({'mode_of_payment':"Cash"})
			inv.write_off_amount = 0
			inv.validate()
			frappe.db.set_default("hooked_%s_%s"%(self.waiter, invoice), 0)
			inv.submit()
			frappe.defaults.clear_default("hooked_%s_%s"%(self.waiter, invoice))
		frappe.db.commit()


	def remove_items(self, item_group, item, quantity):
		if not (item and frappe.utils.cint(quantity)):
			return []
		for row in self.invoice_items:
			if quantity and row.item_code == item:
				if row.qty >= quantity:
					row.qty = row.qty - quantity
					quantity = 0
					row.amount = row.rate*row.qty
					break
				elif row.qty < quantity:
					quantity = quantity - row.qty
					row.qty = 0
					row.amount = 0
		if quantity: frappe.msgprint('Quantity specified is greater than that found in invoices')
		self.total_amount = sum([i.amount for i in self.invoice_items])
