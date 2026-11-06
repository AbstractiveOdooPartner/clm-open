import logging

from lxml import etree

from odoo import api, models

_logger = logging.getLogger(__name__)

PORTAL_FORM = "clm_contact_manager.res_partner_sharing_view_form"


# [PEP-PORTAAL-VELDEN]
class PortalFormAccess(models.AbstractModel):
    """Read access on the Studio models that /my/account shows.

    A relational field on the portal form makes the client read its comodel. Without an
    ir.model.access row for the portal group the whole form dies with an AccessError, so
    the grant has to follow whatever Studio puts on the view.
    """

    _name = "clm.portal.form.access"
    _description = "CLM Portal Form Access"

    @api.model
    def _portal_form_views(self):
        view = self.env.ref(PORTAL_FORM, raise_if_not_found=False)
        if not view:
            return self.env["ir.ui.view"]
        # get_combined_arch() drops Studio views while modules are loading, so collect the
        # inheritance chain by hand and parse each arch on its own.
        views = view.sudo()
        while True:
            children = views.search(
                [
                    ("inherit_id", "in", views.ids),
                    ("mode", "=", "extension"),
                    ("active", "=", True),
                ]
            )
            if children <= views:
                return views
            views |= children

    @api.model
    def _portal_form_relations(self):
        views = self._portal_form_views()
        if not views:
            return []
        names = set()
        for view in views:
            arch = etree.fromstring(view.arch_db)
            names |= {el.get("name") for el in arch.iter("field") if el.get("name")}
        fields = (
            self.env["ir.model.fields"]
            .sudo()
            .search(
                [
                    ("model", "=", views[0].model),
                    ("name", "in", sorted(names)),
                    ("relation", "!=", False),
                ]
            )
        )
        # Only Studio models: everything else is standard and already has its own ACL.
        return sorted({f.relation for f in fields if f.relation.startswith("x_")})

    @api.model
    def _sync_portal_read_access(self):
        portal = self.env.ref("base.group_portal", raise_if_not_found=False)
        if not portal:
            return
        access = self.env["ir.model.access"].sudo()
        for model_name in self._portal_form_relations():
            model = (
                self.env["ir.model"]
                .sudo()
                .search([("model", "=", model_name)], limit=1)
            )
            if not model:
                continue
            if access.search_count(
                [("model_id", "=", model.id), ("group_id", "=", portal.id)]
            ):
                continue
            access.create(
                {
                    "name": "%s: portal read" % model_name,
                    "model_id": model.id,
                    "group_id": portal.id,
                    "perm_read": True,
                    "perm_write": False,
                    "perm_create": False,
                    "perm_unlink": False,
                }
            )
            _logger.info(
                "Granted portal read access on %s for the /my/account form", model_name
            )
