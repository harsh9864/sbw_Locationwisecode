# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CountryCodeLogic(Document):
	@frappe.whitelist()
	def get_data(self):
		month_list = [
			"Country Zone",
			"States",
			"State Zone",
			"Districts",
			"District Zone",
			"Area",
			"Area Zone",
			"Society",
			"Sub Society",
			"Street",
	
		]
		idx = 1
		for m in month_list:
			mnth = self.append("country_code_logic_table")
			mnth.doctype_list = m
			idx += 1
	pass
