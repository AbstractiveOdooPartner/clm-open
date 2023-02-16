from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    website_form_entry_count = fields.Integer(compute="_compute_website_form_entry_count")

    def _compute_website_form_entry_count(self):
        for partner in self:
            partner.website_form_entry_count = self.env["website.form.entry"].search_count([("partner_id", "=", partner.id)])

    def action_view_website_form_entries(self):
        self.ensure_one()
        action = self.env.ref("clm_base.website_form_entry_action").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        return action
