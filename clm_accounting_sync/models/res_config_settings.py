from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    odoo_url = fields.Char("URL", related="company_id.odoo_url", readonly=False)
    odoo_username = fields.Char("Username", related="company_id.odoo_username", readonly=False)
    odoo_password = fields.Char("Password", related="company_id.odoo_password", readonly=False)
    odoo_db = fields.Char("DB", related="company_id.odoo_db", readonly=False)
    odoo_uid = fields.Char("UID", related="company_id.odoo_uid")

    def action_sync_taxes(self):
        self.env.company.tax_sync()

    def action_sync_journals(self):
        self.env.company.journal_sync()

    def action_sync_accounts(self):
        self.env.company.account_sync()

    def action_sync_auth(self):
        r = self.env.company._get_odoorpc()
        auth = r.authenticate()
        if auth.get("uid"):
            return self.notify(val=True, msg="Authentication successful")
        return self.notify(val=False, msg="Authentication failed")

    def notify(self, val, msg):
        if val:
            ntype = "success"
        else:
            ntype = "warning"
        notify = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Info"),
                "message": _(msg),
                "sticky": False,
                "type": ntype,
            },
        }
        return notify
