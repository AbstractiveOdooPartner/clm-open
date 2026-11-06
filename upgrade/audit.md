# Audit of clm-open for PEP VZW, Odoo 17.0 → 20.0

Phases 0 and 1 of the upgrade, run 2026-11-06 on the repository
`AbstractiveOdooPartner/clm-open` and a fresh 17.0 database (production itself was not reachable).

## Verdict

| Question | Answer | Evidence |
| --- | --- | --- |
| Is the remote a fork? | No (default branch `master`) | GitHub API, read by agentd for `brief.md` |
| Which branch does a 17.0 production run? | `17.0`, not `enterprise` | See "The production branch" below |
| Modules on the production branch | 2 own modules: `clm_contact_manager`, `clm_contact_manager_website_fix` | `git ls-tree origin/17.0` |
| Installed in production? | UNKNOWN for every module | No dump, SQL, RPC or shell access to environment 502 |
| Studio and database-only customizations | UNKNOWN; the code proves they exist (Studio fields on the portal form) | `models/portal_form_access.py`, commit `eb4265a` |
| `upgrade/before.json` (inventory of the source) | Not made | Needs the production database |
| Source tests (17.0, fresh database, module + `website`) | 6 of 6 green after 2 fixes, 0 ERROR | `src_gate6` log; see "Source baseline" |
| Security hole found on the source | Portal users could write to any contact | See "Security" |

## The production branch

`brief.md` names `enterprise` as the production branch. That branch cannot run on Odoo 17.0:

| Branch | Commits | Last commit | Manifest versions | Loads on 17.0? |
| --- | --- | --- | --- | --- |
| `enterprise` | 2 | 2022-09-19 `409d4b2` `[ADD] clm_simple_acc_enterprise` | 14.0.x and 15.0.x | No: `ValueError: Invalid version '15.0.0.0.0'`, the registry does not load (`repro_create mode=custom`, 2026-11-06 07:38) |
| `master` | 12 | 2023-03-15 `a5442fe` | 14.0.x and 15.0.x | No (same versions) |
| `17.0` | 21 | 2026-09-19 `481be07` `[IMP] clm_contact_manager: control question on the signup form` | `17.0.0.1.0`, `17.0.0.0.0` | Yes: both modules install, `state = installed` |

`17.0` descends from `master`. It holds `ad83479 [MIG] Make clm_contact_manager work in v17`
(2024-07-10), `b65ab34 [RM] removed non17.0 modules` (2024-08-06), and fixes from 2025 and
2026 (`d5e2b60 [FIX][H4573]`, `eb4265a`, `c5c9159`, `481be07`). The brief's line "this code got
no change since 2022" is true for `enterprise` only.

The upgrade branch `support-agent/upgrade-20.0` therefore starts from `origin/17.0` (`481be07`).
This is not proven on the server itself: the checkout there (remote, branch, commit) is not
read yet. It is item 1 of `HUMAN-TODO.md`.

## Modules

### On the production branch (`17.0`)

| Module | Python lines | What it does | Risk on 20.0 | Choice |
| --- | --- | --- | --- | --- |
| `clm_contact_manager` | 382 | `/my/account` shows an embedded back-end contact form (Studio extends it), login redirect of portal users to `/my/account`, control question on `/web/signup`, portal read access on the Studio models of that form | MEDIUM-HIGH: see the next table | Port (proposal) |
| `clm_contact_manager_website_fix` | 0 (manifest only) | Adds 3 website assets to the bundle of `clm_contact_manager`, so the form loads with `website` installed. `auto_install` | LOW, but the paths must exist on 20.0 | Port, or merge into `clm_contact_manager` in phase 5 (proposal) |

What breaks on 20.0, checked in `odoo-core/20.0` (commit `3a00e0b21`, 2026-10-30):

| Point | 17.0 code | 20.0 source |
| --- | --- | --- |
| Asset bundle `clm_contact_manager.webclient` | Copy of `project.webclient` 17.0, 87 entries | 23 paths no longer exist: all of `web_editor/`, jQuery, select2, `legacy/scss`, `font-awesome.css`. Rebuild it from `project.webclient` 20.0 (`project/__manifest__.py:113`) |
| JS `useService("user")` | `contact_sharing.js:15` | No `user` service; `user` is the module `@web/core/user` |
| `conf.server_wide_modules`, `ir.http.get_web_translations_hash` | `controllers/portal.py:15-22` | `get_web_translations_hash` is gone from `web/models/ir_http.py`; project sharing 20.0 no longer sends cache hashes |
| `_prepare_signup_values(self, qcontext)` | `controllers/auth_signup.py:56` | `_prepare_signup_values(self, qcontext, *, validate_email=False)` (`auth_signup/controllers/main.py:161`) |
| `from odoo import _` in a controller | `controllers/auth_signup.py:3` | `request.env._()` (skill, phase 3 step 6) |
| Override of the whole record `portal.portal_my_details` | `templates/contact_portal.xml:5` | The record moved to `portal/views/address_templates.xml:480`; still a full replacement of a core template |
| `web.FormStatusIndicator` xpaths on `o_form_button_save` / `o_form_button_cancel` | `form_status_indicator.xml` | Both buttons still exist (`form_status_indicator.xml:7-26`); the icon is now `oi` with `data-icon` |
| `auth_signup.fields`, `div.field-confirm_password` | `templates/auth_signup_templates.xml` | Both still exist (`auth_signup_login_templates.xml:12,24`) |

