import random

from odoo import _
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

QUESTION_PARAM = "clm_contact_manager.signup_question"
SESSION_KEY = "clm_signup_question"
# The sum is at most 9: the answer is 1 digit.
NUMBER_WORDS = {
    "nl": ["één", "twee", "drie", "vier", "vijf"],
    "fr": ["un", "deux", "trois", "quatre", "cinq"],
    "en": ["one", "two", "three", "four", "five"],
}


# [PEP-CONTROLEVRAAG]
class ClmAuthSignupHome(AuthSignupHome):
    """A control question on /web/signup: a sum in words, which a robot does not read.

    The system parameter clm_contact_manager.signup_question = True switches it on. The
    numbers are in the session, so the server checks the answer.
    """

    def _clm_signup_question_enabled(self, qcontext):
        # An invitation or a password reset has a token: the person proved the address.
        if qcontext.get("token"):
            return False
        get_param = request.env["ir.config_parameter"].sudo().get_param
        return get_param(QUESTION_PARAM) == "True"

    def _clm_new_signup_numbers(self):
        numbers = [random.randint(1, 5), random.randint(1, 4)]
        request.session[SESSION_KEY] = numbers
        return numbers

    def _clm_signup_question_text(self, numbers):
        words = NUMBER_WORDS.get((request.env.lang or "en_US")[:2])
        first, second = (words[number - 1] for number in numbers) if words else numbers
        return _(
            "How much is %(first)s plus %(second)s? Answer with a digit.",
            first=first,
            second=second,
        )

    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        if self._clm_signup_question_enabled(qcontext):
            numbers = request.session.get(SESSION_KEY)
            # A post keeps the question that the page showed.
            if request.httprequest.method != "POST" or not numbers:
                numbers = self._clm_new_signup_numbers()
            qcontext["clm_signup_question"] = self._clm_signup_question_text(numbers)
        return qcontext

    def _prepare_signup_values(self, qcontext):
        if self._clm_signup_question_enabled(qcontext):
            # 1 answer for each question: a wrong answer gets a new question.
            numbers = request.session.pop(SESSION_KEY, None)
            answer = (request.params.get("clm_signup_answer") or "").strip()
            if not numbers or answer != str(sum(numbers)):
                qcontext["clm_signup_question"] = self._clm_signup_question_text(
                    self._clm_new_signup_numbers()
                )
                raise UserError(_("The answer to the control question is not correct."))
        return super()._prepare_signup_values(qcontext)
