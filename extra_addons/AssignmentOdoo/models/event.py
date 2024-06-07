from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta,date

class Event(models.Model):
    _name = 'event.management'
    _description = 'Event Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Event Name', required=True)
    date = fields.Date(string='Event Date', required=True)
    communication_start_before = fields.Integer(string='Communication Start Before (days)', required=True)
    participant_ids = fields.Many2many('res.partner', string='Participants')

    @api.constrains('date')
    def _check_event_date(self):
        for record in self:
            if record.date and record.date < date.today():
                raise ValidationError("The event date cannot be in the past.")

    def get_event_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/web#id={self.id}&model=event.management&view_type=form"

    @api.model
    def send_event_reminders(self):
        today = fields.Date.today()
        events = self.search([('date', '>=', today)])
        for event in events:
            notify_date = event.date - timedelta(days=event.communication_start_before)
            if today == notify_date:
                for participant in event.participant_ids:
                    if participant.responsible_user_id:
                        self.env['mail.mail'].create({
                            'subject': f'Reminder: {event.name} is coming up',
                            'body_html': f'<p>Dear {participant.responsible_user_id.name},</p>'
                                         f'<p>Please start communicating with the contacts for the event {event.name}.</p>'
                                         f'<p><a href="/web#id={event.id}&model=event.management">Event Details</a></p>',
                            'email_to': participant.responsible_user_id.email,
                        }).send()

    def action_start_communication(self):
        self.ensure_one()
        participants = self.participant_ids
        chat_channel = self.env['mail.channel'].create({
            'name': f"Communication for {self.name}",
            'public': 'private',
            'channel_partner_ids': [(4, partner.id) for partner in participants],
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.channel',
            'view_mode': 'form',
            'res_id': chat_channel.id,
            'target': 'new',
        }

