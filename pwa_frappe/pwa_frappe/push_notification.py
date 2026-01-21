# Copyright (c) 2026, omfsakib@gmail.com and contributors
# For license information, please see license.txt

import json

import frappe
from pywebpush import WebPushException, webpush


@frappe.whitelist()
def send_push_notification(user, title, body, data=None):
	"""
	Send push notification to a specific user
	
	Args:
		user (str): User email/ID to send notification to
		title (str): Notification title
		body (str): Notification body text
		data (dict, optional): Additional data payload
	
	Returns:
		dict: Success status and message
	"""
	try:
		# Get active subscriptions for the user
		subscriptions = frappe.get_all(
			"Push Subscription",
			filters={"user": user, "is_active": 1},
			fields=["name", "endpoint", "p256dh_key", "auth_key"]
		)
		
		if not subscriptions:
			return {"success": False, "message": "No active subscriptions found for user"}
		
		# Get VAPID keys from Service Worker
		service_worker = frappe.get_single("Service Worker")
		
		if not service_worker.vapid_public_key or not service_worker.vapid_private_key:
			frappe.throw("VAPID keys not configured. Please generate keys in Service Worker settings.")
		
		if not service_worker.vapid_email:
			frappe.throw("VAPID email not configured. Please set email in Service Worker settings.")
		
		# Prepare notification payload
		notification_data = data or {}
		payload = {
			"title": title,
			"body": body,
			"data": notification_data,
			"icon": frappe.utils.get_url("/assets/frappe/images/favicon.png"),
			"badge": frappe.utils.get_url("/assets/frappe/images/favicon.png")
		}
		
		# Send to all user's subscriptions
		success_count = 0
		failed_subscriptions = []
		
		for sub in subscriptions:
			try:
				subscription_info = {
					"endpoint": sub.endpoint,
					"keys": {
						"p256dh": sub.p256dh_key,
						"auth": sub.auth_key
					}
				}
				
				# Send push notification
				webpush(
					subscription_info=subscription_info,
					data=json.dumps(payload),
					vapid_private_key=service_worker.vapid_private_key,
					vapid_claims={
						"sub": f"mailto:{service_worker.vapid_email}"
					}
				)
				
				success_count += 1
				
			except WebPushException as e:
				# Handle expired or invalid subscriptions
				if e.response and e.response.status_code in [404, 410]:
					# Subscription expired or invalid, deactivate it
					frappe.db.set_value("Push Subscription", sub.name, "is_active", 0)
					failed_subscriptions.append(sub.name)
				else:
					frappe.log_error(
						f"Push notification failed for {sub.name}: {str(e)}",
						"Push Notification Error"
					)
			except Exception as e:
				frappe.log_error(
					f"Unexpected error sending push to {sub.name}: {str(e)}",
					"Push Notification Error"
				)
		
		# Commit deactivations
		if failed_subscriptions:
			frappe.db.commit()
		
		return {
			"success": True,
			"message": f"Sent to {success_count}/{len(subscriptions)} subscriptions",
			"sent_count": success_count,
			"failed_count": len(failed_subscriptions)
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Push Notification Error")
		return {"success": False, "message": str(e)}


def send_push_from_notification_log(doc, method=None):
	"""
	Automatically send push notification when a Notification Log is created
	This function is called from Server Script
	
	Args:
		doc: Notification Log document
		method: Hook method (not used)
	"""
	# Only send push if notification is for a specific user
	if not doc.for_user or not doc.subject:
		return
	
	try:
		# Send push notification
		send_push_notification(
			user=doc.for_user,
			title=doc.subject,
			body=doc.email_content or doc.subject,
			data={
				"document_type": doc.document_type,
				"document_name": doc.document_name,
				"notification_log": doc.name,
				"url": f"/app/notification-log/{doc.name}"
			}
		)
	except Exception as e:
		# Log error but don't fail notification creation
		frappe.log_error(
			f"Push notification failed for Notification Log {doc.name}: {str(e)}",
			"Push Notification Error"
		)