`audit.py` (`upgrade/audit.json`): 2 modules, 407 Python lines, 2 JS files, 1 SCSS file, 1
runtime hint (the `_` import). Applicable `upgrade_code` scripts: 8, from `17.5-01-tree-to-list`
to `18.5-00-no-tax-tag-invert`; `20.0-00-search-date-filters` and `owl3-migration` are run in
phase 3 as well.

### Named in the brief, not on the production branch

`b65ab34 [RM] removed non17.0 modules` deleted these from `17.0` in 2024. Whether production
still has any of them installed is not known.

| Module | Author | Last version in the repo | Target version upstream | Choice |
| --- | --- | --- | --- | --- |
| `clm_base` | Abstractive | 15.0 (`master`) | own code | Question: installed? |
| `clm_accounting_sync` | Abstractive | 15.0 (`master`) | own code | Question: installed? |
| `clm_simple_acc` | Abstractive | 15.0 | own code | Question: installed? |
| `clm_simple_acc_enterprise` | Abstractive | 15.0 (`enterprise`) | own code | Question: installed? |
| `partner_firstname` | OCA | 15.0 | OCA/partner-contact: 17.0, 18.0, 19.0; no 20.0 | Question: installed? |
| `membership_extension` | OCA | 14.0 | OCA/vertical-association: 17.0, 18.0; no 19.0, no 20.0 | Question: installed? |
| `membership_variable_period` | OCA | 14.0 | OCA/vertical-association: 17.0 to 19.0; no 20.0 | Question: installed? |
| `account_budget_oca` | OCA | 15.0 | OCA/account-budgeting: 17.0 to 19.0; no 20.0 | Question: installed? |
| `website_event_require_login` | OCA (Tecnativa) | 14.0 | not checked | Question: installed? |

A module installed in production that no repository holds is first a question about the remote
(skill, phase 0). The answer comes from `ir_module_module` on production.

## Source baseline (17.0)

| Run | Database | Result |
| --- | --- | --- |
| `-i clm_contact_manager,website --test-enable`, branch `17.0` as is | `src_gate` | 5 failed of 1809: the 4 tests of `TestSignupQuestion` (404 on `/web/signup`) and `portal.TestWebLoginPortal.test_web_login_external` |
| same, with fix `b9ec813` | `src_gate2` | 1 failed of 1809: `portal.TestWebLoginPortal.test_web_login_external` |
| `--test-tags /clm_contact_manager,/clm_contact_manager_website_fix`, with `b9ec813` and `dc3427e` | `src_gate6` | 0 failed of 6, 0 ERROR, 0 WARNING, exit 0 |

- **404 on `/web/signup`**: with `website` installed, `website/models/res_users.py:67` takes the
  signup scope from the website (`auth_signup_uninvited`, default `b2b`), not from the system
  parameter that the test set. The test now opens signup on each website too. Fix `b9ec813`.
- **`portal.test_web_login_external`** asserts that a portal user lands on `/my` after login.
  `WebsiteHome._login_redirect` (`controllers/portal.py:56`) sends them to `/my/account` on
  purpose (`d99557c [IMP] redirect on login to /my/account`, 2023). Both cannot hold. This is a
  decision: `HUMAN-TODO.md`, item 4.

## Security

`security/ir.model.access.csv` sets the core row `base.access_res_partner_portal` to read +
write. The only portal rule on `res.partner` (`base.res_partner_portal_public_rule`) has
`perm_write = False`, so it does not limit a write. Proven on 17.0 (`src_gate2`, `odoo shell`):
a portal user cannot read another contact (AccessError), and **can write to it** (its e-mail
changed). Any member with a portal login could change any contact of the company over
JSON-RPC.

Fix `dc3427e`: rule `clm_contact_manager.res_partner_portal_write_rule`, write only, domain
`[('id', 'child_of', user.commercial_partner_id.id)]` (the scope of the read rule), with
`tests/test_portal_partner_access.py` (2 tests, green on 17.0). This fix belongs on production
now, on 17.0: `HUMAN-TODO.md`, item 2.

## What needs a person

See `HUMAN-TODO.md`: access to the production database and the server, the production branch,
the security fix on 17.0, the login redirect, and the choice per module.

## What was checked and not found

- No submodules (`.gitmodules` absent), no `migrations/` folder, no `.pre-commit-config.yaml`,
  no lint configuration.
- No `attrs` or `states` in the XML (the source is 17.0: `replace_attrs.py` does not apply).
- No `_sql_constraints`, no `type='json'` routes, no `self._cr` / `self._context`.
- Not checked: Studio views and fields, automated and server actions, mail templates, website
  copies of templates (all need the production database).
