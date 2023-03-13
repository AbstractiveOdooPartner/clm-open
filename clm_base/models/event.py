from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    extra_registration_cta_bottom = fields.Boolean(
        string="Extra registratieknop onderaan",
    )
