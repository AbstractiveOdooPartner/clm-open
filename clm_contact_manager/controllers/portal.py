from odoo import conf, http
from odoo.http import request, Request
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.addons.web.controllers.home import Home

request: Request


class ContactCustomerPortal(CustomerPortal):
    # NOTE: This is based on _prepare_project_sharing_session_info
    def _prepare_contact_sharing_session_info(self, contact):
        session_info = request.env["ir.http"].session_info()
        user_context = dict(request.env.context) if request.session.uid else {}
        mods = conf.server_wide_modules or []
        if request.env.lang:
            lang = request.env.lang
            session_info["user_context"]["lang"] = lang
            # Update Cache
            user_context["lang"] = lang
        lang = user_context.get("lang")
        translation_hash = request.env["ir.http"].get_web_translations_hash(mods, lang)
        cache_hashes = {
            "translations": translation_hash,
        }

        company = contact.company_id or request.env.company

        session_info.update(
            cache_hashes=cache_hashes,
            action_name="clm_contact_manager.res_partner_sharing_action",
            contact_id=contact.id,
            view_id=request.env.ref("clm_contact_manager.res_partner_sharing_view_form").id,
            user_companies={
                "current_company": company.id,
                "allowed_companies": {
                    company.id: {
                        "id": company.id,
                        "name": company.name,
                    },
                },
            },
            # FIXME: See if we prefer to give only the currency that the portal user just need to see the correct information in project sharing
            currencies=request.env["ir.http"].get_currencies(),
        )
        return session_info

    @http.route(["/my/info/"], type="http", auth="public", website=True)
    def contact_sharing(self, **kwargs):
        contact = request.env.user.partner_id
        if contact:
            session_info = self._prepare_contact_sharing_session_info(contact)
            return request.render("clm_contact_manager.contact_sharing_embed", {"session_info": session_info})


class WebsiteHome(Home):
    def _login_redirect(self, uid, redirect=None):
        if not redirect and not request.env["res.users"].sudo().browse(uid).has_group("base.group_user"):
            redirect = "/my/account"
        return super()._login_redirect(uid, redirect=redirect)
