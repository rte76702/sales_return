# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "sales_return"
app_title = "Sales Return"
app_publisher = "rte76702"
app_description = "Handle returns"
app_icon = "octicon octicon-file-directory"
app_color = "orange"
app_email = "crossxcell99@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sales_return/css/sales_return.css"
# app_include_js = "/assets/sales_return/js/sales_return.js"

# include js, css files in header of web template
# web_include_css = "/assets/sales_return/css/sales_return.css"
# web_include_js = "/assets/sales_return/js/sales_return.js"

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
# get_website_user_home_page = "sales_return.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sales_return.install.before_install"
# after_install = "sales_return.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sales_return.notifications.get_notification_config"

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
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	'Sales Invoice': {
		'validate': 'sales_return.utils.prevent_submission',
		'on_submit': 'sales_return.utils.prevent_submission'
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sales_return.tasks.all"
# 	],
# 	"daily": [
# 		"sales_return.tasks.daily"
# 	],
# 	"hourly": [
# 		"sales_return.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sales_return.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sales_return.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sales_return.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sales_return.event.get_events"
# }

