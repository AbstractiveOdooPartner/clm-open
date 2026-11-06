CLM Contact Manager Website Fix
===============================

Summary
-------

Zorgt dat het formulier op Mijn account ook laadt wanneer de website van Odoo geïnstalleerd is.

Functional
----------

- [PEP-MIJN-ACCOUNT-WEBSITE] Open Mijn account als lid vanuit het menu van de website: het
  formulier met je gegevens verschijnt volledig en je krijgt geen foutmelding.

Technical
---------

- PEP-MIJN-ACCOUNT-WEBSITE: `website` patches the link dialog of the editor
  (`website/static/src/js/editor/editor.js` in 17.0), which needs `website/static/src/js/utils.js`
  and the autocomplete components. The bundle `clm_contact_manager.webclient` loads that patch
  but not its dependencies, so the iframe stops on an unmet dependency. This module adds the 3
  paths to the bundle. Same fix as `website_form_project` in core. `auto_install`: it installs
  with `website` and `clm_contact_manager` together.
