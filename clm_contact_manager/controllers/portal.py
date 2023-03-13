from odoo import conf, http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.addons.web.controllers.main import HomeStaticTemplateHelpers, Home


class ContactCustomerPortal(CustomerPortal):
    def _prepare_contact_sharing_session_info(self, contact):
        session_info = request.env["ir.http"].session_info()
        user_context = request.session.get_context() if request.session.uid else {}
        mods = conf.server_wide_modules or []
        qweb_checksum = HomeStaticTemplateHelpers.get_qweb_templates_checksum(
            debug=request.session.debug, bundle="clm_contact_manager.assets_qweb"
        )
        if request.env.lang:
            lang = request.env.lang
            session_info["user_context"]["lang"] = lang
            # Update Cache
            user_context["lang"] = lang
        lang = user_context.get("lang")
        translation_hash = request.env["ir.translation"].get_web_translations_hash(mods, lang)
        cache_hashes = {
            "qweb": qweb_checksum,
            "translations": translation_hash,
        }

        contact_company = request.env.user.company_id
        session_info.update(
            cache_hashes=cache_hashes,
            action_name="clm_contact_manager.res_partner_sharing_action",
            contact_id=contact.id,
            view_id=request.env.ref("clm_contact_manager.res_partner_sharing_view_form").id,
            user_companies={
                "current_company": contact_company.id,
                "allowed_companies": {
                    contact_company.id: {
                        "id": contact_company.id,
                        "name": contact_company.name,
                    },
                },
            },
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
        if not redirect and not request.env['res.users'].sudo().browse(uid).has_group('base.group_user'):
            redirect = '/my/account'
        return super()._login_redirect(uid, redirect=redirect)
