import re

from odoo.tests import HttpCase, tagged
from odoo.tools import mute_logger

from odoo.addons.clm_contact_manager.controllers.auth_signup import NUMBER_WORDS

# The question is in the language of the request: read the numbers in each language.
VALUES = {
    word: index + 1
    for words in NUMBER_WORDS.values()
    for index, word in enumerate(words)
}


# [PEP-CONTROLEVRAAG]
@tagged("post_install", "-at_install")
class TestSignupQuestion(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        get_param = cls.env["ir.config_parameter"].sudo()
        get_param.set_param("auth_signup.invitation_scope", "b2c")
        get_param.set_param("clm_contact_manager.signup_question", "True")
        # With website installed, each website overrides the scope (default b2b).
        if "website" in cls.env:
            cls.env["website"].search([]).auth_signup_uninvited = "b2c"

    def _signup_page(self):
        page = self.url_open("/web/signup")
        self.assertEqual(page.status_code, 200)
        token = re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)
        question = re.search(r'name="clm_signup_answer"', page.text) and re.search(
            r'for="clm_signup_answer">[^<]*?\b(%s)\b[^<]*?\b(%s)\b'
            % ("|".join(VALUES), "|".join(VALUES)),
            page.text,
        )
        return page, token, question

    def _post(self, token, login, answer=None):
        data = {
            "csrf_token": token,
            "login": login,
            "name": "Signup Test",
            "password": "signup-test-1",
            "confirm_password": "signup-test-1",
        }
        if answer is not None:
            data["clm_signup_answer"] = answer
        return self.url_open("/web/signup", data=data)

    def _user(self, login):
        return self.env["res.users"].sudo().search([("login", "=", login)])

    def test_right_answer(self):
        __, token, question = self._signup_page()
        self.assertTrue(question, "The signup page shows the control question.")
        answer = VALUES[question.group(1)] + VALUES[question.group(2)]
        self._post(token, "signup.right@example.com", str(answer))
        self.assertTrue(self._user("signup.right@example.com"))

    @mute_logger("odoo.http")
    def test_wrong_answer(self):
        __, token, question = self._signup_page()
        answer = VALUES[question.group(1)] + VALUES[question.group(2)]
        response = self._post(token, "signup.wrong@example.com", str(answer + 1))
        self.assertIn("field-clm_signup_answer", response.text)
        self.assertIn("alert-danger", response.text)
        self.assertFalse(self._user("signup.wrong@example.com"))
        # The same answer again does not work: a wrong answer gets a new question.
        response = self._post(token, "signup.wrong@example.com", "")
        self.assertFalse(self._user("signup.wrong@example.com"))

    @mute_logger("odoo.http")
    def test_post_without_page(self):
        # A robot posts straight to the form, without the question in its session.
        __, token, __ = self._signup_page()
        self.url_open("/web/session/logout")
        self._post(token, "signup.robot@example.com", "7")
        self.assertFalse(self._user("signup.robot@example.com"))

    def test_question_off(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "clm_contact_manager.signup_question", "False"
        )
        __, token, question = self._signup_page()
        self.assertFalse(question)
        self._post(token, "signup.off@example.com")
        self.assertTrue(self._user("signup.off@example.com"))
