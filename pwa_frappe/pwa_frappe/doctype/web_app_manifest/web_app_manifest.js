// Copyright (c) 2021, Md Omar Faruk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Web App Manifest", {
	configure_pwa: function (frm) {
		frappe.call({
			method: "pwa_frappe.pwa_frappe.doctype.web_app_manifest.web_app_manifest.configure_pwa",
			callback: function () {
				frappe.show_alert({ message: __("Web app was configured"), indicator: "green" });
			},
		});
	},
});
