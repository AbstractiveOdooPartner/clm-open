from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sync_db_res_id = fields.Integer()
