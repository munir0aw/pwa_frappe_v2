# Copyright (c) 2026, omfsakib@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PushSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		auth_key: DF.Text
		created_at: DF.Datetime | None
		endpoint: DF.Data
		is_active: DF.Check
		p256dh_key: DF.Text
		user: DF.Link
		user_agent: DF.Data | None
	# end: auto-generated types

	pass
