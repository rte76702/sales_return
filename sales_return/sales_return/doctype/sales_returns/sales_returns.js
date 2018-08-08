// Copyright (c) 2018, rte76702 and contributors
// For license information, please see license.txt

var iter_rows = function(frm, rows){
	if (rows) {
		frm.doc.invoice_items = [];
		rows.forEach((row)=>{
			frm.add_child('invoice_items', row)
		})
		frm.set_value('items_found', 1);
		frm.refresh_fields();
	} else {
		frm.doc.invoice_items = [];
		frm.set_value('items_found', 0);
		frm.refresh_fields();
		frappe.msgprint('No pending Sales Invoices')
	}
};

frappe.ui.form.on('Sales Returns', {
	refresh: function(frm) {
		frm.disable_save()
	},

	submit_invoices: async function(frm){
		await frappe.call({
			method: 'submit_invoices',
			doc: frm.doc,
			freeze: true
		})
		frm.doc.invoice_items = [];
		frm.set_value('items_found', 0);
		frm.refresh_fields();
		frappe.msgprint('Invoices Submitted');
	},

	render_items: function(frm) {
		var data = frappe.call({
			method:'get_invoices',
			doc: frm.doc,
			freeze:true,
			callback: function(r){
				iter_rows(frm, r.message);
			}
		});
	},

	get_invoices: function(frm){
		frm.trigger('render_items');
	},

	remove_items: function(frm){
		frappe.prompt([
		    {'fieldname': 'item_group', 'fieldtype': 'Link', 'label': 'Item Group', 'options':'Item Group', 'reqd': 1,
				'item_group': (doc) => {console.log(doc)}
			},
		    {'fieldname': 'item', 'fieldtype': 'Link', 'label': 'Item', 'options':'Item', 'reqd': 1,
				get_query: (doc) => { return { filters: {  'item_group': $('div[data-fieldname=item_group]').find('input').val() } } }
			},
		    {'fieldname': 'quantity', 'fieldtype': 'Int', 'label': 'Quantity', 'reqd': 1},
		],  function(values){
				frappe.call({
					method:'remove_items',
					doc: frm.doc,
					args: values,
					freeze: true,
					callback: function(r){
						iter_rows(frm, r.message);
						frappe.msgprint('Items Updated')
					}
				});
			}, 'Add/Remove Items','Submit'
		)
	},
});
