# Copyright (c) 2026, omfsakib@gmail.com and Contributors
# See license.txt

import json

import frappe

no_sitemap = 1


@frappe.whitelist(allow_guest=False)
def index():
	"""
	Save or update push subscription for the current user
	
	Expected POST data:
		subscription: JSON string of subscription object from browser
	
	Returns:
		dict: Success status and message
	"""
	try:
		# Get subscription data from request
		subscription_json = frappe.form_dict.get("subscription")
		
		if not subscription_json:
			frappe.throw("Subscription data is required")
		
		# Parse subscription data
		subscription = json.loads(subscription_json)
		
		endpoint = subscription.get("endpoint")
		keys = subscription.get("keys", {})
		p256dh = keys.get("p256dh")
		auth = keys.get("auth")
		
		if not endpoint or not p256dh or not auth:
			frappe.throw("Invalid subscription data")
		
		# Get user agent from request headers
		user_agent = frappe.request.headers.get("User-Agent", "")[:140]  # Limit to 140 chars
		
		# Check if subscription already exists
		existing = frappe.db.exists("Push Subscription", {"endpoint": endpoint})
		
		if existing:
			# Update existing subscription
			doc = frappe.get_doc("Push Subscription", existing)
			doc.user = frappe.session.user
			doc.p256dh_key = p256dh
			doc.auth_key = auth
			doc.user_agent = user_agent
			doc.is_active = 1
			doc.save(ignore_permissions=True)
			message = "Subscription updated successfully"
		else:
			# Create new subscription
			doc = frappe.get_doc({
				"doctype": "Push Subscription",
				"user": frappe.session.user,
				"endpoint": endpoint,
				"p256dh_key": p256dh,
				"auth_key": auth,
				"user_agent": user_agent,
				"is_active": 1
			})
			doc.insert(ignore_permissions=True)
			message = "Subscription created successfully"
		
		frappe.db.commit()
		
		return {
			"success": True,
			"message": message,
			"subscription_name": doc.name
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Push Subscription Error")
		return {
			"success": False,
			"message": str(e)
		}
