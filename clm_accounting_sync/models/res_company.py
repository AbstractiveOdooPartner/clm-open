import logging
import pprint

from odoo import fields, models, _

from ..services.odoo_rpc import OdooRPC

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    odoo_url = fields.Char("URL")
    odoo_db = fields.Char("DB")
    odoo_username = fields.Char("Username")
    odoo_uid = fields.Char("UID")
    odoo_password = fields.Char("Password")

    # region Contact sync (C to E)
    def contact_sync(self):
        # ToDo : Add time stamp to filter
        contacts = self.env["res.partner"].search([("active", "=", True)])
        for contact in contacts:
            if contact.sync_db_res_id:
                self._update_contact(contact)
            else:
                self._create_contact(contact)

    def _create_contact(self, contact):
        r = self._get_odoorpc()
        obj_id = r.object_create(model="res.partner", fields=self._contact_data(contact))
        if obj_id:
            contact.sync_db_res_id = obj_id
            _logger.info("contact ID : %s created", pprint.pformat(contact.id))

    def _update_contact(self, contact):
        r = self._get_odoorpc()
        obj = r.object_update(model="res.partner", fields=self._contact_data(contact), obj_id=contact.sync_db_res_id)
        if obj is None:
            self._create_contact(contact=contact)
        else:
            _logger.info("contact ID : %s updated", pprint.pformat(contact.id))

    def _contact_data(self, contact):
        parent_id = False
        if contact.parent_id:
            if not contact.parent_id.sync_db_res_id:
                self._create_contact(contact.parent_id)
            parent_id = contact.parent_id.sync_db_res_id
        data = {
            "name": contact.name,
            "street": contact.street or "",
            "street2": contact.street2 or "",
            "zip": contact.zip or "",
            "city": contact.city or "",
            "country_id": contact.country_id.id or False,
            "email": contact.email or "",
            "vat": contact.vat or "",
            "parent_id": parent_id,
        }
        return data

    # endregion Contact sync (C to E)
    # region Move sync
    def move_sync(self):
        moves = self.env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("sync_db_res_id", "=", False),
                ("move_type", "in", ("out_invoice","out_refund")),
            ], order="id asc"
        )
        for move in moves:
            if self._move_required_fields_check(move):
                self._create_move(move)

    def _create_move(self, move):
        r = self._get_odoorpc()
        obj_id = r.object_create(model="account.move", fields=self._move_data(move))
        if obj_id:
            move.sync_db_res_id = obj_id
            _logger.info("move ID : %s  created", pprint.pformat(move.id))
            self._move_state_change(move)
            move.message_post(body=_("Move synced to connected database"), author_id=self.env.ref("base.partner_root").id)

    def _move_data(self, move):
        if not move.partner_id.sync_db_res_id:
            self._create_contact(move.partner_id)
        else:
            self._update_contact(move.partner_id)
        data = {
            "move_type": move.move_type,
            "partner_id": move.partner_id.sync_db_res_id,
            "payment_reference": move.payment_reference or "",
            "ref": move.ref or "",
            "journal_id": move.journal_id.sync_db_res_id,
            "invoice_date": str(move.invoice_date),
            "invoice_date_due": str(move.invoice_date_due),
            "invoice_line_ids": self._move_lines_data(move.invoice_line_ids),
        }
        return data

    def _move_lines_data(self, invoice_lines):
        invoice_lines_data = []

        for line in invoice_lines:
            invoice_line = [
                0,
                0,
            ]
            data = {
                "account_id": line.account_id.sync_db_res_id,
                "name": line.name or "",
                "quantity": line.quantity,
                "price_unit": line.price_unit,
                "tax_ids": [id.sync_db_res_id for id in line.tax_ids] or [],
            }
            invoice_line.append(data)
            invoice_lines_data.append(tuple(invoice_line))

        return invoice_lines_data

    def _move_state_change(self, move):
        r = self._get_odoorpc()
        obj = r.object_update(model="account.move", fields={"state": move.state}, obj_id=move.sync_db_res_id)
        if obj is not None:
            _logger.info("Move state : %s updated", pprint.pformat(move.id))
            return True
        return False

    def _move_required_fields_check(self, move):
        user_info_data = []
        tax_ids = []
        account_ids = []
        lines = move.invoice_line_ids

        if not move.journal_id.sync_db_res_id:
            user_info_data.append(f"Journal: {move.journal_id.name}")

        for l in lines:
            tax_ids.extend([id for id in l.tax_ids])
            account_ids.append(l.account_id)
        tax_ids = list(set(tax_ids))
        for tax in tax_ids:
            if not tax.sync_db_res_id:
                user_info_data.append(f"Tax: {tax.name}")
        for account in account_ids:
            if not account.sync_db_res_id:
                user_info_data.append(f"Account: {account.code}")

        if not user_info_data:
            return True

        note = _("Missing ID of records to match with connected database: ") + ", ".join(user_info_data)
        return self._create_activity(summary=_("Synchronization Failed"), note=note, model="account.move", rec=move)

    # endregion Move sync
    # region payment sync
    # move paymnet sync
    def move_payment_sync(self):
        moves = self.env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("sync_db_res_id", "!=", False),
                ("payment_state", "=", "paid"),
                ("move_type", "in", ("out_invoice","out_refund")),
                ("sync_db_payment_res_id", "=", False),
            ]
        )

        for move in moves:
            self._create_payment_register(move)

    def _create_payment_register(self, move):
        r = self._get_odoorpc()
        payments = move._get_reconciled_payments() or []
        for payment in payments:
            obj_id = r.object_create(
                model="account.payment.register",
                fields=self._payment_data(payment),
                context=self._payment_context_data(move),
            )
            if obj_id:
                self._payment_update(obj_id, move)

    def _payment_data(self, payment):

        if not payment.partner_id.sync_db_res_id:
            self._create_contact(payment.partner_id)
        else:
            self._update_contact(payment.partner_id)
        data = {
            "payment_type": payment.payment_type,
            "partner_type": payment.partner_type,
            "partner_id": payment.partner_id.sync_db_res_id,
            "payment_method_line_id": payment.payment_method_line_id.id,
            "amount": payment.amount,
            "payment_date": str(payment.create_date.date()),
            "journal_id": payment.journal_id.sync_db_res_id,
            "communication": payment.ref,
        }
        return data

    def _payment_context_data(self, move):
        data = {"active_model": "account.move", "active_ids": move.sync_db_res_id}
        return data

    def _payment_update(self, obj_id, move):
        r = self._get_odoorpc()
        obj = r.action_execute(model="account.payment.register", obj_id=obj_id, odoo_action="action_create_payments")
        if obj is not None:
            _logger.info("payment created for move : %s", pprint.pformat(move.id))
            move.sync_db_payment_res_id = obj.get("res_id")
            return True
        return False

    # endregion payment sync
    # region Move payment status sync
    def payment_status_sync(self):
        payment_status = self._get_payment_status()
        for ps in payment_status:
            moves = self.env["account.move"].search(
                [("payment_state", "!=", "paid"), ("sync_db_res_id", "=", ps.get("id"))]
            )
            for move in moves:
                move.payment_state = ps.get("payment_state")

    def _get_payment_status(self):
        r = self._get_odoorpc()
        domain = [["payment_state", "=", "paid"]]
        search_res = r.objects_search_read(model="account.move", domain=domain, fields=["id", "payment_state"])
        return search_res

    # endregion Move payment status sync
    # region tax sync

    def tax_sync(self):
        taxes = self._get_taxes()
        # ToDo: code imp
        for tax in taxes:
            odoo_c_taxes = self.env["account.tax"].search([("sync_db_res_id", "=", False)])
            for oc_tax in odoo_c_taxes:
                if (
                    oc_tax.type_tax_use == tax.get("type_tax_use")
                    and oc_tax.amount == tax.get("amount")
                    and oc_tax.name == tax.get("name")
                ):
                    oc_tax.sync_db_res_id = tax.get("id")

    def _get_taxes(self):
        r = self._get_odoorpc()
        domain = [["active", "=", True]]
        search_res = r.objects_search_read(
            model="account.tax", domain=domain, fields=["type_tax_use", "amount", "id", "name"]
        )
        return search_res

    # endregion tax sync
    # region journal sync

    def journal_sync(self):
        journals = self._get_journals()
        for j in journals:
            oc_journals = self.env["account.journal"].search([("sync_db_res_id", "=", False)])
            for journal in oc_journals:
                if journal.code == j.get("code"):
                    journal.sync_db_res_id = j.get("id")

    def _get_journals(self):
        r = self._get_odoorpc()
        domain = [["active", "=", True]]
        search_res = r.objects_search_read(model="account.journal", domain=domain, fields=["code", "id"])
        return search_res

    # endregion journal sync
    # region account sync

    def account_sync(self):
        accounts = self._get_accounts()
        for a in accounts:
            oc_accounts = self.env["account.account"].search([("sync_db_res_id", "=", False)])
            for account in oc_accounts:
                if account.code == a.get("code"):
                    account.sync_db_res_id = a.get("id")

    def _get_accounts(self):
        r = self._get_odoorpc()
        domain = [["code", "!=", False]]
        search_res = r.objects_search_read(model="account.account", domain=domain, fields=["code", "id"])
        return search_res

    # endregion account sync

    def _get_odoorpc(self):
        company = self.env.user.company_id
        r = OdooRPC(company)
        return r

    def _create_activity(self, summary, note, model, rec):
        data = {
            "res_id": rec.id,
            "res_model_id": self.env["ir.model"].search([("model", "=", model)]).id,
            "summary": summary,
            "note": note,
            "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,  # ToDo
            "date_deadline": fields.Date.today(),
            "user_id": self.env.ref("base.user_root").id,  # OdooBot
        }

        self.env["mail.activity"].create(data)
        return False
