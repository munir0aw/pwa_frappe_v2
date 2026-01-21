# Copyright (c) 2026, omfsakib@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PushSubscription(Document):
	def before_insert(self):
		"""Set user and created_at before inserting"""
		if not self.user:
			self.user = frappe.session.user
		if not self.created_at:
			self.created_at = frappe.utils.now()

	def validate(self):
		"""Validate subscription data"""
		# Ensure user can only create subscriptions for themselves (unless System Manager)
		if not frappe.has_permission("Push Subscription", "write"):
			if self.user != frappe.session.user:
				frappe.throw("You can only create subscriptions for yourself")

		# Deactivate any existing subscriptions with the same endpoint
		existing = frappe.db.get_all(
			"Push Subscription",
			filters={
				"endpoint": self.endpoint,
				"name": ["!=", self.name],
			},
			pluck="name"
		)
		
		if existing:
			for sub_name in existing:
				frappe.db.set_value("Push Subscription", sub_name, "is_active", 0)
