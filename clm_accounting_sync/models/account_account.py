from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    sync_db_res_id = fields.Integer(
        copy=False, string="Connected db id"
    )  # field to store record id of database which is synced with current database
