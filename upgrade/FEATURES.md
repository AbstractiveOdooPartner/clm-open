# Feature list of PEP VZW, the UAT script of phase 9

The feature tags of the READMEs on the upgrade branch (phase 2, source 17.0), with the choice of the
audit. The key users test each line in the validation form of phase 9.

| Module | Summary (nl_BE) | Choice | Tags |
| --- | --- | --- | --- |
| `clm_contact_manager` | Leden beheren hun eigen gegevens in het portaal: de pagina Mijn account toont het contactformulier van Odoo, met de velden die het team erop zette. Nieuwe accounts zonder uitnodiging krijgen een controlevraag tegen robots. | Port (awaits the customer, HUMAN-TODO item 6) | `PEP-MIJN-ACCOUNT`, `PEP-LOGIN-ACCOUNT` (decision: item 4), `PEP-OPSLAAN`, `PEP-CONTROLEVRAAG`, `PEP-PORTAAL-VELDEN` |
| `clm_contact_manager_website_fix` | Zorgt dat het formulier op Mijn account ook laadt wanneer de website van Odoo geïnstalleerd is. | Port, merge into `clm_contact_manager` in phase 5 (awaits the customer) | `PEP-MIJN-ACCOUNT-WEBSITE` |

6 tags, 18 tagged places in the code (`grep -rn "\[PEP-" clm_*`). `validation_form.py` lint on
the 6 key-user lines: 0 problems.

Not checked per feature: the production data (`count(*)` per field, last write, users per group,
skill phase 2 step 1c). The production database is not reachable (HUMAN-TODO item 3). The use of
the control question is the system parameter `clm_contact_manager.signup_question` on production:
not known.
