from odoo import models, fields, api
from datetime import timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Customer')
    is_lead = fields.Boolean(string='Lead')
    is_vendor = fields.Boolean(string='Vendor')
    is_employee = fields.Boolean(string='Employee')
    responsible_user_id = fields.Many2one('res.users', string='Responsible Salesperson')