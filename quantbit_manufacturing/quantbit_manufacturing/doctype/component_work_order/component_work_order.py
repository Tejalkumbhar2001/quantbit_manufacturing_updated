# Copyright (c) 2024, Quantbit Technologies Pvt. Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ComponentWorkOrder(Document):

	# Fetch Child table from Component Manifest doctype to Component Work Order Doctype
	@frappe.whitelist()
	def get_raw_materials(self):
		if self.finished_item_code:
			doc_name = frappe.get_value('Component Manifest',{'finished_item_code': self.finished_item_code, "enable": True}, "name")
			if doc_name:
				doc = frappe.get_doc('Component Manifest', doc_name)
				self.quantity_to_manufacturing=doc.quantity_to_manufacturing
				self.rate_of_quantity = doc.rate_of_quantity
				for d in doc.get("raw_materials"):
					self.append('component_raw_item', {	
						"item_code": d.item_code,
						"item_name": d.item_name,
						"quantity": d.quantity,
						"actual_quantity":d.quantity,
						"uom": d.uom,
						"total": d.total,
					})
			else:
				frappe.throw(("Component Manifest not found for item code {0}").format(self.finished_item_code))


	# Calculate Quantity and Used Quantity In Component Raw Item			
	@frappe.whitelist()
	def calculate_quantity_in_component_row_item(self):
		for row in self.get("component_raw_item"):
			row.quantity = (self.updated_quantity_to_manufacturing * row.actual_quantity)/self.quantity_to_manufacturing
			row.used_quantity = (self.updated_quantity_to_manufacturing * row.actual_quantity)/self.quantity_to_manufacturing


	# If Source Warehouse is same for all Raw Item then Set selected source warehouse for all child entries
	@frappe.whitelist()
	def set_source_warehouse(self):
		if self.source_warehouse:
			for i in self.get('component_raw_item'):			
				i.source_warehouse = self.source_warehouse


	def on_submit(self):
		self.Manufacturing_stock_entry()


	# After Submitting Component Work Order Manufacturing Stock Entry will be created
	@frappe.whitelist()
	def Manufacturing_stock_entry(self):
		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = "Manufacture"
		doc.company = self.company
		doc.posting_date =self.posting_date
		for i in self.get("component_raw_item"):
			doc.append("items", {
				"s_warehouse": i.source_warehouse,
				"item_code": i.item_code,
				"item_name": i.item_name,
				"qty": i.used_quantity,
			})
		
		doc.append("items", {
			"item_code": self.finished_item_code,
			"qty": self.updated_quantity_to_manufacturing,
			"t_warehouse": self.target_warehouse,
			"is_finished_item": True,
		})
		for j in self.get("operational_cost"):
			doc.append("additional_costs", {
				"expense_account": j.operations,
				"description": j.description,
				"amount": j.cost,
			})

		doc.custom_component_work_order = self.name
		doc.insert()
		doc.save()
		doc.submit()
