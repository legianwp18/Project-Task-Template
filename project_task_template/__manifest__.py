# -*- coding: utf-8 -*-
{
	'name': "Project Task Template",
	'summary': """
		Project Task Template
	""",
	'description': """
		Project Task Template
	""",
	'website': 'https://www.odoo.com/app/project',
	'category': 'Services/Project',
	'version': '1.1',
	'depends': ['base','project'],
	'data': [
		'security/ir.model.access.csv',
		'views/project_task_templates.xml',
		'views/project_templates.xml',
	],
	'license': 'LGPL-3',
}