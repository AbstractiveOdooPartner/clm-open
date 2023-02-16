from odoo import models, fields


class WebsiteFormEntry(models.Model):
    _name = "website.form.entry"
    _description = "Website Form Entry"
    _order = "id desc"

    name = fields.Char()
    description = fields.Text()
    email_from = fields.Char()
    partner_id = fields.Many2one("res.partner")
    type_id = fields.Many2one("website.form.entry.type")
    tag_ids = fields.Many2many("res.partner.category")

    # ====== CRUD METHODS ====== #

    def create(self, vals):
        res = super().create(vals)
        if res.type_id.apply_tags:
            res.partner_id.category_id = [fields.Command.link(tag.id) for tag in res.tag_ids]
        return res


class WebsiteFormEntryType(models.Model):
    _name = "website.form.entry.type"
    _description = "Website Form Entry Type"
    _order = "name"

    name = fields.Char()
    active = fields.Boolean(default=True)
    apply_tags = fields.Boolean(default=False)
