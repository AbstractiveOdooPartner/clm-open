from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPortalPartnerAccess(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_user = cls.env["res.users"].create(
            {
                "name": "Portal Member",
                "login": "portal.member@example.com",
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )
        cls.other_partner = cls.env["res.partner"].create(
            {"name": "Other Member", "email": "other.member@example.com"}
        )

    def test_portal_user_writes_own_partner(self):
        partner = self.portal_user.partner_id.with_user(self.portal_user)
        partner.write({"phone": "+32 470 00 00 00"})
        self.assertEqual(self.portal_user.partner_id.phone, "+32 470 00 00 00")

    def test_portal_user_cannot_write_other_partner(self):
        with self.assertRaises(AccessError):
            self.other_partner.with_user(self.portal_user).write(
                {"email": "changed@example.com"}
            )
        self.assertEqual(self.other_partner.email, "other.member@example.com")
