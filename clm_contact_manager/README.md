CLM Contact Manager
===================

Summary
-------

Leden beheren hun eigen gegevens in het portaal: de pagina Mijn account toont het
contactformulier van Odoo, met de velden die het team erop zette. Nieuwe accounts zonder
uitnodiging krijgen een controlevraag tegen robots.

Functional
----------

- [PEP-MIJN-ACCOUNT] Meld je aan als lid en open Mijn account: je ziet het formulier met je eigen
  gegevens, je wijzigt je naam en na het opslaan staat de nieuwe naam op je account.
- [PEP-LOGIN-ACCOUNT] Meld je aan als lid op de aanmeldpagina: je komt meteen op Mijn account
  terecht en niet op het portaaloverzicht.
- [PEP-OPSLAAN] Wijzig een gegeven op Mijn account: bovenaan verschijnen een blauwe knop
  "Wijzigingen opslaan" en een knop om de wijziging te annuleren.
- [PEP-CONTROLEVRAAG] Open de pagina om zelf een account aan te maken: onder het wachtwoord staat
  een rekenvraag in woorden; met het juiste cijfer wordt je account aangemaakt, met een fout
  cijfer krijg je een melding en een nieuwe vraag.
- [PEP-PORTAAL-VELDEN] Open Mijn account als lid: elk veld van het formulier toont zijn waarde,
  ook de keuzelijsten die het team aan het formulier toevoegde, en je krijgt geen foutmelding.

Technical
---------

- PEP-MIJN-ACCOUNT: `templates/contact_portal.xml` replaces the whole core template
  `portal.portal_my_details` (same XML ID) by an iframe on `/<lang>/my/info`. That route
  (`controllers/portal.py`, `ContactCustomerPortal.contact_sharing`) renders a stand-alone web
  client, the asset bundle `clm_contact_manager.webclient`, which opens the form view
  `res_partner_sharing_view_form` on the partner of the user. The bundle and the JS are a copy of
  project sharing (`project.webclient`, `project_sharing.js`) of 17.0. The base view shows only the
  name: the customer adds fields with Studio, in the database.
  - `security/ir.model.access.csv` gives `base.group_portal` write on `res.partner` (an own row
    next to the read row of `base`), so that the form can save. `security/ir_rule.xml` limits that
    write to the own commercial partner and its contacts: the standard portal rule limits read
    only.
- PEP-LOGIN-ACCOUNT: `WebsiteHome._login_redirect` sends a non-internal user without an explicit
  redirect to `/my/account`. It replaces the `/my` of `portal`, so the core test
  `portal.TestWebLoginPortal.test_web_login_external` fails with this module installed.
- PEP-OPSLAAN: `static/src/contact_sharing/form_status_indicator.xml` and
  `contact_sharing.scss` restyle the save and discard buttons of `web.FormStatusIndicator`. The
  bundle is only loaded in the iframe, so the back end keeps the standard icons.
- PEP-CONTROLEVRAAG: `controllers/auth_signup.py`: a sum of 2 numbers in words on `/web/signup`,
  in the language of the request, kept in the session and checked on the server. On when the
  system parameter `clm_contact_manager.signup_question` is `True`. An invitation or a password
  reset (a token in the context) skips it. A wrong answer raises `UserError`, which the core
  signup controller shows as an error, and draws a new question.
- PEP-PORTAAL-VELDEN: `models/portal_form_access.py`: a relational field on the portal form makes
  the client read its comodel, and a Studio model (`x_*`) has no portal ACL, so the whole form
  fails with an AccessError. `_sync_portal_read_access` walks the active extension views of the
  form (the combined arch drops Studio views while modules load), and creates a read-only ACL for
  `base.group_portal` on each `x_*` comodel. It runs on each install and update of the module
  (`security/portal_form_access.xml`), and from the server action "CLM: update portal access for
  /my/account" after a Studio change.
- Tests: `tests/test_signup_question.py` (4, the control question, `HttpCase`),
  `tests/test_portal_partner_access.py` (2, the write rule).
