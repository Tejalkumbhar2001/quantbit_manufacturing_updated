// Copyright (c) 2024, Quantbit Technologies Pvt. Ltd and contributors
// For license information, please see license.txt


// after getting finished Item code raw mnaterial for that finished item appended in child table
frappe.ui.form.on('Component Work Order', {
	finished_item_code: function(frm) {
		frm.clear_table("component_raw_item");
		frm.refresh_field('component_raw_item');
		frm.call({
			method:'get_raw_materials',
			doc:frm.doc
		})
	}
});

// calculate quantity and used quantity in Component Raw Item child table after entering updated quantity to manufacturing
frappe.ui.form.on('Component Work Order', {
	updated_quantity_to_manufacturing: function(frm) {
		frm.refresh_field('quantity');
		frm.call({
			method:'calculate_quantity_in_component_row_item',
			doc:frm.doc
		})
	}
});

//  setting source warehouse in Component Raw Item child table after selected source warehouse field
frappe.ui.form.on('Component Work Order', {
	source_warehouse: function(frm) {
		frm.call({
			method:'set_source_warehouse',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on("Component Work Order", {
	setup: function(frm) {
			frm.set_query("operator", function() { // Replace with the name of the link field
				return {
					filters: [
						["Employee", "company", '=', frm.doc.company],// Replace with your actual filter criteria
						["Employee", "designation", '=', 'Operator'],
					]
				};
			});

		}
});


frappe.ui.form.on("Component Work Order", {
	setup: function(frm) {
			frm.set_query("supervisor", function() { // Replace with the name of the link field
				return {
					filters: [
						["Employee", "company", '=', frm.doc.company],// Replace with your actual filter criteria
						["Employee", "designation", '=', 'Supervisor'],
					]
				};
			});

		}
});
	