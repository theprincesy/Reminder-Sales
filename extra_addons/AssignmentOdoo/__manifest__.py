# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reminder Salesperson',
    'version': '1.0',
    'category': 'Management',
    'sequence': -300,
    'summary': 'Track addons',
    'description': "",
    'website': 'https://www.odoo.com',
    'depends': [
        'base','sale', 'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'data/send_event_reminders.xml',
        'views/event_views.xml',
        'views/event_menu.xml',
        'data/test_data.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
