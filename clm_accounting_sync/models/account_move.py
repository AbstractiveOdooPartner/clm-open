from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    sync_db_res_id = fields.Integer(
        copy=False
    )  # field to store record id of database which is synced with current database
    sync_db_payment_res_id = fields.Integer(copy=False)
