# Status of the upgrade of PEP VZW, 17.0 → 20.0, after phase 3

Code track on `support-agent/upgrade-20.0` (from `origin/17.0`), 2026-11-06. Phases 0 to 3 ran;
phase 4 starts from here.

## Verdict

| Phase | Gate | Result | Number |
| --- | --- | --- | --- |
| 0 | The remote is the code production runs | Passed, with 1 open check on the server | not a fork; `enterprise` does not load on 17.0, `17.0` does |
| 1 | The user agrees per module | Open: needs the customer and the production database | 2 modules on `17.0`, 9 modules of the brief not on `17.0`, installed list unknown |
| 2 | Each feature explained, tags in place | Passed | 2 READMEs, 6 tags, 18 tagged places, lint 0 problems |
| 2 | Platform request | Not sent | Odoo has no upgrade scripts for 20.0 yet (`brief.md`) |
| 3 | The branch is on the target version | Passed | 2 of 2 manifests on `20.0.x`, each with `UPGRADE TODO: Module unupgraded` |

`upgrade-status.sh`: modules 2, ported 0, not ported 2; **open markers: 11** (2 module markers,
9 open points with a text).

## What is proven

| Claim | Number | Command or file |
| --- | --- | --- |
| Source tests green on 17.0 after the fixes | 0 failed of 6, 0 ERROR, 0 WARNING | `odoo -d src_gate8 -i clm_contact_manager,website --test-enable --test-tags /clm_contact_manager,/clm_contact_manager_website_fix` on the 17.0 sandbox, upgrade checkout first on the addons path |
| Portal users could write any contact on 17.0 | write allowed, read refused | `odoo shell` on `src_gate2`, before `82484a8` |
| `upgrade_code` 17.0 → 20.0 ran on the repo only | 4 scripts changed 5 files, 15 scripts 0 files, 0 crashes; core checkout 0 files changed | `out/tools/run_upgrade_code_standalone.py` of run 1180 (see below), commit `[UPG][CLAUDE] Run upgrade_code 17.0 → 20.0` |
| `_()` to `request.env._()` leaves the translations alone | 2 of 2 strings extracted the same before and after | `odoo/tools/babel/python_extractor.py` of 20.0 on both versions of `controllers/auth_signup.py` |
| No view of our modules lost its definition | 2 views, 0 stale | `find_renamed_views.py` on `src_gate8` |
| No override of a method that 20.0 removed | 0 dead overrides; 3 controller overrides exist on 20.0, 1 changed signature (marked) | `find_dead_overrides.py --custom . --odoo odoo-core/20.0 --odoo enterprise/20.0` |

The `upgrade_code` runner: `run_upgrade_code.py` of the skill imports `odoo.cli`, which needs the
full server dependencies; there is no 20.0 runtime (`repro_create mode=upgrade` refuses to build
without a platform dump). `odoo/cli/upgrade_code.py` of 20.0 supports a standalone run; the
wrapper loads it that way, gives 3 scripts the real `SetDefinitions`, `groupby` and `frozendict`
compiled from the 20.0 sources, gives `19.4-00-ir-access` the core addons as read-only context,
and writes only files inside the repo. `owl3-migration` (no version prefix) ran with `--extra`.

## The commits of phases 0 to 3

| Commit | What |
| --- | --- |
| `d7a7ced` `[FIX]` | The control question tests open signup per website (404 with `website` installed) |
| `82484a8` `[FIX]` | Portal write on contacts limited to the own commercial partner, 2 tests |
| `6fcfee3` `[META]` | Audit, open decisions, log |
| `3c48c99`, `644de6d` `[META]` | READMEs and feature tags, 1 commit per module |
| `[UPG]` own ACL row | The portal write as an own ACL row, so that `19.4-00-ir-access` can convert it |
| `[UPG] Run upgrade_code` | The raw result of the tool |
| `[UPG]` `_()` | `request.env._()` in the signup controller |
| `[UPG] Bump` | Both manifests to 20.0 with the module marker |
| `[UPG] Mark` | 9 markers with a text at the open points |

## What needs a person

`HUMAN-TODO.md`: 6 items. Blocking phase 4: the production database (item 3) for the seed and the
installed module list, and the login redirect (item 4) for the gate "all tests green".

## Open points of the port (the markers)

1. Rebuild `clm_contact_manager.webclient` from `project.webclient` 20.0: 23 of 87 paths are gone.
2. `controllers/portal.py`: `odoo.conf` and `get_web_translations_hash` are gone.
3. `controllers/portal.py`: the login redirect against the core test (decision).
4. `controllers/auth_signup.py`: new signature of `_prepare_signup_values`.
5. `models/portal_form_access.py`: create `ir.access` instead of `ir.model.access`.
6. `templates/contact_portal.xml`: full replacement of `portal.portal_my_details`; the `t-call`
   that `19.1-00-t-call` rewrote passes `head_contact_sharing` as a string.
7. `contact_sharing.js`: drop the unused `user` service; compare the Owl 2 compatibility layer
   with `project_sharing.js` of 20.0.
8. `form_status_indicator.xml`: check the class override on the 20.0 buttons.
9. `tests/test_portal_partner_access.py`: `groups_id` is `group_ids`.

## What was checked and not found

- No `<tree>`, `attrs`, `states`, `_sql_constraints`, `type='json'` routes, `self._cr`,
  `self._context`, `self._uid`, submodules, `migrations/` folders or lint configuration.
- Not checked: anything in the production database (Studio views and fields, website copies,
  server actions, mail templates, installed modules). Not installed on 20.0: no runtime.
