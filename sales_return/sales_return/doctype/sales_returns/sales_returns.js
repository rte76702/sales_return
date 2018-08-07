// Copyright (c) 2018, rte76702 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Returns', {
	refresh: function(frm) {
	},

	render_items: async function(frm) {
		var data = await frappe.call({
			method:'get_items',
		});
		$(this.frm.fields_dict['items_html'].wrapper)
		.html(frappe.render_template('invoice_items', data.message))
	},

	get_invoices: function(frm){
		frm.set_value('items_found', 1);
		frm.refresh_fields();
	},

	add_remove_items: function(){
		frappe.prompt([
		    {'fieldname': 'item_group', 'fieldtype': 'Link', 'label': 'Item Group', 'options':'Item Group', 'reqd': 1},
		    {'fieldname': 'item', 'fieldtype': 'Link', 'label': 'Item', 'options':'Item', 'reqd': 1},
		    {'fieldname': 'quantity', 'fieldtype': 'Int', 'label': 'Quantity', 'reqd': 1},
		    {'fieldname': 'add_remove', 'fieldtype': 'Select', 'label': 'Add/Remove', 'options':'Add\nRemove', 'reqd': 1},
		],
		async function(values){
			await frappe.call({
				method:'add_remove_items',
				freeze: true
			});
			cur_frm.reload_doc();
			frappe.msgprint('Items Updated')
		},
		'Add/Remove Items','Submit'
		)
	},
});
