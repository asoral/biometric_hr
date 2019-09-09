# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "biometric_hr"
app_title = "Biometric HR"
app_publisher = "VHRS"
app_description = "Biometry"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ramya.a@voltechgroup.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/biometric_hr/css/biometric_hr.css"
# app_include_js = "/assets/biometric_hr/js/biometric_hr.js"

# include js, css files in header of web template
# web_include_css = "/assets/biometric_hr/css/biometric_hr.css"
# web_include_js = "/assets/biometric_hr/js/biometric_hr.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "biometric_hr.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "biometric_hr.install.before_install"
# after_install = "biometric_hr.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "biometric_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
	# "Attendance": {
    #     "on_update_after_submit": "biometric_hr.biometric_hr.doctype.late_in_register.late_in_register.update_time_details"
    # },
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"biometric_hr.tasks.all"
# 	],
	"daily": [
		"biometric_hr.biometric_hr.doctype.late_in_register.late_in_register.update_time_details"
	],
# 	"hourly": [
# 		"biometric_hr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"biometric_hr.tasks.weekly"
# 	]
	"monthly": [
		"biometric_hr.custom.calcute_latein_earlyout"
	]
}

# Testing
# -------

# before_tests = "biometric_hr.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "biometric_hr.event.get_events"
# }

